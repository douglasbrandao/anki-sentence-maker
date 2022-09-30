import requests
from utils.word_separated_by_delimiter import word_separated_by_delimiter
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from anki_sentence_maker.headers import headers
from utils import str_env


class Base(ABC):
    def __init__(self, word, min_examples, max_examples, max_definitions):
        self._word = word
        self._min_examples = min_examples
        self._max_examples = max_examples
        self._max_definitions = max_definitions

    @abstractmethod
    def scrape(self):
        """This method must be overridden"""

    def get_phonetic_notation_from_list(*args):
        """Find a phonetic notation IPA on oxford dictionary"""
        full_phonetic_notation: str = ""
        words = args[0]
        for word in words:
            response = requests.get(str_env("OXFORD_URL") + word, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            try:
                phonetic_notation = soup.find("span", attrs={"class": "phon"}).text
                full_phonetic_notation += f"{phonetic_notation} "
            except AttributeError as error:
                return error

        return "".join(c for c in full_phonetic_notation if c not in "\/").rstrip()

    def find_new_examples(self):
        """
        Go to WordHippo website in order to find new examples to meet the minimum requirements
        """
        word: str = word_separated_by_delimiter(self._word, "_")
        response = requests.get(
            str_env("EXAMPLES_URL") + word + ".html", headers=headers
        )

        if "No examples found." in response.text:
            raise NoExamplesFound("We didn't find examples on WordHippo!")

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"id": "mainsentencestable"})
        tr = table.find_all("tr")
        sentences = [s.text.strip("\n") for s in tr]
        return sentences


class NoExamplesFound(Exception):
    def __init__(self, message="No examples were found on WordHippo"):
        super().__init__(message)
