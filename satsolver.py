from itertools import product

import sat_errs as err


def from_file(fd):
    output = Problem()
    for line in fd:
        if len(line) == 0 or line[0] == 'c':
            continue
    return output


class VarSet(object):
    """A Variable Set is the set of variables a problem will use
    """

    def __init__(self):
        self._set = set()

    def add(self, keys):
        self._set = self._set | set(keys)

    def size(self):
        return len(self._set)

    def all_solutions(self):
        """Returns a generator of every possible solution
        """
        var_list = list(self._set)
        return ({var_list[i]: bln for i, bln in enumerate(sol)} 
            for sol in product([False, True], repeat=self.size()))


class Literal(object):
    """A literal is a specific variable with its sign
    """

    def __init__(self, number, sign):
        self.number = number
        self.sign = sign

    def is_valid(self, sol_dict):
        """given a solution dictionary, mapping numbers to booleans, return whether that setting matches this boolean; return false if sol_dict doesn't set it
        """
        if self.number not in sol_dict:
            return False
        return sol_dict[self.number] == self.sign

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
                raise err.TooManyLiterals
            else:
                self.literals.add(literal)

    def is_valid(self, sol_dict):
        """given a solution dictionary, mapping numbers to booleans, return whether that setting makes the clause true
        """
        return any(literal.is_valid(sol_dict) for literal in self.literals)

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
        self.var_set.add(clause._vars())

    def is_valid(self, sol_dict):
        """given a solution dictionary, mapping numbers to booleans, return whether that setting makes the clause true
        """
        return all(clause.is_valid(sol_dict) for clause in self.clauses)

    def brute_solve(self):
        """returns list of all valid solutions, as found by brute force
        """
        return [sol for sol in self.var_set.all_solutions() if self.is_valid(sol)]

    def to_string(self):
        return "\n".join(
            ["p cnf {0} {1}".format(
                self.var_set.size(), len(self.clauses))] +\
            sorted([c.to_string() for c in self.clauses])
        )
