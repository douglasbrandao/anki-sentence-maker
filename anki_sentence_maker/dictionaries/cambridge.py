from xml.dom.minidom import Attr

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet, Tag
from requests import Response

from anki_sentence_maker.dictionaries.base import Base
from anki_sentence_maker.headers import headers
from exceptions import IncorrectlyTypedException
from type.data import Data
from utils import str_env, word_separated_by_delimiter


class Cambridge(Base):
    def scrape(self):
        """Scrape the cambridge dictionary"""
        word: str = word_separated_by_delimiter(self._word, "-")
        response: Response = requests.get(
            f"{str_env('CAMBRIDGE_URL')}{word}", headers=headers
        )

        if (
            "Search suggestions for" in response.text
            or "Get clear definitions and audio" in response.text
        ):
            raise IncorrectlyTypedException(f"Was this word [{word}] typed correctly?")

        soup = BeautifulSoup(response.text, "html.parser")

        title_div: PageElement | None = soup.find("div", attrs={"class": "di-title"})
        phon_span: ResultSet[Tag] = soup.select(
            "span.us.dpron-i > span.pron.dpron", limit=1
        )
        definition_div: ResultSet[PageElement] = soup.find_all(
            "div", class_="def ddef_d db"
        )
        examples_div = soup.find_all("div", class_="examp dexamp")
        dataset_div = soup.find("div", attrs={"id": "dataset-example"})

        name: str = title_div.text if title_div else ""

        try:
            phonetic_notation = phon_span[0].text
        except IndexError:
            word_to_list = self._word.split()
            phonetic = self.get_phonetic_notation_from_list(word_to_list)
            phonetic_notation = f"/{phonetic}/"

        definitions: list[str] = [
            s.text.strip().replace(":", "") for s in definition_div
        ]
        examples: list[str] = [s.text for s in examples_div]

        if dataset_div:
            examples: list[str] = [
                s.text.strip() for s in soup.find_all("span", class_="deg")
            ]

        return Data(
            name=name,
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
