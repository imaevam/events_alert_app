from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    concert_lst = get_payload('msk/concerts/')['Widget']['CardsCarousels']
    result = collect_details(concert_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

