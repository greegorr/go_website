from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from board import *
from forms.game import GameForm
from forms.user import RegisterForm, LoginForm
from data.game import Game
from data.users import User
from data import db_session, game_api

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': "bad request"}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/game', methods=['GET', 'POST'])
@login_required
def add_game():
    draw_board("0" * 361)
    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = Game()
        game.title = form.title.data
        # game.content = form.content.data
        game.content = "0"*361
        game.is_private = form.is_private.data
        current_user.game.append(game)
        game.content += draw_board(move(form.content.data, game.content))
        db_sess.merge(current_user)
        db_sess.commit()
        a = db_sess.query(Game).filter(Game.title==game.title, Game.user == current_user).first()
        # print(a.id)
        # return redirect('/')
        return redirect(f'/game/{a.id}')
    return render_template('game.html', title='Добавление партию', form=form)


@app.route('/game_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def game_delete(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
    if game:
        db_sess.delete(game)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/game/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_game(id):

    form = GameForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
        # print(game.content)
        draw_board(game.content)
        if game:
            form.title.data = game.title
            form.content.data = ""
            form.is_private.data = game.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        data = form.content.data
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
        if game:
            game.title = form.title.data
            game.content += draw_board(move(data, game.content))
            game.is_private = form.is_private.data
            db_sess.commit()
            return render_template('game.html', title='Редактирование партию', form=form)
            # return redirect('/')
        else:
            abort(404)
    return render_template('game.html', title='Редактирование партию', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        game = db_sess.query(Game).filter((Game.user == current_user) | (Game.is_private != True))
    else:
        game = db_sess.query(Game).filter(Game.is_private != True)
    return render_template("index.html", game=game)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/go_game.db")
    app.register_blueprint(game_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
