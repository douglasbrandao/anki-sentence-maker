from anki_sentence_maker.dictionaries import Cambridge, Oxford
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
        except IndexError as error:
            print("[NOT ENOUGH EXAMPLES] -> ", end="")
            print(error)
        except (ValueError, AttributeError) as error:
            print("[WE DIDN'T FIND IT ON OXFORD] -> ", end="")
            print(error)

        try:
            oxford = Cambridge(
                self.__word,
                self.__min_examples,
                self.__max_examples,
                self.__max_definitions,
            )
            response = oxford.scrape()
            return response
        except IndexError as error:
            print("[NOT ENOUGH EXAMPLES] -> ", end="")
        except (ValueError, AttributeError) as error:
            print("[WE DIDN'T FIND IT ON CAMBRIDGE] -> ", end="")
