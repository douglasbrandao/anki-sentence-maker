from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement

from anki_sentence_maker.headers import headers
from exceptions import PhoneticNotationNotFoundException
from utils import str_env


class BaseScrape(ABC):
    def __init__(self, word):
        self._word = word

    @abstractmethod
    def scrape(self):
        """This method must be overridden"""

    def get_phonetic_notation_from_list(self, words: list[str]) -> str | None:
        """Find a phonetic notation IPA on oxford dictionary"""
        full_phonetic_notation: str = ""
        for word in words:
            response = requests.get(f"{str_env('OXFORD_URL')}{word}", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            phon_span_element: PageElement | None = soup.find(
                "span", attrs={"class": "phon"}
            )

            if not phon_span_element:
                raise PhoneticNotationNotFoundException(
                    "Phonetic Notation hasn't been found"
                )

            phonetic_notation: str | None = phon_span_element.text
            full_phonetic_notation += f"{phonetic_notation} " f""
            return "".join(c for c in full_phonetic_notation if c not in "\/").rstrip()
