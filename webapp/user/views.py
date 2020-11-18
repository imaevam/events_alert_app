from flask import Blueprint, flash, render_template, redirect, url_for

from webapp.models import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User, UserEvents
from webapp.event.models import Event
from flask_login import current_user, login_user, logout_user


blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('event.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('event.index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно покинули личную страницу')
    return redirect(url_for('event.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('event.index'))
    form = RegistrationForm()
    title = 'Регистрация'
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
        last_name=form.last_name.data, gender=form.gender.data, birthday=form.birthday.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():  # field - название поля(username, email), errors - список строк с ошибками
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))


@blueprint.route('/subscribed')
def subscription():
    try:
        user_sub_events_id = [x.event_id for x in  UserEvents.query.filter(UserEvents.user_id == current_user.id).all()]
        events = Event.query.filter(Event.id.in_(user_sub_events_id)).all()
        return render_template('event/index.html', events=events) 
    except:
        title = 'Куда сходить и чем заняться в Москве'
        events = Event.query.order_by(Event.date_start).all()
        return render_template('event/index.html', page_title=title, events=events)
