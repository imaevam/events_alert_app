from flask import abort, Blueprint, current_app, flash, g, redirect, request, render_template, url_for  # current_app выведем события
from flask_login import current_user, login_required

from webapp.event.forms import CommentForm, SearchForm
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


@blueprint.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('event.index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Event.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('event.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('event.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('event/search.html', title=('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


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
