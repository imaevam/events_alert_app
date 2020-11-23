from flask import (abort, Blueprint, current_app, flash, redirect,
                   request, render_template, url_for)
from flask_login import current_user, login_required

from sqlalchemy import or_
from webapp.event.forms import CommentForm, SearchForm
from webapp.event.models import Comment, Event
from webapp.user.models import UserEvents
from webapp.models import Category
from webapp.models import db
from connect_db import get_data_from_db_by_search


blueprint = Blueprint('event', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():    
    title = 'Куда сходить и чем заняться в Москве'
    events = Event.query.order_by(Event.date_start).all()
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('event/index.html', page_title=title, events=events, form=search)


@blueprint.route('/category/<category_id>')
def event_by_category(category_id):
    category_events = Event.query.filter(Event.category_id == category_id).order_by(Event.date_start).all()
    return render_template('event/index.html', events=category_events) 


@blueprint.route('/event/comment', methods=['POST'])
@login_required
def add_comment():
    pass


@blueprint.route('/event/<int:event_id>')  # проверка по id
def single_event(event_id):
    my_event = Event.query.filter(Event.id == event_id).first()
    form = CommentForm()
    if not my_event:
        abort(404)

    return render_template('event/single_event.html', event=my_event, comment_form=form)
        

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


@blueprint.route('/search')
def search_results(search):
    if search.validate_on_submit():
        search_str = f"%{search.search.data}%"
        search_result_data = get_data_from_db_by_search(search_str)
        #all_search_results = Event.query.filter_by(event_id=ids_str).first()
    return render_template('event/search_results.html', events=search_result_data, search_str=search_str)