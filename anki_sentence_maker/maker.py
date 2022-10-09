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
        self.__min_examples = int_env("MINIMUM_EXAMPLES")
        self.__max_examples = int_env("MAXIMUM_EXAMPLES")
        self.__max_definitions = int_env("MAX_DEFINITIONS")

    def __has_reached_minimum_amount_of_examples(self, examples: list[str]) -> bool:
        return len(examples) > self.__min_examples

    def __get_examples_from_word_hippo(self, word: str) -> list[str]:
        word_hippo = WordHippo(word=word)
        sentences: list[str] = word_hippo.scrape()
        return sentences

    def __get_data(self, data: Data) -> Data:

        if not self.__has_reached_minimum_amount_of_examples(data.examples):
            logger.warning(f"It hasn't reached the minimum number of examples. Wait...")
            sentences = self.__get_examples_from_word_hippo(self.__word)
            data.examples.extend(list(set(sentences)))
            return self.__get_data(data)

        random.shuffle(data.examples)

        if not data.examples:
            raise NoExamplesFoundException(self.__word)

        logger.info(f"[{self.__word}] found!")

        return Data(
            name=data.name,
            phonetic_notation=data.phonetic_notation,
            definitions=data.definitions[: self.__max_definitions],
            examples=data.examples[: self.__max_examples],
        )

    @property
    def sentence(self) -> Data | None:
        """Try to find the words provided"""

        dictionaries = [Oxford, Cambridge]

        for dictionary in dictionaries:
            try:
                instance = dictionary(self.__word)
                return self.__get_data(instance.scrape())
            except NoExamplesFoundException as error:
                logger.error(error)
            except PhoneticNotationNotFoundException as error:
                logger.error(error)
            except IncorrectlyTypedException as error:
                logger.error(error)
