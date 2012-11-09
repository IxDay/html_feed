import utils


__author__ = 'mvidori'


from bs4 import BeautifulSoup
import yaml
from pages import Pages

def beautifulSoup():
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>

    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """
    soup = BeautifulSoup(html_doc)
    print(soup.prettify())


def pyYAML():
    f = open('onani.yml')
    y = yaml.load(f.read())

    f.close()
    utils.initialize(y)

def test_dict():
    toto = {}
    toto['titi'] = {}
    print(toto)

if __name__ == "__main__":
#    beautifulSoup()
    pyYAML()
#    test_dict()
