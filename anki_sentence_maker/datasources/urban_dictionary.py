import re
from anki_sentence_maker.bases import RestAPIDataSource

import requests
import random

from exceptions import IncorrectlyTypedException, PhoneticNotationNotFoundException
from logger import logger
from type.data import Data
from utils import get_phonetic_notation_from_list, str_env, word_separated_by_delimiter

class UrbanDictionary(RestAPIDataSource):

    def get(self):
        """Fetch examples from Urban Dictionary API"""
        word_separated_by_hyphen: str = word_separated_by_delimiter(self.word, "-")
        response = requests.get(f"{str_env('URBAN_DICTIONARY_URL')}define?term={word_separated_by_hyphen}").json()

        if "list" in response and not response["list"]:
            raise IncorrectlyTypedException(f"Was this word [{word_separated_by_hyphen}] typed correctly?")

        examples: list[str] = []
        definitions: list[str] = []

        for item in response["list"]:
            definition = re.sub("[^a-zA-Z.\\s\\n]", "", item["definition"])
            example = re.sub("[^a-zA-Z.\\s]", "", item["example"])
            example_capitalized = example.capitalize()
            definitions.append(definition)
            examples.append(example_capitalized)
        
        try:
            word_to_list = self.word.split()
            phonetic = get_phonetic_notation_from_list(word_to_list)
            phonetic_notation = f"/{phonetic}/"
        except PhoneticNotationNotFoundException as error:
            logger.error(error)
            phonetic_notation = ""
        

        return Data(
            name=self.word,
            phonetic_notation=phonetic_notation,
            definitions=definitions,
            examples=examples,
        )
    
    def retrieve(self):
        return self.get()
