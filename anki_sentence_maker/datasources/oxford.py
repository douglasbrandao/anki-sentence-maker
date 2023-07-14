from anki_sentence_maker.bases import ScrapeDataSource
from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from exceptions import IncorrectlyTypedException
from type import Data
from utils import get_phonetic_notation_from_list, get_word_separated_by_delimiter

import os
import requests

class Oxford(ScrapeDataSource):
    def scrape(self):
        '''Scrape the oxford dictionary'''
        word_separated_by_hyphen = get_word_separated_by_delimiter(self.word, '-')

        response = requests.get(
            f'{os.getenv("OXFORD_URL")}{word_separated_by_hyphen}',
            headers=headers
        )

        if 'Word not found in the dictionary' in response.text:
            raise IncorrectlyTypedException(Oxford.get_classname(), word_separated_by_hyphen)

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1', attrs={'class': 'headword'})
        phonetic_notation = soup.find('span', attrs={'class': 'phon'})
        definitions = soup.find_all('span', class_='def')
        examples = soup.select('ul.examples > li > span.x')

        name = title.text if title else ''
        phonetic_notation = phonetic_notation.text if phonetic_notation else ''

        if not phonetic_notation:
            word_to_list = self.word.split()
            phonetic_notation = get_phonetic_notation_from_list(word_to_list)

        definitions= [s.text.strip() for s in definitions]
        examples = [s.text for s in examples]

        return Data(
            name=name,
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )

    def retrieve(self):
        return self.scrape()
