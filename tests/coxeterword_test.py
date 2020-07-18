import unittest
from coxetergroup import CoxeterGroup
from coxeterword import CoxeterWord


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.presentation1 = CoxeterGroup([[1, 2], [2, 1]])
        self.word1 = CoxeterWord("abab", self.presentation1)
        self.word2 = CoxeterWord("ab", self.presentation1)
        self.word3 = CoxeterWord("", self.presentation1)

        self.presentation2 = CoxeterGroup([[1, 3, 3], [3, 1, 3], [3, 3, 1]])
        self.word4 = CoxeterWord("bababacabababc", self.presentation2)
        self.word5 = CoxeterWord("bb", self.presentation2)

    def test_is_identity(self):
        self.assertTrue(self.word1.is_identity())
        self.assertFalse(self.word2.is_identity())
        self.assertTrue(self.word3.is_identity())
        self.assertTrue(self.word4.is_identity())
        self.assertTrue(self.word5.is_identity())


if __name__ == '__main__':
    unittest.main()
