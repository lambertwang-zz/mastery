
class Noun:
    def __init__(self, names, importance = 1):
        self.names = tuple(names)
        self.importance = importance

class Thing(Noun):
    def __init__(self, names, weight, **kwargs):
        super(Thing, self).__init__(names, **kwargs)
        self.weight = weight
