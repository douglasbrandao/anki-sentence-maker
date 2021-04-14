from requests import get
from .headers import headers
import random
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from .utils.word_separated_by_delimiter import word_separated_by_delimiter

init()


class Maker:

    def __init__(self, word, max_definitions, minimum, maximum):
        self.word = word
        self.max_definitions = max_definitions
        self.min_examples = minimum
        self.max_examples = maximum

    def scrape_oxford_dictionary(self):
        word = word_separated_by_delimiter(self.word, '-')
        response = get(f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word}', headers=headers)

        if 'Word not found in the dictionary' in response.text:
            raise ValueError(f"Was this word [{word}] typed correctly?")

        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', attrs={'class': 'headword'}).text

        try:
            full_phonetic_notation = soup.find('span', attrs={'class': 'phon'}).text
        except AttributeError:
            word_to_list = self.word.split()
            phonetic = self.get_phonetic_notation_from_list(word_to_list)
            full_phonetic_notation = '/{}/'.format(phonetic)

        definitions = [s.text.strip() for s in soup.find_all('span', class_='def')]
        examples = [s.text for s in soup.select('ul.examples > li > span.x')]

        if len(examples) < self.min_examples:
            sentences = self.find_new_examples()
            examples.extend(sentences)
            random.shuffle(examples)

        if not examples:
            raise IndexError(f"We could not find a good number of examples of [{word}]. Let me try the next one!")

        print(Fore.GREEN + Style.BRIGHT + "[WE FOUND IT ON OXFORD!] -> " + Style.RESET_ALL, end='')
        print(f'We have found [{word}] on Oxford!')

        return {
            'name': name,
            'ipa': full_phonetic_notation,
            'definitions': definitions[:self.max_definitions],
            'examples': examples[:self.max_examples]
        }

    def scrape_cambridge_dictionary(self):
        word = word_separated_by_delimiter(self.word, '-')

        response = get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers)

        if 'Search suggestions for' in response.text or 'Get clear definitions and audio' in response.text:
            raise ValueError(f"Was this word [{word}] typed correctly?")

        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('div', attrs={'class': 'di-title'}).text

        try:
            full_phonetic_notation = soup.select('span.us.dpron-i > span.pron.dpron', limit=1)[0].text
        except IndexError:
            word_to_list = self.word.split()
            phonetic = self.get_phonetic_notation_from_list(word_to_list)
            full_phonetic_notation = '/{}/'.format(phonetic)

        definitions = [s.text.strip().replace(':', '') for s in soup.find_all('div', class_='def ddef_d db')]
        examples = [s.text for s in soup.find_all('div', class_='examp dexamp')]

        dataset_examples = soup.find('div', attrs={'id': 'dataset-example'})

        if dataset_examples is not None:
            examples = [s.text.strip() for s in soup.find_all('span', class_='deg')]

        if len(examples) < self.min_examples:
            sentences = self.find_new_examples()
            examples.extend(sentences)
            random.shuffle(examples)

        if not examples:
            raise IndexError(f"We could not find a good number of examples of [{word}]. Let me try the next one!")

        print(Fore.GREEN + Style.BRIGHT + "[WE FOUND IT ON CAMBRIDGE!] -> " + Style.RESET_ALL, end='')
        print(f'We have found [{word}] on Cambridge!')

        return {
            'name': name,
            'ipa': full_phonetic_notation,
            'definitions': definitions[:self.max_definitions],
            'examples': examples[:self.max_examples]
        }

    def find_new_examples(self):
        word = word_separated_by_delimiter(self.word, '_')
        response = get(f'https://www.wordhippo.com/what-is/sentences-with-the-word/{word}.html', headers=headers)

        if 'No examples found.' in response.text:
            raise ValueError("We haven't found examples on WordHippo!")

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', attrs={'id': 'mainsentencestable'})
        tr = table.find_all('tr')

        sentences = [s.text.strip('\n') for s in tr]
        return sentences

    @staticmethod
    def get_phonetic_notation_from_list(*args):

        full_phonetic_notation = ''
        words = args[0]

        for word in words:
            response = get(f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word}', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            phonetic_notation = soup.find('span', attrs={'class': 'phon'}).text
            full_phonetic_notation += '{} '.format(phonetic_notation)

        return ''.join(c for c in full_phonetic_notation if c not in '\/').rstrip()

    def grab_examples(self):

        try:
            word_information = self.scrape_oxford_dictionary()
            return word_information
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except ValueError as error:
            print(Fore.RED + Style.BRIGHT + "[WE HAVEN'T FOUND IT ON OXFORD] -> " + Style.RESET_ALL, end='')
            print(error)

        try:
            word_information = self.scrape_cambridge_dictionary()
            return word_information
        except IndexError as error:
            print(Fore.YELLOW + Style.BRIGHT + "[NOT ENOUGH EXAMPLES] -> " + Style.RESET_ALL, end='')
            print(error)
        except ValueError as error:
            print(Fore.RED + Style.BRIGHT + "[WE HAVEN'T FOUND IT ON CAMBRIDGE] -> " + Style.RESET_ALL, end='')
            print(error)
