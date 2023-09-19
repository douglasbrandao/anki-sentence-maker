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

class Cambridge(ScrapeDataSource):
    def scrape(self):
        """Scrape the cambridge dictionary"""
        word_in_kebab_case: str = get_word_separated_by_delimiter(self.word, '-')
        response = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word_in_kebab_case}', headers=headers)

        if not "Meaning of" in response.text:
            raise IncorrectlyTypedException(Cambridge.get_classname(), word_in_kebab_case)

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find(attrs={'class': 'di-title'})
        phonetic_notation = soup.select('span.pron.dpron', limit=1)
        definitions = soup.find_all('div', class_='def ddef_d db')
        examples = soup.find_all('div', class_='examp dexamp')
        dataset_examples = soup.find('div', attrs={'id': 'dataset-example'})

        try:
            phonetic_notation = phonetic_notation[0].text
        except IndexError:
            word_to_list = self.word.split()
            phonetic_notation = get_phonetic_notation_from_list(word_to_list)

        definitions = [d.text.strip().replace(':', '') for d in definitions]
        examples = [e.text.strip().capitalize() for e in examples]

        if dataset_examples:
            examples.extend([e.text.strip().capitalize() for e in soup.find_all('span', class_='deg')])

        return Data(
            name=title.text if title else '',
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )

