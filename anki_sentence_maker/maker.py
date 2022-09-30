from utils import int_env
from anki_sentence_maker.dictionaries import Oxford, Cambridge
from colorama import Fore, Style, init

init()


class Maker:

    def __init__(self, word):
        self.__word: str = word
        self.__max_definitions: int = int_env('MAX_DEFINITIONS')
        self.__min_examples: int = int_env('MINIMUM_EXAMPLES')
        self.__max_examples: int = int_env('MAXIMUM_EXAMPLES')

    def get(self):
        """Try to find the words provided"""
        try:
            oxford = Oxford(self.__word, self.__min_examples, self.__max_examples, self.__max_definitions)
            response = oxford.scrape()
            return response
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except (ValueError, AttributeError) as error:
            print(Fore.RED + Style.BRIGHT + "[WE DIDN'T FIND IT ON OXFORD] -> " + Style.RESET_ALL, end='')
            print(error)

        try:
            oxford = Cambridge(self.__word, self.__min_examples, self.__max_examples, self.__max_definitions)
            response = oxford.scrape()
            return response
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except (ValueError, AttributeError) as error:
            print(Fore.RED + Style.BRIGHT + "[WE DIDN'T FIND IT ON CAMBRIDGE] -> " + Style.RESET_ALL, end='')
            print(error)
