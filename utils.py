from objects import Link,TagRetriever


__author__ = 'mvidori'

def delete_duplicates(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

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
    def parse_links(struct, document,path):
        if isinstance(document, list):
            for elt in document:
                if isinstance(elt, dict):
                    link = Link(elt['entitled'],path)
                    link.courses = elt['courses']
                else:
                    link = Link(elt,path)
                struct += [link]
        else:
            for key, value in document.items():
                struct[key] = type(value)()
                parse_links(struct[key], value,path+[key])


    def parse_parsing_next(struct, document, part):
        for key, value in document.items():
            if key in struct:
                parse_parsing_next(struct[key], value,part)
            else:
                links = get_links(struct)
                for link in links:
                    if part =='next':
                        link.next = TagRetriever('a',value)
                    elif part == 'path':
                        link.set_path(value)
                    elif part == 'parsing':
                        link.tag_retrievers += [TagRetriever(key,value)]


    links_struct = {}
    parse_links(links_struct, document['links'],[])
    parse_parsing_next(links_struct, document['parsing'],'parsing')
    parse_parsing_next(links_struct, document['next'],'next')
    parse_parsing_next(links_struct, document['path'],'path')

    return get_links(links_struct)


