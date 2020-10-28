from webapp.models import db

class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), unique=True, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_finish = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=True)
    #img_url = db.Column(db.String(100), nullable=True)
    #img_data = db.Column(db.LargeBinary)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='events')
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref='events')

    def __repr__(self): 
        return '<Events {} {}>'.format(self.title, self.url)
