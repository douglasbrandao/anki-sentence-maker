import random

from anki_sentence_maker.dictionaries import Cambridge, Oxford, WordHippo
from exceptions import (
    IncorrectlyTypedException,
    NoExamplesFoundException,
    PhoneticNotationNotFoundException,
)
from logger import logger
from type.data import Data
from utils import int_env


class Maker:
    def __init__(self, word: str):
        self.__word = word
        self._min_examples = int_env("MINIMUM_EXAMPLES")
        self._max_examples = int_env("MAXIMUM_EXAMPLES")
        self._max_definitions = int_env("MAX_DEFINITIONS")

    def check_if_examples_match_minimum_amount(self, data: Data) -> Data:

        if len(data.examples) < self._min_examples:
            word_hippo = WordHippo(word=data.name)
            sentences: list[str] = word_hippo.scrape()
            data.examples.extend(sentences)
            random.shuffle(data.examples)

        if not data.examples:
            raise NoExamplesFoundException(
                f"We couldn't find a good amount of examples of [{self.__word}]."
            )

        logger.info(f"We have found [{self.__word}]")

        return Data(
            name=data.name,
            phonetic_notation=data.phonetic_notation,
            definitions=data.definitions[: self._max_definitions],
            examples=data.examples[: self._max_examples],
        )

    @property
    def sentence(self) -> Data | None:
        """Try to find the words provided"""

        dictionaries = [Oxford, Cambridge]

        for dictionary in dictionaries:
            try:
                instance = dictionary(self.__word)
                return self.check_if_examples_match_minimum_amount(instance.scrape())
            except NoExamplesFoundException as error:
                logger.error(error)
            except PhoneticNotationNotFoundException as error:
                logger.error(error)
            except IncorrectlyTypedException as error:
                logger.error(error)
