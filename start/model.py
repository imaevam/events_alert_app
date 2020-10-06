from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model): # атрибуты, поля в таблице
    id = db.Column(db.Integer, primary_key=True) # целое число, первичный ключ, бд будет его индексировать
    title = db.Column(db.String, nullable=False) # nullable -может ли это значение не быть в сопоставляемых данных, просим БД проверять нас
    url = db.Column(db.String, unique=True, nullable=False) #unique - url у каждой новости уникальный
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.Text, nullable=False)
    place = db.Column(db.String, nullable=True)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('caregory.id'))
    resourse_id = db.Column(db.Integer, db.ForeignKey('resourse.id'))

    def __repr__(self): # магический метод, чтобы в дальнейшем при получении обьекта понимать что это за объект
        return '<Events {} {}>'.format(self.title, self.url)


class User(db.Model, UserMixin):   #множественное наследование; def is_authenticated и тд
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False) # ограничение по длине; те, колонки по которым в дальнейшем будем фильтровать запросы имеет смысл делать индексами, т.к. поиск по индексу быстрее
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Enum('male', 'female', name='gender'))  #???
    birthday = db.Column(db.Date, nullable=False)
    notify_bday = db.Column(db.Boolean)
    registered_on = db.Column(db.Date, nullable=False)
    last_activity = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(10), index=True)
    resourse_id = db.Column(db.Inteder, db.ForeignKey('resourse.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) #true \ false

    def __repr__(self):
        return '<User {}>'.format(self.username)
  
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    resourse_id = db.Column(db.Integer, db.ForeignKey('resourse.id'))

    def __repr__(self):
        return '<Category: {}>'.format(self.name_category)


class Resourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Resourse: {}>'.format(self.name_resourse)
