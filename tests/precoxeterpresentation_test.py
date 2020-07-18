import unittest
from precoxeterpresentation import PreCoxeterPresentation


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.presentation = PreCoxeterPresentation(['a', 'b'], ["abab"])
        self.presentation2 = PreCoxeterPresentation(['a', 'b', 'c', 'd'], ["abc", "bc"])

    def test_has_coxeter_quotient_with_matrix(self):
        self.assertTrue(self.presentation.has_coxeter_quotient_with_matrix([[1, 2], [2, 1]]))

    def test_all_primes_less_than(self):
        self.assertEqual([2, 3, 5], PreCoxeterPresentation.all_primes_less_than(5))
        self.assertEqual([2, 3], PreCoxeterPresentation.all_primes_less_than(4))

    def test_prime_coxeter_matrices_of_max_entry(self):
        self.assertEqual([[[1, 2], [2, 1]]],
                         PreCoxeterPresentation.prime_coxeter_matrices_of_max_entry(2, 2))
        self.assertEqual(3 ** 6,
                         len(PreCoxeterPresentation.prime_coxeter_matrices_of_max_entry(5, 4)))

    def test_all_coxeter_quotients(self):
        from coxetergroup import CoxeterGroup
        self.assertEqual([CoxeterGroup([[1, 2], [2, 1]])],
                         list(self.presentation.all_obvious_visible_coxeter_quotients()))

    def test_identify_generators(self):
        new_presentation = self.presentation2.identify_generators(['b', 'c'])
        self.assertTrue("a" in new_presentation.rels)
        self.assertFalse('' in new_presentation.rels)


if __name__ == '__main__':
    unittest.main()
