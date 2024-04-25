import flask
from flask import jsonify, make_response, request
from . import db_session
from .game import Game

blueprint = flask.Blueprint(
    "game_api",
    __name__,
    template_folder='templates'
)


@blueprint.route("/api/game")
def get_game():
    db_sess = db_session.create_session()
    game = db_sess.query(Game).all()
    return jsonify(
        {
            'game':
                [item.to_dict(only=("title", 'content', "user.name")) for item in game]
        }
    )


@blueprint.route("/api/game/<int:game_id>", methods=["GET"])
def get_one_game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).get(game_id)
    if not game:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(
        {
            "game": game.to_dict(only=(
                'title', "content", "user.id", "is_private"
            ))
        }
    )


@blueprint.route("/api/game", methods=["POST"])
def create_game():
    if not request.json:
        return make_response(jsonify({'error': "Empty request"}), 400)
    elif not all(key in request.json for key in ["title", 'content', "user_id", "is_private"]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    db_sess = db_session.create_session()
    game = Game(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json["user_id"],
        is_private=request.json["is_private"]
    )
    db_sess.add(game)
    db_sess.commit()
    return jsonify({"id": game.id})


@blueprint.route('/api/game/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).get(game_id)
    if not game:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(game)
    db_sess.commit()
    return jsonify({'success': 'OK'})
