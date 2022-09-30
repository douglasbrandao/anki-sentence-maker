import random
from typing import List

from bs4 import BeautifulSoup
from requests import Response, get

from anki_sentence_maker.dictionaries.base import Base
from anki_sentence_maker.headers import headers
from exceptions import NoExamplesFound
from utils import str_env, word_separated_by_delimiter


class Oxford(Base):
    def scrape(self):
        """Scrape the oxford dictionary"""
        word: str = word_separated_by_delimiter(self._word, "-")
        response: Response = get(str_env("OXFORD_URL") + word, headers=headers)

        if "Word not found in the dictionary" in response.text:
            raise ValueError(f"Was this word [{word}] typed correctly?")

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        name: str = soup.find("h1", attrs={"class": "headword"}).text

        try:
            full_phonetic_notation: str = soup.find(
                "span", attrs={"class": "phon"}
            ).text
        except AttributeError:
            word_to_list: List[str] = self._word.split()
            phonetic: str = self.get_phonetic_notation_from_list(word_to_list)
            full_phonetic_notation: str = "/{}/".format(phonetic)

        definitions: List[str] = [
            s.text.strip() for s in soup.find_all("span", class_="def")
        ]
        examples: List[str] = [s.text for s in soup.select("ul.examples > li > span.x")]

        if len(examples) < self._min_examples:
            sentences: List[str] = self.find_new_examples()
            examples.extend(sentences)
            random.shuffle(examples)

        if not examples:
            raise NoExamplesFound(
                f"We could not find a good number of examples of [{word}]. Let me try the next one!"
            )

        print("[WE FOUND IT ON OXFORD!] -> ", end="")
        print(f"We have found [{word}] on Oxford!")

        return {
            "name": name,
            "ipa": full_phonetic_notation,
            "definitions": definitions[: self._max_definitions],
            "examples": examples[: self._max_examples],
        }
