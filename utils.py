from objects import Link,TagRetriever, LinkDownload


__author__ = 'mvidori'

def delete_duplicates(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]



def initialize(filename):

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


    def parse_links(struct, document,path):
        if isinstance(document, list):
            for elt in document:
                if isinstance(elt, dict):
                    link = link_class(elt['entitled'],path)
                    link.courses = elt['courses']
                else:
                    link = link_class(elt,path)
                struct += [link]
        else:
            for key, value in document.items():
                struct[key] = type(value)()
                parse_links(struct[key], value,path+[key])


    def parse(struct, document, part):
        for key, value in document.items():
            if key in struct:
                parse(struct[key], value,part)
            else:
                links = get_links(struct)
                for link in links:
                    if part =='next':
                        link.next = TagRetriever('a',value)
                    elif part == 'path':
                        link.set_path(value)
                    elif part == 'parsing':
                        link.tag_retrievers += [TagRetriever(key,value)]

    import yaml
    with open(filename,'r') as f:
        try :
            document = yaml.load(f.read())
        except IOError :
            raise

    if 'path' in document :
        link_class = LinkDownload
    else:
        link_class = Link

    links_struct = {}
    parse_links(links_struct, document['links'],[])
    parse(links_struct, document['parsing'],'parsing')
    parse(links_struct, document['next'],'next')

    if 'path' in document :
        parse(links_struct, document['path'],'path')

    return get_links(links_struct)


