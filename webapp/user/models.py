from datetime import datetime
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.models import db

Model = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship

class ServiceMixin:
    @declared_attr
    def created_at(cls):
        return Column(db.DateTime, default=datetime.utcnow)

    @declared_attr
    def last_modified(cls):
        return Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow)

    
class User(Model, UserMixin, ServiceMixin):  # Множественное наследование
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50), index=True, unique=True, nullable=False)
    password = Column(db.String(50), nullable=False)
    email = Column(db.String(120), unique=True, nullable=False)
    first_name = Column(db.String(50), nullable=False)
    last_name = Column(db.String(50), nullable=True)
    profile_picture = Column(db.String(255), nullable=True)
    gender = Column(db.Enum('male', 'female', name='gender'))
    birthday = Column(db.Date, nullable=True)
    is_active = Column(db.Boolean, nullable=False, default=True)
    role = Column(db.String(10), index=True)
    subscribed_events = relationship("UserEvents", back_populates="user", lazy="dynamic")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)  # true \ false

    def subscribe(self, event_id):
        sub = UserEvents(user_id=self.id, event_id=event_id)
        db.session.add(sub)
        db.session.commit()

    def unsubscribe(self, event_id):
        sub = UserEvents.query.filter_by(user_id=self.id, event_id=event_id).first()
        db.session.delete(sub)
        db.session.commit()

    @property  # является ли пользователь администратором
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return 'User name={} id={}'.format(self.username, self.id)


class UserEvents(Model):  # Subscription
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE'), index=True)
    event_id = Column(db.Integer, ForeignKey('event.id', ondelete='CASCADE'), index=True)
    user = relationship('User', backref='events')
    event = relationship('Event', backref='users')

    def __repr__(self):
        return 'Subscribe={}'.format(self.id)
