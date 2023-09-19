from .datasources import (
    Cambridge,
    Oxford,
    WordHippo,
)
from exceptions import (
    IncorrectlyTypedException,
    NoExamplesFoundException,
    PhoneticNotationNotFoundException,
)
from logger import logger
from type import Data

import os
import random

from anki_sentence_maker.bases import DataSource

class Maker:
    def __init__(self, word: str):
        self.__word = word
        self.__min_examples = int(os.getenv('MINIMUM_EXAMPLES', 3))
        self.__max_examples = int(os.getenv('MAXIMUM_EXAMPLES', 5))
        self.__max_definitions = int(os.getenv('MAX_DEFINITIONS', 2))

    def __has_reached_minimum_number_of_examples(self, examples: list[str]) -> bool:
        return len(examples) > self.__min_examples

    def __find_more_examples_on_word_hippo(self, word: str) -> list[str]:
        word_hippo = WordHippo(word=word)
        sentences = word_hippo.retrieve()
        return sentences

    def __get_examples(self, data: Data) -> Data:
        if not self.__has_reached_minimum_number_of_examples(data.examples):
            logger.warning(f"It hasn't reached the minimum number of examples. Wait.")
            sentences = self.__find_more_examples_on_word_hippo(self.__word)
            data.examples.extend(list(set(sentences)))
            return self.__get_examples(data)

        random.shuffle(data.examples)

        if not data.examples:
            raise NoExamplesFoundException(self.__word)

        logger.info(f"[{self.__word}] found!")

        return Data(
            name=data.name,
            phonetic_notation=data.phonetic_notation,
            definitions=data.definitions[:self.__max_definitions],
            examples=data.examples[:self.__max_examples],
        )

    @property
    def sentence(self) -> Data | None:
        """Find examples with the given words"""

        data_sources: list[DataSource] = [Cambridge, Oxford]

        for data_source in data_sources:
            try:
                instance = data_source(word=self.__word)
                data = instance.retrieve()
                return self.__get_examples(data)
            except NoExamplesFoundException as error:
                logger.error(error)
            except PhoneticNotationNotFoundException as error:
                logger.error(error)
            except IncorrectlyTypedException as error:
                logger.error(error)
