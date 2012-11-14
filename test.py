import utils


__author__ = 'mvidori'


from bs4 import BeautifulSoup
import yaml

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

    links_struct = utils.initialize(y)

    import urllib
    for link in utils.get_links(links_struct):
        for link_entitled in link.get_links():
            html_page = urllib.urlopen(link_entitled)
            html_page.read()




def test_dict():
    toto = {}
    toto['titi'] = {}
    print(toto)
#    toto = {}
#    toto += {'test':3}
#    print(toto)

def ternary():
    toto = 'test'
    test = (toto == 'test' and 'ok' or 'nok')
    print(test)

def test_splat():
    toto = ['toto','titi','tutu']
    print('{} {} {}'.format(*toto))


def test_for():
    i = 0
#    for x in range(25):
#        for y in range(25):
#            i += 1
#            print i
#            print x,y

    toto = [ [x,y] for x in range(25) for y in range(25)]
    print(toto)

def test_list():
    l1 = [1,2]
    l2 = [1,2,3]

def get_html_page():
    import urllib
    f = urllib.urlopen('http://mangafox.me/manga/onani_master_kurosawa/v04/c025/1.html')
    html_file = open('page.html','w')
    html_file.write(f.read())
    f.close()
    html_file.close()

def test_beautiful():
    f = open('page.html','r')
    html_feed = f.read()
    f.close()
    soup = BeautifulSoup(html_feed)


    f = open('onani.yml')
    y = yaml.load(f.read())
    f.close()

    links_struct = utils.initialize(y)
    link = utils.get_links(links_struct)[0]





if __name__ == "__main__":
#    beautifulSoup()
#    test_dict()
#    ternary()
#    test_splat()
#    test_for()
#    test_list()
#    pyYAML()
    test_beautiful()



