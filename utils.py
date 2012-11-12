from objects import Link


__author__ = 'mvidori'


def initialize(document):
    def parse_links(struct, document):
        if isinstance(document, list):
            for elt in document:
                if isinstance(elt,dict):
                    link = Link(elt['entitled'])
                    link.courses = elt['courses']
                else:
                    link = Link(elt)
                struct += [link]
        else:
            for key, value in document.items():
                struct[key] = type(value)()
                parse_links(struct[key], value)


    def parse_parsing(struct, document):
        for key, value in document.items():
            if key in struct :
                parse_parsing(struct[key],value)
            else:
                parse_catchers(struct,key,value)

    def get_links(struct):
        if isinstance(struct,Link):
            return

    def parse_catchers(struct,tag,attr):
        pass








    links_struct = {}
    parse_links(links_struct, document['links'])
    parse_parsing(links_struct, document['parsing'])


#    print(links_struct)

