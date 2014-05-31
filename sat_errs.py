class CustomException(Exception):

    def __init__(self):
        self.value = "Custom exception triggered"

    def __str__(self):
        return repr(self.value)


class TooManyLiterals(CustomException):

    def __init__(self):
        self.value = "Cannot add another literal to this clause."


class InvalidLiteralToken(CustomException):

    def __init__(self, token):
        self.value = "Cannot parse token {} as literal.".format(token)
