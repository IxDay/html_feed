from objects import Link


__author__ = 'mvidori'


def initialize(document):
    links_struct = {}


    def parse_links(struct,document):
        if document.has_key("link") :
            for elt in document['link']:
                Link(elt)

        else :
            for key in document:
                if document[key].has_key("link") :
                    struct[key] = []
                else:
                    struct[key] = {}
                parse_links(struct[key],document[key])

    parse_links(links_struct, document["links"])
    print(links_struct)

