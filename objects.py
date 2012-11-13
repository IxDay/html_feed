__author__ = 'mvidori'


class Link:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.catchers = {}
        self.next = {}


    def __repr__(self):
        return 'Link({})'.format(self.name)