from webapp.models import db
from datetime impirt datetime
from sqlalchemy.orm import relationship


class Event(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=False)
    date_start = db.Column(db.Date, nullable=True)
    date_finish = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    place = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    price = db.Column(db.DECIMAL(10, 2), nullable=True)
    img_url = db.Column(db.String(200), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='events')
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref='events')

    def __repr__(self):
        return '<Events {} {}>'.format(self.title, self.url)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),  # ondelete='CASCADE' - если удаляется новость- удаляются все к ней комментарии автоматически
        index=True
    )
    event = relationship('Event', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

