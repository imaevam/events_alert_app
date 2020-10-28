from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.models import db

Model = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship


class User(Model, UserMixin):  # Множественное наследование
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50), index=True, unique=True, nullable=False)
    password = Column(db.String(50), nullable=False)
    email = Column(db.String(120), unique=True, nullable=False)
    first_name = Column(db.String(50), nullable=False)
    last_name = Column(db.String(50), nullable=False)
    profile_picture = Column(db.String(255), nullable=True)
    gender = Column(db.Enum('male', 'female', name='gender'))
    birthday = Column(db.Date, nullable=False)
    role = Column(db.String(10), index=True)
    subscribed_events = relationship("Subscription", back_populates="user", lazy="dynamic")

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)  # true \ false

    def is_subscribe(self):
        sub = UserEvents(user_id=current_user.id)
        db.session.add(sub)
        db.session.commit()

    def unsubscribe(self):
        sub = UserEvents.query.filter_by(user_id=current_user.id).first()
        db.session.delete(sub)
        db.session.commit()

    @property  # является ли пользователь администратором
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return 'User name={} id={}'.format(self.username, self.id)


class UserEvents(Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, ForeignKey('user.id'))
    event_id = Column(db.Integer, ForeignKey('event.id'))
    user = relationship('User', backref='events')
    event = relationship('Event', backref='users')


"""class Subscription(Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, ForeignKey("user.id"))
    subscription_id = Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'User {} is subscribed to {}'.format(self.user_id, self.subscription_id)"""
