import unittest
from braid import Braid


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.easy_braid = Braid([1])
        self.trefoil = Braid([1, 1, 1])
        self.hopf_link = Braid([1, 1])
        self.figure8 = Braid([1, -2, 1, -2])
        self.weirdBraid = Braid([1, -2, 1, 2])

    def test_braid_to_gauss_code(self):
        self.assertEqual([[1, -1]], self.easy_braid.gauss_code)
        self.assertEqual([[1, -2, 3, -1, 2, -3]], self.trefoil.gauss_code)
        self.assertEqual([[1, -2], [-1, 2]], self.hopf_link.gauss_code)
        self.assertEqual([[1, -2, 4, -1, 3, -4, 2, -3]], self.figure8.gauss_code)


if __name__ == '__main__':
    unittest.main()
