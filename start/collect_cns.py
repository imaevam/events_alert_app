from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    concert_lst = get_payload('msk/concerts/')['Widget']['CardsCarousels']
    category = 'concert'
    result = collect_details(concert_lst, category)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

