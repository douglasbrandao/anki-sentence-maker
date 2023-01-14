import os
import random

from anki_sentence_maker.datasources import (
    Cambridge,
    Oxford,
    WordHippo,
    UrbanDictionary,
)
from exceptions import (
    IncorrectlyTypedException,
    NoExamplesFoundException,
    PhoneticNotationNotFoundException,
)
from logger import logger
from type.data import Data


class Maker:
    def __init__(self, word: str):
        self.__word = word
        self.__min_examples = int(os.environ.get("MINIMUM_EXAMPLES", 3))
        self.__max_examples = int(os.environ.get("MAXIMUM_EXAMPLES", 5))
        self.__max_definitions = int(os.environ.get("MAX_DEFINITIONS", 2))

    def __has_reached_minimum_amount_of_examples(self, examples: list[str]) -> bool:
        return len(examples) > self.__min_examples

    def __find_more_examples_from_word_hippo(self, word: str) -> list[str]:
        word_hippo = WordHippo(word=word)
        sentences: list[str] = word_hippo.retrieve()
        return sentences

    def __get_examples(self, data: Data) -> Data:

        if not self.__has_reached_minimum_amount_of_examples(data.examples):
            logger.warning(f"It hasn't reached the minimum number of examples. Wait...")
            sentences = self.__find_more_examples_from_word_hippo(self.__word)
            data.examples.extend(list(set(sentences)))
            return self.__get_examples(data)

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

        data_sources = [Cambridge, Oxford, UrbanDictionary]

        for data_source in data_sources:
            try:
                instance = data_source(word=self.__word)
                return self.__get_examples(instance.retrieve())
            except NoExamplesFoundException as error:
                logger.error(error)
            except PhoneticNotationNotFoundException as error:
                logger.error(error)
            except IncorrectlyTypedException as error:
                logger.error(error)
