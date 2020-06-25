import unittest
from .maker import Maker


class MakerTests(unittest.TestCase):

    def test_non_found_word_should_raise_error(self):

        sentence = Maker("hahaha", 2, 3, 4)

        with self.assertRaises(ValueError):
            sentence.scrape_oxford_dictionary()

        with self.assertRaises(ValueError):
            sentence.scrape_cambridge_dictionary()

    def test_find_examples_wordhippo(self):

        sentence = Maker("caralho", 2, 3, 4)

        with self.assertRaises(ValueError):
            sentence.find_new_examples()


if __name__ == "__main__":
    unittest.main()
