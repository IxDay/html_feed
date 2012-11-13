__author__ = 'mvidori'



class Link:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.catchers = {}
        self.next = {}


    def __repr__(self):
        return 'Link({})'.format(self.name)


    def _course_generator(self, course):
        for value in range(
            int(course['start']),
            int(course['end']) + 1,
            int(course['step'])):
            yield value


    def get_links(self):
        import urllib


        generators = []
        for course in self.courses:
            generators.append(self._course_generator(course))

        for generator in generators:
            print(generator.next())





