from presentation import Presentation
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.pres1 = Presentation(['a', 'b'], ['abab'])
        self.pres2 = Presentation(['a', 'b'], ['baba'])
        self.pres3 = Presentation(['a', 'b'], ['ababab'])
        self.pres4 = Presentation(['b', 'a'], ['abab'])

    def test_is_permutation_of(self):
        self.assertTrue(self.pres1.is_permutation_of(self.pres2))
        self.assertFalse(self.pres1.is_permutation_of(self.pres3))
        self.assertTrue(self.pres1.is_permutation_of(self.pres4))

    def test_remove_duplicates(self):
        lst = [self.pres1, self.pres2, self.pres3, self.pres4]
        self.assertEqual([self.pres1, self.pres3], Presentation.remove_permutations_from_list(lst))


if __name__ == '__main__':
    unittest.main()
