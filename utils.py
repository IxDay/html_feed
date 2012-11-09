from objects import Link


__author__ = 'mvidori'


def initialize(document):
    def parse_links(struct,document):
        for key in document:
            if isinstance(document[key],list) :
                struct[key] = []
                for elt in document[key]:
                    link = Link(elt['link'])
                    if elt.has_key('courses'):
                        link.courses = elt['courses']
                    struct[key].append(link)

            else:
                struct[key] = {}
                parse_links(struct[key],document[key])

    def parse_parsing(struct,document):
        pass

    links_struct = {}
    parse_links(links_struct, document["links"])


