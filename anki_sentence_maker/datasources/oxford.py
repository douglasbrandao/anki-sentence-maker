from anki_sentence_maker.bases import ScrapeDataSource
from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from exceptions import IncorrectlyTypedException
from type import Data
from utils import (
    get_phonetic_notation_from_list,
    get_word_separated_by_delimiter
)

import requests

url = 'https://www.oxfordlearnersdictionaries.com/us/definition/english/'


class Oxford(ScrapeDataSource):
    def scrape(self):
        """Scrape the oxford dictionary"""
        word_in_kebab_case = get_word_separated_by_delimiter(self.word, '-')
        response = requests.get(
            url + word_in_kebab_case,
            headers=headers
        )

        if "Definition of" not in response.text:
            raise IncorrectlyTypedException(
                Oxford.get_classname(),
                word_in_kebab_case
            )

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1', attrs={'class': 'headword'})
        phonetic_notation = soup.find('span', attrs={'class': 'phon'})
        definitions = soup.find_all('span', class_='def')
        examples = soup.select('ul.examples > li > span.x')

        phonetic_notation = phonetic_notation.text if phonetic_notation else ''

        if not phonetic_notation:
            word_to_list = self.word.split()
            phonetic_notation = get_phonetic_notation_from_list(word_to_list)

        definitions = [d.text.strip() for d in definitions]
        examples = [e.text.strip().capitalize() for e in examples]

        return Data(
            name=title.text if title else '',
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
