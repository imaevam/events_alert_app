from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    movie_lst = get_payload('msk/cinema')['Widget']['CardsCarousels']
    result = collect_details(movie_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
