from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from webapp.user.models import User
from wtforms import BooleanField, StringField, PasswordField, \
                    SubmitField, RadioField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError


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
    profile_picture = FileField('Фотография', validators=[FileAllowed(['jpg', 'png'])])
    birthday = DateField('Дата рождения', format='%d.%m.%Y')
    gender = RadioField('Пол', choices=[('male', 'Male'), ('female', 'Female')])
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с таким именем уже зарегистрирован")


    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с такой электронной почтой уже зарегистрирован")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),
                        Email("Неправильно введен Email")])
    submit = SubmitField("Сбросить пароль", render_kw={"class": "btn btn-primary"})


class ResetPasswordForm(FlaskForm):  # update password form 
    email = StringField("email",
                        validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=5, max=30, 
                                message="Длина пароля должна быть не менее 5 символов и не более 30 символов"),
                                         Regexp("^(?=.*[A-Z]+)(?=.*[!@#$&*])(?=.*[0-9]+)(?=.*[a-z]+).{5,}$", message="Пароль должен содержать заглавные буквы, числа и знаки препинания.")])
    confirm_password = PasswordField("Повторите пароль", validators=[DataRequired(),
                            EqualTo("password", 'Пароли должны совпадать')])
    submit = SubmitField("Обновить пароль", render_kw={"class": "btn btn-primary"})
