def from_file(fd):
    output = Problem()
    for line in fd:
        if len(line) == 0 or line[0] == 'c':
            continue
    return output


class TooManyLiterals(Exception):

    def __init__(self):
        self.value = "Cannot add another literal to this clause."

    def __str__(self):
        return repr(self.value)


class Problem(object):

    def __init__(self):
        self.clauses = set()

    def add_clause(self, clause):
        self.clauses.add_clause(clause)


class VarSet(object):

    def __init__(self):
        self.var_dict = {}

    def add(self, *keys):
        for key in keys:
            self.var_dict[key] = True

    def to_set(self):
        return set(self.var_dict.keys())


class Literal(object):

    def __init__(self, number, setting):
        self.number = number
        self.setting = setting

    def to_string(self):
        prefix = "" if self.setting == True else "-"
        return "{0}{1}".format(prefix, self.number)

class Clause(object):

    def __init__(self):
        self.literals = set()

    def add_literals(self, *literals):
        for literal in literals:
            if len(self.literals) >= 3:
                raise TooManyLiterals
            else:
                self.literals.add(literal)

    def to_string(self):
        return "{}\n".format(" ".join(
            lit.to_string() for lit in sorted(
                self.literals, key=lambda x: x.number
            )
        ))
