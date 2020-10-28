from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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
# session_options={'autocommit': True}
