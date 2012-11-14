__author__ = 'mvidori'



class Link:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.catchers = {}
        self.next = {}



    def __repr__(self):
        return 'Link({})'.format(self.name)


    def get_links(self):
        if not hasattr(self,'links'):

            def course_generator(course):
                length = len(course['start'])

                for value in range(
                    int(course['start']),
                    int(course['end']) + 1,
                    int(course['step'])):

                    value = '{}{}'.format(
                        '0'*(length - len(str(value))),
                        value
                    )
                    yield value


            import itertools
            combinations = itertools.product(
                *[course_generator(course) for course in self.courses]
            )

            self.links = [self.name.format(*link) for link in combinations]
        return self.links
