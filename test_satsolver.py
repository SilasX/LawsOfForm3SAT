import unittest
from os.path import dirname, join

import satsolver

THIS_DIR = dirname(__file__)
FILE_DIR = join(THIS_DIR, "test_files")


class TestParse(unittest.TestCase):

    def test_blank(self):
        expected = set()
        with open(join(FILE_DIR, "blank.txt"), "r") as f:
            sat_prob = satsolver.from_file(f)
            actual = sat_prob.clauses
        self.assertEqual(expected, actual)

    def test_comments(self):
        expected = set()
        with open(join(FILE_DIR, "comments.txt"), "r") as f:
            sat_prob = satsolver.from_file(f)
            actual = sat_prob.clauses
        self.assertEqual(expected, actual)


class TestVarSet(unittest.TestCase):

    def test_single_var(self):
        expected = set([2])
        var_set = satsolver.VarSet()
        var_set.add(2)
        actual = var_set.to_set()
        self.assertEqual(expected, actual)

    def test_single_var(self):
        expected = set([1, 2, 3])
        var_set = satsolver.VarSet()
        var_set.add(*range(1,4))
        actual = var_set.to_set()
        self.assertEqual(expected, actual)


class TestLiteral(unittest.TestCase):

    def setUp(self):
        self.literal_obj = satsolver.Literal(3, False)
        self.literal_obj2 = satsolver.Literal(2, True)

    def test_single_literal(self):
        expected = (3, False)
        actual = (self.literal_obj.number, self.literal_obj.sign)
        self.assertEqual(expected, actual)

    def test_check_literal_true_non_match(self):
        expected = False
        sol_dict = {3: True}
        actual = self.literal_obj.is_valid(sol_dict)
        self.assertEqual(expected, actual)

    def test_check_literal_false_match(self):
        expected = True
        sol_dict = {3: False}
        actual = self.literal_obj.is_valid(sol_dict)
        self.assertEqual(expected, actual)

    def test_check_literal_unmatched(self):
        expected = False
        sol_dict = {5: True}
        actual = self.literal_obj2.is_valid(sol_dict)
        self.assertEqual(expected, actual)

    def test_to_string(self):
        expected1, expected2 = "-3", "2"
        actual1 =  self.literal_obj.to_string()
        actual2 =  self.literal_obj2.to_string()
        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)


class TestClause(unittest.TestCase):

    def setUp(self):
        self.literals = (
            satsolver.Literal(3, False),
            satsolver.Literal(2, True),
            satsolver.Literal(1, True),
        )
        self.clause_obj = satsolver.Clause()

    def test_single_clause(self):
        expected = set([(1, True), (2, True), (3, False)])
        for literal in self.literals:
            self.clause_obj.add_literals(literal)
        actual = set([
            (lit.number, lit.sign) for lit in self.clause_obj.literals
        ])
        self.assertEqual(expected, actual)

    def test_add_several_clauses_at_once(self):
        expected = set([(1, True), (2, True), (3, False)])
        self.clause_obj.add_literals(*self.literals)
        actual = set([
            (lit.number, lit.sign) for lit in self.clause_obj.literals
        ])
        self.assertEqual(expected, actual)

    def test_too_many_literals(self):
        for literal in self.literals:
            self.clause_obj.add_literals(literal)
        with self.assertRaises(satsolver.TooManyLiterals):
            self.clause_obj.add_literals(satsolver.Literal(4, False))

    def test_clause_setting_false(self):
        expected = False
        sol_dict = {3: True, 2: False, 1: False}
        self.clause_obj.add_literals(*self.literals)
        actual = self.clause_obj.is_valid(sol_dict)
        self.assertEqual(expected, actual)

    def test_clause_setting_true(self):
        expected = True
        sol_dict = {3: True, 2: False, 1: True}
        self.clause_obj.add_literals(*self.literals)
        actual = self.clause_obj.is_valid(sol_dict)
        self.assertEqual(expected, actual)

    def test_to_string(self):
        expected = "1 2 -3"
        self.clause_obj.add_literals(*self.literals)
        actual = self.clause_obj.to_string()
        self.assertEqual(expected, actual)


class TestProblem(unittest.TestCase):

    def setUp(self):
        """
        set up problem:
        (x1 + x2 + ~x3)(x2 + x3 + ~x4)(~x1 + x3 + ~x4)(x1 + ~x2 + x4)
        """
        self.problem = satsolver.Problem()
        variables = [[1, 2, 3],
                     [2, 3, 4],
                     [1, 3, 4],
                     [1, 2, 4],]
        signs = [[True, True, False],
                    [True, True, False],
                    [False, True, False],
                    [True, False, True],]
        for i in xrange(len(variables)):
            literals = [satsolver.Literal(variables[i][j], signs[i][j]) for j in xrange(len(variables[0]))]
            clause = satsolver.Clause()
            clause.add_literals(*literals)
            self.problem.add_clause(clause)

    def test_4clause_4vars(self):
        lits = (
            satsolver.Literal(2, True),
            satsolver.Literal(3, True),
            satsolver.Literal(4, False),
        )
        clause = satsolver.Clause()
        clause.add_literals(*lits)
        self.assertIn(clause.to_string(), set(
            [c.to_string() for c in self.problem.clauses]
        ))
        expected = "p cnf 4 4\n" +\
            "\n".join(["-1 3 -4", "1 -2 4", "1 2 -3", "2 3 -4", ])
        actual = self.problem.to_string()
        self.assertEqual(expected, actual)
