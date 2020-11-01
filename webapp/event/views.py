from flask import Blueprint, flash, redirect, render_template, url_for  # current_app выведем события
from flask_login import current_user, login_required
from webapp.event.forms import CommentForm
from webapp.event.models import Comment, Event
from webapp.user.models import UserEvents
from webapp.models import Category
from webapp.models import db


blueprint = Blueprint('event', __name__)


@blueprint.route('/')
def index():
    title = 'Куда сходить и чем заняться в Москве'
    events = Event.query.order_by(Event.date_start).all()
    return render_template('event/index.html', page_title=title, events=events)     

  
@blueprint.route('/category/<category_id>')
def event_by_category(category_id):
    category_events = Event.query.filter(Event.category_id == category_id).order_by(Event.date_start).all()
    return render_template('event/index.html', events=category_events) 


@blueprint.route('/event/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment_text, event_id=form.event_id, user_id=current_user.id)  # ??
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')


@blueprint.route('/subscribe/<int:event_id>/')
def subscribe_event(event_id):
    is_user_subscribed = UserEvents.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if is_user_subscribed:
        return redirect(url_for('event.index'))
    else:
        current_user.subscribe(event_id=event_id)
        return redirect(url_for('event.index'))


@blueprint.route('/unsubscribe/<int:event_id>/')
def unsubscribe_event(event_id):
    is_user_subscribed = UserEvents.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if is_user_subscribed:
        current_user.unsubscribe(event_id=event_id)
        return redirect(url_for('event.index'))
    else:
        return redirect(url_for('event.index'))
        