class TooManyLiterals(Exception):

    def __init__(self):
        self.value = "Cannot add another literal to this clause."

    def __str__(self):
        return repr(self.value)
