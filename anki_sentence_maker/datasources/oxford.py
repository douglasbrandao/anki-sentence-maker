from anki_sentence_maker.bases import ScrapeDataSource
import os
import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import IncorrectlyTypedException
from type.data import Data
from utils import get_phonetic_notation_from_list, word_separated_by_delimiter


class Oxford(ScrapeDataSource):
    def scrape(self):
        """Scrape the oxford dictionary"""

        word_separated_by_hyphen: str = word_separated_by_delimiter(self.word, "-")
        response = requests.get(
            f"{os.environ.get('OXFORD_URL')}{word_separated_by_hyphen}", headers=headers
        )

        if "Word not found in the dictionary" in response.text:
            raise IncorrectlyTypedException(
                f"Was this word [{word_separated_by_hyphen}] typed correctly?"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        title_h1 = soup.find("h1", attrs={"class": "headword"})
        phon_span = soup.find("span", attrs={"class": "phon"})
        definitions_span = soup.find_all("span", class_="def")
        examples_li = soup.select("ul.examples > li > span.x")

        name: str = title_h1.text if title_h1 else ""
        phonetic_notation: str = phon_span.text if phon_span else ""

        if not phon_span:
            word_to_list: list[str] = self.word.split()
            phonetic: str | None = get_phonetic_notation_from_list(word_to_list)
            phonetic_notation = f"/{phonetic}/"

        definitions: list[str] = [s.text.strip() for s in definitions_span]
        examples: list[str] = [s.text for s in examples_li]

        return Data(
            name=name,
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )

    def retrieve(self):
        return self.scrape()
