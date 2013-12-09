class Friend():
    class State():
        FRIEND = 0
        PENDING = 1
        BLOCKED = 2
        DELETED = 3
    def __init__(self, name, display, type, can_see_custom_stories):
        self.name = name
        self.display = display
        self.type = type
        self.can_see_custom_stories = can_see_custom_stories
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
