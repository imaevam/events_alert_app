from flask import Flask, render_template
from model import db


def create_app():
    app = Flask(__name__)
    #config
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('start.html')

    return app