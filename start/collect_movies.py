from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    movie_lst = get_payload('msk/cinema')['Widget']['CardsCarousels']
    category = 'movie'
    result = collect_details(movie_lst, category)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
