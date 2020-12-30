from upylib.net.url import get_url
from upylib.util.parser import HTMLParser
from bs4 import BeautifulSoup


def test_html_parser():
    html = get_url("https://naver.com")
    # parser = HTMLParser(html)
    # parser.run()
    bs = BeautifulSoup(html)
    print(bs.text)
    assert True