from flask import request
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from webapp.event.models import Event


class CommentForm(FlaskForm):
    event_id = HiddenField('ID события', validators=[DataRequired()])
    comment_text = StringField('Текст комментария', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validates_news_id(self, event_id):
        if not Event.query.get(event_id.data):
            raise ValidationError('Вы пытаетесь прокомментировать событие с несуществующим id')


class SearchForm(FlaskForm):
    q = StringField(('Поиск'), validators=[DataRequired()], render_kw={"class": "form-control"})
    # браузер отправит форму, когда вы нажмете Enter с фокусом на поле, поэтому кнопка не нужна

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
