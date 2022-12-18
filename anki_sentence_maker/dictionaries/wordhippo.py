import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet, Tag

from anki_sentence_maker.bases.scrape import BaseScrape
from anki_sentence_maker.headers import headers
from exceptions import NoExamplesFoundException
from utils import str_env, word_separated_by_delimiter


class WordHippo(BaseScrape):
    def scrape(self) -> list[str]:
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
        main_sentences_rows: ResultSet[Tag] = soup.select("table#mainsentencestable tr")

        sentences = [s.text.strip("\n") for s in main_sentences_rows]
        return sentences
