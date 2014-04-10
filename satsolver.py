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


class VarSet(object):
    """A Variable Set is the set of variables a problem will use
    """

    def __init__(self):
        self.var_dict = {}

    def add(self, *keys):
        for key in keys:
            self.var_dict[key] = True

    def to_set(self):
        return set(self.var_dict.keys())


class Literal(object):
    """A literal is a specific variable with its sign
    """

    def __init__(self, number, sign):
        self.number = number
        self.sign = sign

    def to_string(self):
        prefix = "" if self.sign == True else "-"
        return "{0}{1}".format(prefix, self.number)


class Clause(object):
    """A clause is a set of up to three Literals
    """

    def __init__(self):
        self.literals = set()

    def add_literals(self, *literals):
        for literal in literals:
            if len(self.literals) >= 3:
                raise TooManyLiterals
            else:
                self.literals.add(literal)

    def _vars(self):
        return [lit.number for lit in self.literals]

    def to_string(self):
        return " ".join(lit.to_string() for lit in sorted(
            self.literals, key=lambda x: x.number
        ))


class Problem(object):
    """Problem is made up of many clauses, and draws from a 
    """

    def __init__(self):
        self.clauses = set()
        self.var_set = VarSet()

    def add_clause(self, clause):
        self.clauses.add(clause)
        self.var_set.add(clause._vars)

    def to_string(self):
        return "\n".join(
            ["p cnf {0} {1}".format(
                len(self.var_set.var_dict), len(self.clauses))] +\
            sorted([c.to_string() for c in self.clauses])
        )
