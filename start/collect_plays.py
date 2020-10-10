from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    theatre_lst = get_payload('msk/theatre/')['Widget']['CardsCarousels']
    result = collect_details(theatre_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
