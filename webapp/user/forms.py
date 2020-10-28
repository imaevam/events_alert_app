from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from webapp.user.models import User
from wtforms import BooleanField, StringField, PasswordField, \
                    SubmitField, RadioField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
    # remember_me - Функционал "запоминания" пользователя


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    first_name = StringField('Имя', validators=[DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    profile_picture = FileField('Фотография', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    birthday = DateTimeField('Дата рождения', format='%d.%m.%Y')
    gender = RadioField('Пол', choices=[('М', 'Male'), ('Ж', 'Female')])
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с таким именем уже зарегистрирован")


    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с такой электронной почтой уже зарегистрирован")