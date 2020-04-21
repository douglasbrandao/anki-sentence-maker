import requests
from utils.reformat_word import reformat_word
from bs4 import BeautifulSoup


class SentenceMaker:

    def __init__(self, word):
        self.word = word

    def scrap_oxford(self):
        word = reformat_word(self.word)
        url = requests.get('https://www.oxfordlearnersdictionaries.com/us/definition/english/' + word)
        soup = BeautifulSoup(url.text, 'html.parser')

        name = soup.find('h1').contents[0]

        try:
            ipa = soup.find('span', class_='phon').contents[0]
        except AttributeError as error:
            print("Phonetic transcription haven't found for {}. Error: {}".format(name, error))
            ipa = ''

        definitions = [s.text for s in soup.find_all('span', class_='def')][:2]
        examples = [s.text for s in soup.select('ul.examples > li > span.x')]

        return {
            'name': name,
            'ipa': ipa,
            'definitions': definitions,
            'examples': examples
        }

    def scrap_cambridge(self):
        word = reformat_word(self.word)
        url = requests.get('https://dictionary.cambridge.org/dictionary/english/' + word)
        soup = BeautifulSoup(url.text, 'html.parser')

        name = [s.text for s in soup.select('div.di-title')][0]

        try:
            ipa = [s.text for s in soup.find_all('span', class_='pron dpron')][0]
        except IndexError as error:
            print("Phonetic transcription haven't found for {}. Error: {}".format(name, error))
            ipa = ''

        definitions = [s.text for s in soup.find_all('div', class_='def ddef_d db')][:2]
        examples = [s.text for s in soup.find_all('div', class_='examp dexamp')]

        return {
            'name': name,
            'ipa': ipa,
            'definitions': definitions,
            'examples': examples
        }

    def find_word(self):

        # oxford dictionary
        try:
            oxford = self.scrap_oxford()
            return oxford
        except AttributeError as error:
            print(error)
            print("We haven't found on Oxford Dictionary. I'll try the next one...")

        # cambridge dictionary
        try:
            cambridge = self.scrap_cambridge()
            return cambridge
        except AttributeError:
            print("We haven't found on Cambridge Dictionary. I'll try the next one...")
