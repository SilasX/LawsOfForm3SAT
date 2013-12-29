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


class TestLiteral(unittest.TestCase):

    def setUp(self):
        self.literal_obj = satsolver.Literal(3, False)
        self.literal_obj2 = satsolver.Literal(2, True)

    def test_single_literal(self):
        expected = (3, False)
        actual = (self.literal_obj.number, self.literal_obj.setting)
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
            (lit.number, lit.setting) for lit in self.clause_obj.literals
        ])
        self.assertEqual(expected, actual)

    def test_add_several_clauses_at_once(self):
        expected = set([(1, True), (2, True), (3, False)])
        self.clause_obj.add_literals(*self.literals)
        actual = set([
            (lit.number, lit.setting) for lit in self.clause_obj.literals
        ])
        self.assertEqual(expected, actual)

    def test_too_many_literals(self):
        for literal in self.literals:
            self.clause_obj.add_literals(literal)
        with self.assertRaises(satsolver.TooManyLiterals):
            self.clause_obj.add_literals(satsolver.Literal(4, False))

    def test_to_string(self):
        expected = "1 2 -3\n"
        self.clause_obj.add_literals(*self.literals)
        actual = self.clause_obj.to_string()
        self.assertEqual(expected, actual)


#class TestProblem(unittest.TestCase):
#
#    def test_3clause_3vars(self):
#
