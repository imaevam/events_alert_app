from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'dfdsfsd34534ewfsfsd33red'

REMEMBER_COOKIE_DURATION = timedelta(days=5)  # Длительность сохранения статуса авторизации
ELASTICSEARCH_URL = 'http://localhost:9200'
POSTS_PER_PAGE = 15