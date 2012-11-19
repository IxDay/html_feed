__author__ = 'mvidori'

import utils, re, bs4

class Link:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.courses = []
        self.tag_retrievers = []
        self.next = None
        self.elements = {}


    def __repr__(self):
        return 'Link({})'.format(self.name)


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


    def get_elements(self, start=0, end=None, fail_on_error=False):
        def get_html_feed(link):
            import urllib2

            try:
                html_feed = urllib2.urlopen(link)
                try:
                    return html_feed.read()
                finally:
                    html_feed.close()
            except urllib2.HTTPError:
                if fail_on_error:
                    raise
                return None
            except urllib2.URLError:
                if fail_on_error:
                    raise
                return None


        def parse_html(html_feed, link):
            def get_next(soup):
                next = soup.find_all(self.next)
                if len(next):
                    if 'http://' not in next:
                        return '{}/{}'.format(
                            link.rpartition('/')[0],
                            next[0].get('href')
                        )
                    else:
                        return next[0].get('href')
                else:
                    return None


            soup = bs4.BeautifulSoup(html_feed, "html5lib")

            for tag_retriever in self.tag_retrievers:
                self.elements[tag_retriever.tag] += soup.find_all(tag_retriever)
            return get_next(soup)


        self.get_links()

        if end is None or end > len(self.links):
            end = len(self.links)

        if end < 0:
            pass

        for index, link in enumerate(self.links):
            next = link
            while next is not None:
                html_feed = get_html_feed(next)
                if html_feed is not None:
                    next = parse_html(html_feed, next)
                print next
            if index == end:
                break

        for elt in self.elements.values():
            utils.delete_duplicates(elt)


class TagRetriever():
    def __init__(self, tag, attrs):
        self.tag = tag
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
            if isinstance(value_expected, self.re_type):
                return value_expected.search(value_retrieved)
            else:
                return value_expected == value_retrieved


        def retrieve_attr(tag, elements):
            for key, values in elements.items():
                if key == "or":
                    return any([retrieve_attr(tag, value) for value in values])
                elif key == "and":
                    return all([retrieve_attr(tag, value) for value in values])
                else:
                    if key in tag.attrs:
                        if isinstance(values, list):
                            return any([
                            compare_value(tag[key], value)
                            for value in values
                            ])
                        else:
                            return compare_value(tag[key], values)
                    else:
                        return False


        if self.not_needed is None:
            return retrieve_attr(tag, self.needed)
        else:
            return retrieve_attr(tag, self.needed)\
            and not retrieve_attr(tag, self.not_needed)


    def __call__(self, tag):
        return self.build_function(tag)