from anki_sentence_maker.bases import ScrapeDataSource
from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from exceptions import NoExamplesFoundException
from utils import get_word_separated_by_delimiter

import os
import requests

class WordHippo(ScrapeDataSource):
    def scrape(self):
        '''Go to WordHippo website in order to find new examples to meet the minimum requirements'''
        word_separated_by_underscore = get_word_separated_by_delimiter(self.word, '_')
        response = requests.get(
            f'{os.getenv("EXAMPLES_URL")}{word_separated_by_underscore}.html',
            headers=headers,
        )

        if "No examples found." in response.text:
            raise NoExamplesFoundException(word_separated_by_underscore)

        soup = BeautifulSoup(response.text, 'html.parser')
        sentences = [s.text.strip('\n').capitalize() for s in soup.select('table#mainsentencestable tr')]
        return sentences

    def retrieve(self):
        return self.scrape()
