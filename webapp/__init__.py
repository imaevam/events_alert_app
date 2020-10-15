from flask import Flask, render_template
# from events_alert_app.forms import LoginForm
from webapp.model import db, Event

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Ближайшие события'
        events = Event.query.all() # ADD SORT BY DATE
        return render_template('base.html', page_title=title, events=events)
    '''
    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login-form)
    '''
    
    return app

# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
