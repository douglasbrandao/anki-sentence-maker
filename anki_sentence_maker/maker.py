from anki_sentence_maker.dictionaries import Cambridge, Oxford
from exceptions import (
    IncorrectlyTypedException,
    NoExamplesFoundException,
    PhoneticNotationNotFoundException,
)
from logger import logger


class Maker:
    def __init__(self, word):
        self.__word: str = word

    @property
    def sentence(self):
        """Try to find the words provided"""
        try:
            oxford = Oxford(self.__word)
            response = oxford.scrape()
            return response
        except NoExamplesFoundException as error:
            logger.error(error)
        except PhoneticNotationNotFoundException as error:
            logger.error(error)
        except IncorrectlyTypedException as error:
            logger.error(error)

        try:
            cambridge = Cambridge(self.__word)
            response = cambridge.scrape()
            return response
        except NoExamplesFoundException as error:
            logger.error(error)
        except PhoneticNotationNotFoundException as error:
            logger.error(error)
        except IncorrectlyTypedException as error:
            logger.error(error)
