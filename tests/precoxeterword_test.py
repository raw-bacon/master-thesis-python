import unittest
from precoxeterpresentation import PreCoxeterPresentation
from precoxeterword import PreCoxeterWord


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.presentation = PreCoxeterPresentation(['a', 'e', 'l', 'o'], [])
        self.presentation2 = PreCoxeterPresentation(['a', 'c', 'd'], [])
        self.word = PreCoxeterWord("hello", self.presentation)
        self.word2 = PreCoxeterWord("cdcaadaacd", self.presentation2)

    def test_rewrite(self):
        word = self.word.remove_squares()
        word2 = self.word2.remove_squares()
        self.assertEqual("heo", word.string)
        self.assertEqual("cdcdcd", word2.string)

    def test_contains_square(self):
        self.assertTrue(self.word.contains_square())
        self.assertFalse(self.word.remove_squares().contains_square())


if __name__ == '__main__':
    unittest.main()
