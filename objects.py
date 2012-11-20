__author__ = 'mvidori'

import utils, re, bs4, urllib,os

class Link:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.courses = []
        self.tag_retrievers = []
        self.next = None
        self.elements = {}
        self.__os_path = os.getcwd()

    def set_path(self,path):
        path_tmp = os.path.join(self.__os_path,path)
        if not os.path.exists(path_tmp) :
            path_tmp = os.getcwd()
        self.__os_path = os.path.join(path_tmp,*self.path)

    def get_path(self):
        return self.__os_path

    def __repr__(self):
        return 'Link({})'.format(self.name)


    def set_element(self, tag, elements):
        if tag not in self.elements:
            self.elements[tag] = []

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


    def get_html_feed(self,link,fail_on_error=False):
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


    def get_elements(self, start=0, end=None, fail_on_error=False):
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
                html_feed = self.get_html_feed(next,fail_on_error)
                if html_feed is not None:
                    next = parse_html(html_feed, next)
                print next
            if index == end:
                break

        for elt in self.elements.values():
            utils.delete_duplicates(elt)


    def manipulate_elements(self,callback,tag_reference=None):

        if tag_reference is None :
            for tag_reference in self.elements.keys():
                self.manipulate_elements(callback,tag_reference)
        else:
            for element in self.elements[tag_reference]:
                callback(element)


class TagRetriever():
    def __init__(self, tag, attrs):
        self.tag_reference = tag
        self.tag = tag.partition(' ')[0]
        self.re_type = type(re.compile(''))

        if 'needed' in attrs:
            self.needed = attrs['needed']
        else:
            self.needed = attrs
        self.pre_treatment(self.needed)

        if 'not_needed' in attrs:
            self.not_needed = attrs['not_needed']
            self.pre_treatment(self.not_needed)
        else:
            self.not_needed = None


    def pre_treatment(self, struct):
        if isinstance(struct, dict):
            if 'entitled' in struct and 'regex' in struct:
                struct = re.compile(struct['entitled'].format
                    (*struct['regex']))
            elif 'entitled' in struct:
                struct = struct['entitled']
            else:
                for key, value in struct.items():
                    struct[key] = self.pre_treatment(value)
        elif isinstance(struct, list):
            for index, value in enumerate(struct):
                struct[index] = self.pre_treatment(value)

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