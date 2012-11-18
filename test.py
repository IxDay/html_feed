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

def test_func():
    list_func = []
    list_param = ['foo','bar']
    for i in list_param:
        def print_func():
            print(i)

        list_func += [print_func]

    for func in list_func:
        func()

def test_tag_retrieve():
    f = open('page.html')
    soup = BeautifulSoup(f.read())
    f.close()

    def retrieve(tag):
        import re
        toto = re.compile('left-skyscraper')

        if 'id' in tag.attrs and toto.match(tag.attrs['id']):
            print(tag)
        return True

    soup.find_all(retrieve)

test_tag_retrieve()

class TagRetriever():
    needed = {'src': [{'regex': ['.*([0-9])+'], 'entitled': 'http://c.mfcdn.net/store/manga/{}.jpg'}, {'entitled': 'toto'}, 'titi']}
    not_needed = {'or': [{'id': 'toto'}, {'class': 'tutu'}]}

    def __init__(self,tag,attrs):
        self.tag = tag
        if 'needed' in attrs:
            self.needed = attrs['needed']
        else:
            self.needed = attrs
        if 'not' in attrs :
            self.not_needed = attrs['not']
        else:
            self.not_needed = None

        self.function = self.build_function


    def build_function(self,tag):
        def eval_value(value):
            if isinstance(value,str):
                return value
            if isinstance(value,dict) and 'entitled' in value:
                if 'regex' in value:
                    return value['entitled'].format(value['regex'])
                else:
                    return value['entitled']



        def retrieve_attr(tag,elements):
            for key,values in elements.items():
                if key == "or":
                    return any([retrieve_attr(tag,value) for value in values])
                elif key == "and":
                    return all([retrieve_attr(tag,value) for value in values])
                else:
                    if tag.has_key(key):
                        if isinstance(values,list):
                            return any([tag['key'] == value for value in values])
                        else :
                            return tag['key'] == values
                    else:
                        return False

        if self.not_needed is None:
            return retrieve_attr(tag,self.needed)
        else:
            return retrieve_attr(tag,self.needed) \
                    and not retrieve_attr(tag,self.not_needed)


    def __call__(self,tag):
        return self.function(tag)

def test_parsing():
    f = open('page.html','r')
    beauty = BeautifulSoup(f.read(),'html5lib')
    f.close()


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



