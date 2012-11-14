__author__ = 'mvidori'

import utils

class Link:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.courses = []
        self.catchers = {}
        self.next = {}
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
        def get_html_feed(link, fail_on_error):
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


        def parse_html(html_feed,link):
            import bs4
            import re

            soup = bs4.BeautifulSoup(html_feed, "html5lib")

            for tag, attrs in self.catchers.items():
                self.elements[tag] = []
                for attr, values in attrs.items():
                    for value in values:
                        regex = re.compile(
                            value['entitled'].format(*value['regex']))
                        self.elements[tag] += soup.find_all(tag,
                                {attr: regex})

            next = soup.find_all('a', self.next)
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


        self.get_links()

        if end is None:
            end = len(self.links)

        for index, link in enumerate(self.links):
            next = link
            while next is not None:
                html_feed = get_html_feed(next, fail_on_error)
                if html_feed is not None:
                    next = parse_html(html_feed,next)
                print next
            if index == end:
                break

        for elt in self.elements.values():
            utils.delete_duplicates(elt)
