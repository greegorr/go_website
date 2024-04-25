from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    title = StringField('Игроки', validators=[DataRequired()])
    content = TextAreaField("Ход")
    move = SubmitField('Сделать ход')
    is_private = BooleanField("Личное")
    submit = SubmitField('Сохранить')
