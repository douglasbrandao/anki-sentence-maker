import requests
from bs4 import BeautifulSoup
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
        name: str = soup.find("div", attrs={"class": "di-title"}).text

        try:
            full_phonetic_notation = soup.select(
                "span.us.dpron-i > span.pron.dpron", limit=1
            )[0].text
        except IndexError:
            word_to_list = self._word.split()
            phonetic = self.get_phonetic_notation_from_list(word_to_list)
            full_phonetic_notation = f"/{phonetic}/"

        definitions: list[str] = [
            s.text.strip().replace(":", "")
            for s in soup.find_all("div", class_="def ddef_d db")
        ]
        examples: list[str] = [
            s.text for s in soup.find_all("div", class_="examp dexamp")
        ]

        dataset_examples = soup.find("div", attrs={"id": "dataset-example"})

        if dataset_examples:
            examples: list[str] = [
                s.text.strip() for s in soup.find_all("span", class_="deg")
            ]

        return Data(
            name=name,
            phonetic_notation=full_phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
