from anki_sentence_maker.bases import ScrapeDataSource
from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from exceptions import NoExamplesFoundException
from utils import get_word_separated_by_delimiter

import os
import requests

class WordHippo(ScrapeDataSource):
    def scrape(self):
        """Go to WordHippo website to find new examples and meet the minimum requirements"""
        word_in_kebab_case = get_word_separated_by_delimiter(self.word, '_')
        response = requests.get(f'https://www.wordhippo.com/what-is/sentences-with-the-word/{word_in_kebab_case}.html', headers=headers)

        if "No examples found" in response.text:
            raise NoExamplesFoundException(word_in_kebab_case)

        soup = BeautifulSoup(response.text, 'html.parser')

        sentences = [s.text.strip('\n').capitalize() for s in soup.select('table#mainsentencestable tr')]
        return sentences

