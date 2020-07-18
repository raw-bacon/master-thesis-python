from toruslink import TorusLink
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.trefoil = TorusLink(3, 2)

    def test_gauss_code(self):
        self.assertEqual([[1, -2, 3, -1, 2, -3]], self.trefoil.gauss_code)


if __name__ == '__main__':
    unittest.main()
