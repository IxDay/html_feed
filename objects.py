__author__ = 'mvidori'


class Link:
    def __init__(self, name, courses=None, catchers=None):
        self.name = name
        if courses is None:
            self.courses = []
        else:
            self.courses = courses

        if catchers is None:
            self.catchers = {}
        else:
            self.catchers = catchers


    def __repr__(self):
        return 'Link({},{},{})'.format(self.name,self.courses,self.catchers)

