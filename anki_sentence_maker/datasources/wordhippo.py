from anki_sentence_maker.bases import ScrapeDataSource

import requests
import os
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import NoExamplesFoundException
from utils import word_separated_by_delimiter


class WordHippo(ScrapeDataSource):
    def scrape(self):
        """
        Go to WordHippo website in order to find new examples to meet the minimum requirements
        """
        word_separated_by_underscore: str = word_separated_by_delimiter(self.word, "_")
        response = requests.get(
            f"{os.environ.get('EXAMPLES_URL')}{word_separated_by_underscore}.html",
            headers=headers,
        )

        if "No examples found." in response.text:
            raise NoExamplesFoundException("No examples were found")

        soup = BeautifulSoup(response.text, "html.parser")
        main_sentences_rows = soup.select("table#mainsentencestable tr")

        sentences = [s.text.strip("\n") for s in main_sentences_rows]
        return sentences

    def retrieve(self):
        return self.scrape()
