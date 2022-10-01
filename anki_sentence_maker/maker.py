from anki_sentence_maker.dictionaries import Cambridge, Oxford
from exceptions import (
    IncorrectlyTypedException,
    NoExamplesFoundException,
    PhoneticNotationNotFoundException,
)
from logger import logger
from utils import int_env


class Maker:
    def __init__(self, word):
        self.__word: str = word
        self.__max_definitions: int = int_env("MAX_DEFINITIONS")
        self.__min_examples: int = int_env("MINIMUM_EXAMPLES")
        self.__max_examples: int = int_env("MAXIMUM_EXAMPLES")

    def get(self):
        """Try to find the words provided"""
        try:
            oxford = Oxford(
                self.__word,
                self.__min_examples,
                self.__max_examples,
                self.__max_definitions,
            )
            response = oxford.scrape()
            return response
        except NoExamplesFoundException as error:
            logger.error(error)
        except PhoneticNotationNotFoundException as error:
            logger.error(error)
        except IncorrectlyTypedException as error:
            logger.error(error)

        try:
            cambridge = Cambridge(
                self.__word,
                self.__min_examples,
                self.__max_examples,
                self.__max_definitions,
            )
            response = cambridge.scrape()
            return response
        except NoExamplesFoundException as error:
            logger.error(error)
        except PhoneticNotationNotFoundException as error:
            logger.error(error)
        except IncorrectlyTypedException as error:
            logger.error(error)
