from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()


class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    #date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False) #add True
    #category_id = db.Column(db.Integer, db.ForeignKey('caregory.id'))
    
    def __repr__(self): 
        return '<Events {} {}>'.format(self.title, self.url)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    resourse_id = db.Column(db.Integer, db.ForeignKey('resourse.id'))

    def __repr__(self):
        return '<Category: {}>'.format(self.name_category)


'''
class User(db.Model, UserMixin):   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False) 
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registered_on = db.Column(db.Date, nullable=False)
    last_activity = db.Column(db.Date, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def set_password(self, password):
        #self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) #true \ false

    def __repr__(self):
        return '<User {}>'.format(self.username)
'''  
