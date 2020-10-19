from flask import Blueprint, render_template  # current_app, когда выведем события
from webapp.event.models import db, Event

blueprint = Blueprint('event', __name__)


@blueprint.route('/')
def index():
    title = 'Куда сходить и чем заняться в Москве'
    # Вывести события 
    return render_template('start.html', page_title=title)