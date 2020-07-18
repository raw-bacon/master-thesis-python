from pretzellink import PretzelLink
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.pretzel1 = PretzelLink([2, 3, 3])
        self.pretzel2 = PretzelLink([-2, 3, 7])
        self.pretzel3 = PretzelLink([0])
        self.pretzel4 = PretzelLink([0, 0])
        self.pretzel5 = PretzelLink([2, 0, 0])

    def test_gauss_code(self):
        self.assertEqual([[1, -2, 8, -7, 6, -3, 4, -5, 2, -1, 3, -4, 5, -8, 7, -6]], self.pretzel1.gauss_code)
        self.assertEqual([[-1, 2, 12, -11, 10, -9, 8, -7, 6, -3, 4, -5, -2, 1, 3, -4, 5, -12, 11, -10, 9, -8, 7, -6]],
                         self.pretzel2.gauss_code)
        self.assertEqual([[]], self.pretzel3.gauss_code)
        self.assertEqual([[], []], self.pretzel4.gauss_code)
        self.assertEqual([[1, -2], [-1, 2], []], self.pretzel5.gauss_code)


if __name__ == '__main__':
    unittest.main()
