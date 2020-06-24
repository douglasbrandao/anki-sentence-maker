import unittest
from .word_separated_by_delimiter import word_separated_by_delimiter


class TestUtils(unittest.TestCase):

    def test_word_separated_by_delimiter(self):

        word_with_space = "fall short"
        word_without_space = "example"

        self.assertEqual(word_separated_by_delimiter(word_with_space, '-'), "fall-short")
        self.assertNotEqual(word_separated_by_delimiter(word_with_space, '-'), "fallshort")
        self.assertEqual(word_separated_by_delimiter(word_without_space, "-"), "example")
