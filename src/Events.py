class Event:
    isAbstract = True

    def __init__(self, store):
        this.store = store
    
    def resultDiffs(self, noun):
        return []

    def modify(self, store, subject):
        return store


class WalkEvent(Event):
    isAbstract = False

    def resultDiffs(self, noun):
        return []