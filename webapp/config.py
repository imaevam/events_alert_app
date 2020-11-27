from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'dfdsfsd34534ewfsfsd33red'

REMEMBER_COOKIE_DURATION = timedelta(days=5)  # Длительность сохранения статуса авторизации
MAIL_SERVER = 'smtp.mail.ru'
MAIL_PORT = 587
MAIL_USE_SSL = True
MAIL_USERNAME = "imaevam@list.ru"
MAIL_PASSWORD = 'ehehoz88'
DB_PATH = r"C:\projects\final\events_alert_app\events_alert_app\webapp.db" 
