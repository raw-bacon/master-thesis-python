from coxetergroup import CoxeterGroup
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.matrix1 = [[1, 2], [2, 1]]
        self.matrix2 = [[1, 2, 3], [2, 1, 5], [3, 5, 1]]
        self.matrix3 = [[1, 3, 2], [3, 1, 5], [2, 5, 1]]
        self.matrix4 = [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
        self.invalid = [[1, 1], [1, 1]]
        self.invalid2 = [[1, 0], [1, 2]]
        self.weird_gen_group = CoxeterGroup(self.matrix2, gens=['h', 'd', 'f'])
        self.normal_gen_group = CoxeterGroup(self.matrix2)

    def test_gens(self):
        self.assertEqual(['d', 'f', 'h'], self.weird_gen_group.gens)

    def test_rels(self):
        self.assertTrue('hdhd' in self.weird_gen_group.rels)

    def test_is_valid(self):
        self.assertTrue(CoxeterGroup.is_valid(self.matrix1))
        self.assertFalse(CoxeterGroup.is_valid(self.invalid))
        self.assertFalse(CoxeterGroup.is_valid(self.invalid2))

    def test_is_permutation(self):
        self.assertTrue(CoxeterGroup.matrices_are_permutations(self.matrix2, self.matrix3))
        self.assertFalse(CoxeterGroup.matrices_are_permutations(self.matrix2, self.matrix4))

    def test_join(self):
        matrices = [CoxeterGroup([[1, 2], [2, 1]]), CoxeterGroup([[1, 3], [3, 1]])]
        self.assertEqual(CoxeterGroup([[1, 6], [6, 1]]), CoxeterGroup.join(matrices))

    def test_str(self):
        matrix = [[1, 0], [0, 1]]
        group = CoxeterGroup(matrix)
        self.assertEqual('[[1, inf], [inf, 1]]', group.__str__())
        matrix = [[1, 10], [10, 1]]
        group = CoxeterGroup(matrix)
        self.assertEqual('[[1, 10], [10, 1]]', group.__str__())

if __name__ == '__main__':
    unittest.main()
