from base import get_payload, save_img, convert_date, collect_details
import pprint


if __name__ == "__main__":
    exhibition_lst = get_payload('msk/exhibitions/')['Widget']['CardsCarousels']
    category = 'exhibition'
    result = collect_details(exhibition_lst, category)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
