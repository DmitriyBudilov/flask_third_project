from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, TelField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class Registration(FlaskForm):
    mail = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class Login(FlaskForm):
    mail = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', render_kw={'autofocus': 'True', 'required': 'True'}, validators=[DataRequired()])
    address = StringField('Адрес', render_kw={'placeholder': 'ул.Ленина, дом.#, кв.#'}, validators=[DataRequired()])
    mail = EmailField('Электронная почта', render_kw={'placeholder': 'yuormail@host.com'})
    phone = TelField('Телефон', render_kw={'placeholder': '8 912 345 6789', 'pattern': '8[0-9]{10}'})
    submit = SubmitField('Оформить заказ')