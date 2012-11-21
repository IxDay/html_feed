import os

__author__ = 'mvidori'

import re, bs4, urllib



class Link:
    __parsing = ['parse','next']

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.courses = []
        self.tag_retrievers = []
        self.elements = {}
        self.next = None


    @classmethod
    def add_parsing(cls,*parsing):
        cls.__parsing += parsing

    @classmethod
    def get_parsing(cls):
        return cls.__parsing

    def __repr__(self):
        return 'Link({})'.format(self.name)


    def callback(self,element):
        pass

    def set_element(self, tag, elements):
        if tag not in self.elements:
            self.elements[tag] = []
        else:
            elements = [element for element in elements if
                        element not in self.elements[tag]]

        if self.callback is not None:
            for element in elements:
                self.callback(element)

        self.elements[tag].extend(elements)


    def get_links(self):
        if not hasattr(self, 'links'):
            def course_generator(course):
                length = len(course['start'])

                for value in range(
                    int(course['start']),
                    int(course['end']) + 1,
                    int(course['step'])):
                    value = '{}{}'.format(
                        '0' * (length - len(str(value))),
                        value
                    )
                    yield value


            import itertools

            combinations = itertools.product(
                *[course_generator(course) for course in self.courses]
            )

            self.links = [self.name.format(*link) for link in combinations]
        return self.links


    def retrieve_elements(self, start=0, end=None, fail_on_error=False):
        def get_html_feed(link, fail_on_error=False):
            try:
                html_feed = urllib.urlopen(link)

                try:
                    return html_feed.read()
                except IOError:
                    if fail_on_error:
                        raise
                    return None
                finally:
                    html_feed.close()

            except IOError:
                if fail_on_error:
                    raise
                return None


        def parse_html(html_feed, link):
            def get_next(soup):
                next = soup.find_all(self.next)
                if not len(next):
                    return None

                if 'http://' not in next:
                    return '{}/{}'.format(
                        link.rpartition('/')[0],
                        next[0].get('href')
                    )
                else:
                    return next[0].get('href')


            soup = bs4.BeautifulSoup(html_feed, "html5lib")

            for tag_retriever in self.tag_retrievers:
                self.set_element(tag_retriever.tag_reference,
                                 soup.find_all(tag_retriever))
            return get_next(soup)


        self.get_links()

        if end is None or end > len(self.links):
            end = len(self.links)

        if end < 0:
            pass

        for index, link in enumerate(self.links):
            next = link
            while next is not None:
                html_feed = get_html_feed(next, fail_on_error)
                if html_feed is not None:
                    next = parse_html(html_feed, next)
            if index == end:
                break


    def manipulate_elements(self, callback, tag_reference=None):
        if tag_reference is None:
            for tag_reference in self.elements.keys():
                self.manipulate_elements(callback, tag_reference)
        else:
            for element in self.elements[tag_reference]:
                callback(element)


class LinkDownload(Link):
    def __init__(self, name, path):
        Link.__init__(self, name, path)
        self.__os_path = os.getcwd()

    def set_path(self,path):
        path_tmp = os.path.join(self.__os_path,path)
        if not os.path.exists(path_tmp) :
            path_tmp = os.getcwd()
        self.__os_path = os.path.join(path_tmp,*self.path)

    def get_path(self):
        return self.__os_path


    def callback(self,element):
        if not os.path.exists(self.__os_path):
            os.makedirs(self.__os_path)

        if element.name == 'img' :
            filename = os.path.join(self.__os_path,os.path.basename(element['src']))
            urllib.urlretrieve(element['src'],filename)


class TagRetriever():
    def __init__(self, tag, attrs):
        self.tag_reference = tag
        self.tag = tag.partition(' ')[0]
        self.re_type = type(re.compile(''))

        if 'needed' in attrs:
            self.needed = attrs['needed']
        else:
            self.needed = attrs
        TagRetriever.__pre_treatment(self.needed)

        if 'not_needed' in attrs:
            self.not_needed = attrs['not_needed']
            TagRetriever.__pre_treatment(self.not_needed)
        else:
            self.not_needed = None

    @staticmethod
    def __pre_treatment(struct):
        if isinstance(struct, dict):
            if 'entitled' in struct and 'regex' in struct:
                struct = re.compile(struct['entitled'].format
                    (*struct['regex']))
            elif 'entitled' in struct:
                struct = struct['entitled']
            else:
                for key, value in struct.items():
                    struct[key] = TagRetriever.__pre_treatment(value)
        elif isinstance(struct, list):
            for index, value in enumerate(struct):
                struct[index] = TagRetriever.__pre_treatment(value)

        return struct


    def build_function(self, tag):
        def compare_value(value_retrieved, value_expected):
            if isinstance(value_retrieved, list):
                value_retrieved = ' '.join(value_retrieved)
            if isinstance(value_expected, self.re_type):
                return value_expected.search(value_retrieved)
            else:
                return value_expected == value_retrieved


        def retrieve_attr(tag, struct):
            if tag.name != self.tag:
                return False

            #eval only the first element in the dictionnary others are not
            # considered
            key, value = struct.items()[0]
            if key == "or":
                return any([
                retrieve_attr(tag, {key: value})
                for key, value in value.items()
                ])
            elif key == "and":
                return all([
                retrieve_attr(tag, {key: value})
                for key, value in value.items()
                ])
            else:
                if key not in tag.attrs:
                    return False
                if isinstance(value, list):
                    return any(
                        [compare_value(tag[key], value)for value in value])
                else:
                    return compare_value(tag[key], value)


        if self.not_needed is None:
            return retrieve_attr(tag, self.needed)
        else:
            return retrieve_attr(tag, self.needed)\
            and not retrieve_attr(tag, self.not_needed)


    def __call__(self, tag):
        return self.build_function(tag)


class Parsing:
    def __init__(self,filename,link_object):
        self.filename = filename
        if isinstance(link_object,Link):
           self.link = link_object
        else:
            self.link = Link



    def parse(self):
        import yaml
        with open(self.filename,'r') as f:
            try :
                document = yaml.load(f.read())
            except IOError :
                raise