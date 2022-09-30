import random
from typing import List
from utils import word_separated_by_delimiter, str_env
from colorama import Fore, Style
from anki_sentence_maker.dictionaries.base import Base, NoExamplesFound
from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from requests import get, Response


class Cambridge(Base):
    def scrape(self):
        """Scrape the cambridge dictionary"""
        word: str = word_separated_by_delimiter(self._word, "-")
        response: Response = get(str_env("CAMBRIDGE_URL") + word, headers=headers)

        if (
            "Search suggestions for" in response.text
            or "Get clear definitions and audio" in response.text
        ):
            raise ValueError(f"Was this word [{word}] typed correctly?")

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        name: str = soup.find("div", attrs={"class": "di-title"}).text

        try:
            full_phonetic_notation = soup.select(
                "span.us.dpron-i > span.pron.dpron", limit=1
            )[0].text
        except IndexError:
            word_to_list = self._word.split()
            phonetic = self.get_phonetic_notation_from_list(word_to_list)
            full_phonetic_notation = "/{}/".format(phonetic)

        definitions: List[str] = [
            s.text.strip().replace(":", "")
            for s in soup.find_all("div", class_="def ddef_d db")
        ]
        examples: List[str] = [
            s.text for s in soup.find_all("div", class_="examp dexamp")
        ]

        dataset_examples = soup.find("div", attrs={"id": "dataset-example"})

        if dataset_examples:
            examples: List[str] = [
                s.text.strip() for s in soup.find_all("span", class_="deg")
            ]

        if len(examples) < self._min_examples:
            sentences: List[str] = self.find_new_examples()
            examples.extend(sentences)
            random.shuffle(examples)

        if not examples:
            raise NoExamplesFound(
                f"It wasn't possible to find a good amount of examples of [{word}]."
            )

        print(
            Fore.GREEN
            + Style.BRIGHT
            + "[WE FOUND IT ON CAMBRIDGE!] -> "
            + Style.RESET_ALL,
            end="",
        )
        print(f"We have found [{word}] on Cambridge!")

        return {
            "name": name,
            "ipa": full_phonetic_notation,
            "definitions": definitions[: self._max_definitions],
            "examples": examples[: self._max_examples],
        }
