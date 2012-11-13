from objects import Link


__author__ = 'mvidori'


def get_links(struct):
    if isinstance(struct, Link):
        return [struct]
    if not len(struct):
        return []
    if isinstance(struct, dict):
        struct = dict(struct)
        return get_links(struct.popitem()[1]) + get_links(struct)
    if isinstance(struct, list):
        struct = list(struct)
        return get_links(struct.pop()) + get_links(struct)

def initialize(document):

    def parse_links(struct, document):
        if isinstance(document, list):
            for elt in document:
                if isinstance(elt, dict):
                    link = Link(elt['entitled'])
                    link.courses = elt['courses']
                else:
                    link = Link(elt)
                struct += [link]
        else:
            for key, value in document.items():
                struct[key] = type(value)()
                parse_links(struct[key], value)


    def parse_parsing_next(struct, document, is_parsing):
        for key, value in document.items():
            if key in struct:
                parse_parsing_next(struct[key], value,is_parsing)
            else:
                links = get_links(struct)
                for link in links:
                    if is_parsing:
                        link.catchers[key] = value
                    else :
                        link.next[key] = value


    links_struct = {}
    parse_links(links_struct, document['links'])
    parse_parsing_next(links_struct, document['parsing'],True)
    parse_parsing_next(links_struct, document['next'],False)

    return links_struct

