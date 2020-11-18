from flask_sqlalchemy import SQLAlchemy
from webapp.search import add_to_index, remove_from_index, query_index

db = SQLAlchemy()


class SearchableMixin(object):
    @classmethod  # cls, метод получает в качестве первого аргумента класс, а не экземпляр. 
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod  # какие объекты будут добавлены, изменены и удалены
    def before_commit(cls, session):
        session._changes = {  # словарь для записи этих объектов в месте, которое переживет все фиксации сеанса
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod  # сеанс завершен, поэтому можно внести изменения на стороне Elasticsearch.
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):  # для обновления индекса со всеми данными из реляционной стороны.
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)  # устанавливают обработчики событий, которые вызывают before и after для каждой фиксации
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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
