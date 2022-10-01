from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import NoExamplesFoundException, PhoneticNotationNotFoundException
from utils import int_env, str_env
from utils.word_separated_by_delimiter import word_separated_by_delimiter


class Base(ABC):
    def __init__(self, word):
        self._word = word
        self._min_examples = int_env("MINIMUM_EXAMPLES")
        self._max_examples = int_env("MAXIMUM_EXAMPLES")
        self._max_definitions = int_env("MAX_DEFINITIONS")

    @abstractmethod
    def scrape(self):
        """This method must be overridden"""

    def get_phonetic_notation_from_list(self, words: list[str]):
        """Find a phonetic notation IPA on oxford dictionary"""
        full_phonetic_notation: str = ""
        for word in words:
            response = requests.get(f"{str_env('OXFORD_URL')}{word}", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            try:
                phonetic_notation = soup.find("span", attrs={"class": "phon"}).text
                full_phonetic_notation += f"{phonetic_notation} "
                return "".join(
                    c for c in full_phonetic_notation if c not in "\/"
                ).rstrip()
            except AttributeError:
                raise PhoneticNotationNotFoundException(
                    "Phonetic Notation hasn't been found"
                )

    def find_new_examples(self):
        """
        Go to WordHippo website in order to find new examples to meet the minimum requirements
        """
        word: str = word_separated_by_delimiter(self._word, "_")
        response = requests.get(
            f"{str_env('EXAMPLES_URL')}{word}.html", headers=headers
        )

        if "No examples found." in response.text:
            raise NoExamplesFoundException("No examples were found on WordHippo")

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"id": "mainsentencestable"})
        tr = table.find_all("tr")
        sentences = [s.text.strip("\n") for s in tr]
        return sentences
