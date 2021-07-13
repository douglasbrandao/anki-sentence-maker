import os
from .utils.word_separated_by_delimiter import word_separated_by_delimiter
from bs4 import BeautifulSoup
from sentence_maker.headers import headers
from requests import get


class Base:

    def __init__(self, word, min_examples, max_examples, max_definitions):
        self._word = word
        self._min_examples = min_examples
        self._max_examples = max_examples
        self._max_definitions = max_definitions

    def scrape(self):
        """This method must be overridden"""
        pass

    @staticmethod
    def get_phonetic_notation_from_list(*args):
        full_phonetic_notation = ''
        words = args[0]
        for word in words:
            response = get(os.environ.get('OXFORD_URL') + word, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                phonetic_notation = soup.find('span', attrs={'class': 'phon'}).text
                full_phonetic_notation += '{} '.format(phonetic_notation)
            except AttributeError as error:
                return error

        return ''.join(c for c in full_phonetic_notation if c not in '\/').rstrip()

    def find_new_examples(self):
        word = word_separated_by_delimiter(self._word, '_')
        response = get(os.environ.get('EXAMPLES_URL') + word + '.html', headers=headers)

        if 'No examples found.' in response.text:
            raise ValueError("We didn't find examples on WordHippo!")

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', attrs={'id': 'mainsentencestable'})
        tr = table.find_all('tr')
        sentences = [s.text.strip('\n') for s in tr]
        return sentences
