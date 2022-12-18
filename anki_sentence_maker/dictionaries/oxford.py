import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet, Tag
from requests import Response

from anki_sentence_maker.bases.scrape import BaseScrape
from anki_sentence_maker.headers import headers
from exceptions import IncorrectlyTypedException
from type.data import Data
from utils import str_env, word_separated_by_delimiter


class Oxford(BaseScrape):
    def scrape(self) -> Data:
        """Scrape the oxford dictionary"""
        word: str = word_separated_by_delimiter(self._word, "-")
        response: Response = requests.get(
            f"{str_env('OXFORD_URL')}{word}", headers=headers
        )

        if "Word not found in the dictionary" in response.text:
            raise IncorrectlyTypedException(f"Was this word [{word}] typed correctly?")

        soup = BeautifulSoup(response.text, "html.parser")

        title_h1: PageElement | None = soup.find("h1", attrs={"class": "headword"})
        phon_span = soup.find("span", attrs={"class": "phon"})
        definitions_span: ResultSet[PageElement] = soup.find_all("span", class_="def")
        examples_li: ResultSet[Tag] = soup.select("ul.examples > li > span.x")

        name: str = title_h1.text if title_h1 else ""
        phonetic_notation: str = phon_span.text if phon_span else ""

        if not phon_span:
            word_to_list: list[str] = self._word.split()
            phonetic: str | None = self.get_phonetic_notation_from_list(word_to_list)
            phonetic_notation = f"/{phonetic}/"

        definitions: list[str] = [s.text.strip() for s in definitions_span]
        examples: list[str] = [s.text for s in examples_li]

        return Data(
            name=name,
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
