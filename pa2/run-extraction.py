import sys
from main import extract_rtv_regex, extract_overstock_regex, extract_24ur_regex, extract_kosarka_regex
from main import extract_rtv_xpath, extract_overstock_xpath, extract_24ur_xpath, extract_kosarka_xpath
from main import webstemmer_pair

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run-extraction.py [A/B/C]")
        sys.exit(1)

    algorithm_type = sys.argv[1]
    if algorithm_type not in ['A', 'B', 'C']:
        print("Invalid algorithm type. Choose from: A, B, C")
        sys.exit(1)

    if algorithm_type == 'A':
        extract_rtv_regex(open("./webpages/rtvslo.si/rtvslo-2.html", "r", encoding="utf-8"))
        extract_overstock_regex(open("./webpages/overstock.com/jewelry02.html", "r", encoding="latin-1"))
        extract_24ur_regex(open("./webpages/24ur.com/novica2.html", "r", encoding="utf-8"))
        extract_kosarka_regex(open("./webpages/kosarka.si/novica2.html", "r", encoding="utf-8"))
    elif algorithm_type == 'B':
        extract_rtv_xpath(open("./webpages/rtvslo.si/rtvslo-2.html", "r", encoding="utf-8"))
        extract_overstock_xpath(open("./webpages/overstock.com/jewelry02.html", "r", encoding="latin-1"))
        extract_24ur_xpath(open("./webpages/24ur.com/novica2.html", "r", encoding="utf-8"))
        extract_kosarka_xpath(open("./webpages/kosarka.si/novica2.html", "r", encoding="utf-8"))
    elif algorithm_type == 'C':
        webstemmer_pair("./webpages/rtvslo.si/rtvslo-1.html", "utf-8", "./webpages/rtvslo.si/rtvslo-2.html", "utf-8")
        webstemmer_pair("./webpages/overstock.com/jewelry01.html", "latin-1", "./webpages/overstock.com/jewelry02.html", "latin-1")
        webstemmer_pair("./webpages/24ur.com/novica1.html", "utf-8", "./webpages/24ur.com/novica2.html", "utf-8")
        webstemmer_pair("./webpages/kosarka.si/novica1.html", "utf-8", "./webpages/kosarka.si/novica2.html", "utf-8")