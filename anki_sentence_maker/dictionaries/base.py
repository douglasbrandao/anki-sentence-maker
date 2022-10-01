from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import PhoneticNotationNotFoundException
from utils import str_env


class Base(ABC):
    def __init__(self, word):
        self._word = word

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
