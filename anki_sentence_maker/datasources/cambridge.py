from anki_sentence_maker.bases import ScrapeDataSource

import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import IncorrectlyTypedException
from type.data import Data
from utils import get_phonetic_notation_from_list, word_separated_by_delimiter
import os


class Cambridge(ScrapeDataSource):
    def scrape(self):
        """Scrape the cambridge dictionary"""
        word_separated_by_hyphen: str = word_separated_by_delimiter(self.word, "-")
        response = requests.get(
            f"{os.environ.get('CAMBRIDGE_URL')}{word_separated_by_hyphen}",
            headers=headers,
        )

        if (
            "Search suggestions for" in response.text
            or "Get clear definitions and audio" in response.text
        ):
            raise IncorrectlyTypedException(
                f"Was this word [{word_separated_by_hyphen}] typed correctly?"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        title_div = soup.find("div", attrs={"class": "di-title"})
        phon_span = soup.select("span.us.dpron-i > span.pron.dpron", limit=1)
        definition_div = soup.find_all("div", class_="def ddef_d db")
        examples_div = soup.find_all("div", class_="examp dexamp")
        dataset_div = soup.find("div", attrs={"id": "dataset-example"})

        name: str = title_div.text if title_div else ""

        try:
            phonetic_notation = phon_span[0].text
        except IndexError:
            word_to_list = self.word.split()
            phonetic = get_phonetic_notation_from_list(word_to_list)
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

    def retrieve(self):
        return self.scrape()
