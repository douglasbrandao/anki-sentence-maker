import requests
from bs4 import BeautifulSoup
from requests import Response

from anki_sentence_maker.dictionaries.base import Base
from anki_sentence_maker.headers import headers
from exceptions import IncorrectlyTypedException, PhoneticNotationNotFoundException
from type.data import Data
from utils import str_env, word_separated_by_delimiter


class Oxford(Base):
    def scrape(self):
        """Scrape the oxford dictionary"""
        word: str = word_separated_by_delimiter(self._word, "-")
        response: Response = requests.get(
            f"{str_env('OXFORD_URL')}{word}", headers=headers
        )

        if "Word not found in the dictionary" in response.text:
            raise IncorrectlyTypedException(f"Was this word [{word}] typed correctly?")

        soup = BeautifulSoup(response.text, "html.parser")
        name: str = soup.find("h1", attrs={"class": "headword"}).text

        full_phonetic_notation: str | None = soup.find("span", attrs={"class": "phon"})

        if not full_phonetic_notation:
            raise PhoneticNotationNotFoundException(
                "Phonetic notation hasn't been found"
            )

        word_to_list: list[str] = self._word.split()
        phonetic: str = self.get_phonetic_notation_from_list(word_to_list)
        full_phonetic_notation: str = f"/{phonetic}/"

        definitions: list[str] = [
            s.text.strip() for s in soup.find_all("span", class_="def")
        ]
        examples: list[str] = [s.text for s in soup.select("ul.examples > li > span.x")]

        return Data(
            name=name,
            phonetic_notation=full_phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
