from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    place = db.Column(db.String(50), nullable=True)
    price = db.Column(db.DECIMAL(10, 2), nullable=True)
    genre = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('caregory.id'))
    category = db.relationship('Category', backref='events')
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref='events')


    def __repr__(self): 
        return '<Events {} {}>'.format(self.title, self.url)


class User(db.Model, UserMixin):   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False) 
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Enum('male', 'female', name='gender'))  #???
    birthday = db.Column(db.Date, nullable=False)
    notify_on_bithday = db.Column(db.Boolean)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_activity = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) #true \ false

    def __repr__(self):
        return '<User {}>'.format(self.username)
  
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    
    def __repr__(self):
        return '<Category: {}>'.format(self.name_category)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)

    def __repr__(self):
        return '<Resource: {}>'.format(self.name_resourse)
