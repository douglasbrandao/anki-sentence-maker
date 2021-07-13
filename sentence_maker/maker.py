from sentence_maker.dictionaries import Oxford, Cambridge
from colorama import Fore, Style, init
from pydantic import BaseModel

init()


class Maker(BaseModel):

    word: str
    max_definitions: int
    min_examples: int
    max_examples: int

    def grab_examples(self):
        try:
            oxford = Oxford(self.word, self.min_examples, self.max_examples, self.max_definitions)
            response = oxford.scrape()
            return response
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except ValueError as error:
            print(Fore.RED + Style.BRIGHT + "[WE HAVEN'T FOUND IT ON OXFORD] -> " + Style.RESET_ALL, end='')
            print(error)

        try:
            oxford = Cambridge(self.word, self.min_examples, self.max_examples, self.max_definitions)
            response = oxford.scrape()
            return response
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except ValueError as error:
            print(Fore.RED + Style.BRIGHT + "[WE HAVEN'T FOUND IT ON CAMBRIDGE] -> " + Style.RESET_ALL, end='')
            print(error)
