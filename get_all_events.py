from webapp import create_app
from webapp.parse import parse

app = create_app()
with app.app_context():
    parse()