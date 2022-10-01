import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.dictionaries.base import Base
from anki_sentence_maker.headers import headers
from exceptions import NoExamplesFoundException
from utils import str_env, word_separated_by_delimiter


class WordHippo(Base):
    def scrape(self):
        """
        Go to WordHippo website in order to find new examples to meet the minimum requirements
        """
        word: str = word_separated_by_delimiter(self._word, "_")
        response = requests.get(
            f"{str_env('EXAMPLES_URL')}{word}.html", headers=headers
        )

        if "No examples found." in response.text:
            raise NoExamplesFoundException("No examples were found")

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"id": "mainsentencestable"})
        tr = table.find_all("tr")
        sentences = [s.text.strip("\n") for s in tr]
        return sentences
