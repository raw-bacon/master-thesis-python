import unittest
from link import Link
from precoxeterpresentation import PreCoxeterPresentation


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.knot = Link([[1, -2, 3, -4, 5, -1, 2, -3, 6, -7, 8, -5, 4, -6, 7, -8]])
        self.hopfLink = Link([[1, -2], [-1, 2]])
        self.weirdLink = Link([[1, 2, 3, -8, -2, 4, -6, -7], [-1, 5, 6, 8, -3, -4, -5, 7]])
        self.pretzel = Link([[-1, 2, 12, -11, 10, -9, 8, -7, 6, -3, 4, -5, -2, 1, 3, -4, 5, -12,
                              11, -10, 9, -8, 7, -6]])
        self.stupidLink = Link([[-1, 1, 2, -2, -3, 3, 4, -4]])
        self.trivialKnot = Link([[]])
        self.trivialLink = Link([[], []])
        self.trivialLink3 = Link([[], [], []])

    def test_arcs(self):
        self.assertEqual(self.knot.arcs, [[-8, 1, -2], [-7, 8, -5], [-6, 7, -8], [-5, 4, -6], [-4, 5, -1],
                                          [-3, 6, -7], [-2, 3, -4], [-1, 2, -3]])
        self.assertEqual(self.hopfLink.arcs, [[-2, 1, -2], [-1, 2, -1]])
        self.assertTrue([-6, -1] in self.pretzel.arcs)
        self.assertEqual([[-4, -1], [-3, 3, 4, -4], [-2, -3], [-1, 1, 2, -2]], self.stupidLink.arcs)
        self.assertEqual([[]], self.trivialKnot.arcs)
        self.assertEqual([[], []], self.trivialLink.arcs)

    def test_names_of_arcs(self):
        self.assertEqual(Link.names_of_arcs(self.knot.arcs), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

    def test_index_of(self):
        self.assertEqual(self.knot.index_of([-5, 4, -6]), 3)

    def test_crossings(self):
        self.assertEqual([[[-8, 1, -2], [-4, 5, -1], [-1, 2, -3]],
                          [[-7, 8, -5], [-8, 1, -2], [-6, 7, -8]],
                          [[-6, 7, -8], [-7, 8, -5], [-3, 6, -7]],
                          [[-5, 4, -6], [-4, 5, -1], [-2, 3, -4]],
                          [[-4, 5, -1], [-7, 8, -5], [-5, 4, -6]],
                          [[-3, 6, -7], [-6, 7, -8], [-5, 4, -6]],
                          [[-2, 3, -4], [-3, 6, -7], [-1, 2, -3]],
                          [[-1, 2, -3], [-8, 1, -2], [-2, 3, -4]]], self.knot.crossings)
        self.assertEqual(self.hopfLink.crossings, [[[-2, 1, -2], [-1, 2, -1], [-1, 2, -1]],
                                                   [[-1, 2, -1], [-2, 1, -2], [-2, 1, -2]]])

    def test_is_obvious_visible_generating_set(self):
        self.assertEqual(self.knot.is_obvious_visible_generating_set([self.knot.arcs[1]]), False)
        self.assertEqual(self.knot.is_obvious_visible_generating_set(self.knot.arcs), True)
        self.assertEqual(self.knot.is_obvious_visible_generating_set(self.knot.arcs[3:]), True)

    def test_wirtinger_rank(self):
        self.assertEqual(3, self.knot.wirtinger_rank())
        self.assertEqual(2, self.hopfLink.wirtinger_rank())
        self.assertEqual(1, self.trivialKnot.wirtinger_rank())
        self.assertEqual(2, self.trivialLink.wirtinger_rank())

    def test_get_all_obvious_visible_generating_sets(self):
        self.assertEqual([[[-2, 1, -2], [-1, 2, -1]]], self.hopfLink.all_obvious_visible_generating_sets())
        self.assertEqual(3, len(self.knot.all_obvious_visible_generating_sets()[2]))
        self.assertEqual([self.trivialLink.arcs], self.trivialLink.all_obvious_visible_generating_sets())

    def test_get_reflection_quotient_with_respect_to_generating_set(self):
        self.assertEqual(PreCoxeterPresentation(['a', 'b'], ["abab"]),
                         self.hopfLink.get_reflection_quotient_with_respect_to_generating_set(self.hopfLink.arcs))
        self.assertEqual(PreCoxeterPresentation(['a', 'b', 'c'], []),
                         self.trivialLink3.get_reflection_quotient_with_respect_to_generating_set(self.
                                                                                                  trivialLink3.arcs))

    def test_determinant(self):
        self.assertEqual(21, self.knot.determinant())

    def test_all_obvious_coxeter_quotients(self):
        from coxetergroup import CoxeterGroup
        self.assertNotEqual([], self.hopfLink.
                            all_obvious_visible_coxeter_quotients_with_respect_to_all_generating_sets())
        self.assertEqual([], self.trivialKnot.
                         all_obvious_visible_coxeter_quotients_with_respect_to_all_generating_sets())
        self.assertEqual([CoxeterGroup([[1, 0], [0, 1]])], self.trivialLink.
                         all_obvious_visible_coxeter_quotients_with_respect_to_all_generating_sets())


if __name__ == '__main__':
    unittest.main()
