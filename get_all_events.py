from webapp import create_app
from webapp.base import get_payload, collect_details



app = create_app()
with app.app_context():
    categories = [('concert', 'concerts'), ('movie', 'cinema'), ('theatre', 'theatre'), ('exhibition', 'exhibitions')]
    for category_name, category_link in categories:
        data = get_payload(f'msk/{category_link}/')['Widget']['CardsCarousels']
        result = collect_details(data, category_name)

