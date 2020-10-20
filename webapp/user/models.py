from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash 

from webapp.models import db


class User(db.Model, UserMixin):  # Множественное наследование
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False) 
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Enum('male', 'female', name='gender'))
    birthday = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(10), index=True)
    #registered_on = db.Column(db.DateTime, nullable=False)
    #last_activity = db.Column(db.DateTime, nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) #true \ false

    @property  # Класс должен сообщать нам, является ли пользователь администратором
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return 'User name={} id={}'.format(self.username, self.id)
        
