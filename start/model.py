from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash 

db = SQLAlchemy()

class Event(db.Model): # атрибуты, поля в таблице
    id = db.Column(db.Integer, primary_key=True) # целое число, первичный ключ, бд будет его индексировать
    title = db.Column(db.String, nullable=False) # nullable -может ли это значение не быть в сопоставляемых данных, просим БД проверять нас
    url = db.Column(db.String, unique=True, nullable=False) #unique - url у каждой новости уникальный
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)
    place = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=True)


    def __repr__(self): # магический метод, чтобы в дальнейшем при получении обьекта понимать что это за объект
        return '<Events {} {}>'.format(self.title, self.url)

class User(db.Model, Mixin):   #множественное наследование; def is_authenticated и тд
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False) # ограничение по длине; те, колонки по которым в дальнейшем будем фильтровать запросы имеет смысл делать индексами, т.к. поиск по индексу быстрее
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255))
    gender = db.Column(db.Enum('male', 'female', name='gender'))  #???
    birthday = db.Column(db.DateTime)
    notify = db.Column(db.Boolean)
    registered_on = db.Column(db.Date, nullable=False)
    last_activity = db.Column(db.DateTime)
    role = db.Column(db.String(10), index=True)

    def __init__(self, username, password, first_name, last_name, email, gender='male'):
        UserMixin.__init__(self, role)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password) 
        self.profile_picture = 'user_files/{}/default_{}.png'.format(self.storage_hash, gender)
        self.gender = gender
        self.registered_on = datetime.datetime.now()
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.username)

    #методы класа

    #отдельно class LoginForm \ RegistrationForm ?
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_category = db.Column(db.String(50), index=True, nullable=False)

    def __repr__(self):
        return '<Category: {}>'.format(self.name_category)

    #методы класса


class Resourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_resourse = db.Column(db.String(100), index=True, nullable=False)

    def __repr__(self):
        return '<Resourse: {}>'.format(self.name_resourse)


    #методы класса