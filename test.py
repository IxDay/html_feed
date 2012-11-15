import utils


__author__ = 'mvidori'

from bs4 import BeautifulSoup
import yaml

def beautifulSoup():
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>

    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and
    their names were
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

    link = utils.initialize(y)[0]
    link.get_elements()
    print('toto')

def test_yml():
    f = open('onani.yml')
    y = yaml.load(f.read())
    f.close()



def test_tuple():
    tup = ('1', '2', '3')
    print(tup[2])

def test_dict():
#    fonctionne pas
#    toto = {}
#    toto += {'test':3}
#    print(toto)
#    toto = {'titi': {}}
#    print(toto.values())
#    if 'toto' in toto and toto['toto'] == 'ok':
#        print('ok')
    toto = True
    toto = toto or False
    print(toto)

def ternary():
    toto = 'test'
    test = (toto == 'test' and 'ok' or 'nok')
    print(test)

def test_splat():
    toto = ['toto', 'titi', 'tutu']
    print('{} {} {}'.format(*toto))

def test_for():
    i = 0
    #    for x in range(25):
    #        for y in range(25):
    #            i += 1
    #            print i
    #            print x,y

    toto = [[x, y] for x in range(25) for y in range(25)]
    print(toto)

def test_list():
    l1 = [1, 2]
    l2 = [1, 2, 3]

def get_html_page():
    import urllib

    f = urllib.urlopen(
        'http://mangafox.me/manga/onani_master_kurosawa/v04/c025/1.html')
    html_file = open('page.html', 'w')
    html_file.write(f.read())
    f.close()
    html_file.close()

def test_beautiful():
    f = open('onani.yml')
    y = yaml.load(f.read())
    f.close()

    links = utils.initialize(y)[0]
    links.get_elements()
    print('toto')

def test_format():
    print('test{}test'.format('test' * 0))

def test_urllib():
    import urllib2

    try:
        f = urllib2.urlopen("https://tresdfsdt.fr")
        print f.info()
    except urllib2.HTTPError:
        print("erreur HTTP")
        raise
    except urllib2.URLError:
        print("mauvaise url")
        raise

def test_class():
    class Toto:
        def __init__(self):
            self.name = 'test'


        def function_lambda(self, test='bla'):
            def internal():
                print(self.name)
                print(test)


            internal()



    var = Toto()
    var.function_lambda()
    var.function_lambda('titi')
test_class()


def test_parsing():
    f = open('page.html','r')
    beauty = BeautifulSoup(f.read(),'html5lib')
    f.close()

    next = {'link 1': {'not': {'onclick': 'next_chapter()'}, 'needed': {'class': 'btn next_page'}}}
    catchers = {'img 1': {'not': {'id': 'toto'}, 'needed': {'src': {'regex': ['.*([0-9])+'], 'entitled': 'http://c.mfcdn.net/store/manga/{}.jpg'}}}}


    tag_to_retrieve = {'not': {'onclick': 'next_chapter()'}, 'needed': {'class': 'btn next_page'}}
    elements = {}

    def retrieve_tag(tag):
        if 'not' in tag_to_retrieve:
            pass














        found = False
        for attr,values in next['not']:
            if tag.has_key(attr):
                for value in values:
                    found = found and tag.attrs[attr] == values


        tag_not_needed = False
        tag_needed = False
        if 'needed' in next:
            needed = next['needed']
        else:
            needed = next

        for attr,value in next['not']:
            tag_not_needed = tag_not_needed and\
                             tag.has_key(attr) and\
                             tag.attrs[attr] == value



#    def has_class_but_no_id(tag):
#        if tag.has_key('style'):
#            print tag.attrs['style']
#        return tag.has_key('class') and not tag.has_key('id')


#    result = beauty.find_all(retrieve_tag() and )
#    print(result)


if __name__ == "__main__":
    pass
#    beautifulSoup()
#    test_dict()
#    ternary()
#    test_splat()
#    test_for()
#    test_list()
#    test_format()
#    test_urllib()
#    test_class()
#    test_tuple()
#    test_yml()
#    test_parsing()
#    pyYAML()
#    test_beautiful()



