from flask import Flask, render_template
from webapp.models import db



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('start.html')

    return app