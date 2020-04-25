import requests
from bs4 import BeautifulSoup
from .utils.reformat_word import reformat_word


class SentenceMaker:

    def __init__(self, word, max_def, minimum, maximum):
        self.word = word
        self.min_examples = minimum
        self.max_def = max_def
        self.max_examples = maximum

    def scrap_oxford(self):
        word = reformat_word(self.word)
        url = requests.get('https://www.oxfordlearnersdictionaries.com/us/definition/english/' + word)

        if 'Word not found in the dictionary' in url.text:
            raise ValueError(f"This word {word} was typed correctly? We can't find it on Oxford.")

        soup = BeautifulSoup(url.text, 'html.parser')
        name = soup.find('h1', attrs={'class': 'headword'}).text

        try:
            ipa = soup.find('span', attrs={'class': 'phon'}).text
        except AttributeError:
            word_to_list = self.word.split()
            phonetic = self.find_phonetic(word_to_list)
            ipa = '/{}/'.format(phonetic)

        definitions = [s.text for s in soup.find_all('span', class_='def')]
        examples = [s.text for s in soup.select('ul.examples > li > span.x')]

        if not examples:
            raise IndexError("We haven't found a list of examples on Oxford. I'll try the next one.")

        print(f'We have found {word} on Oxford!')

        return {
            'name': name,
            'ipa': ipa,
            'definitions': definitions[:self.max_def],
            'examples': examples[0:self.max_examples]
        }

    def scrap_cambridge(self):
        word = reformat_word(self.word)
        url = requests.get('https://dictionary.cambridge.org/dictionary/english/' + word)

        soup = BeautifulSoup(url.text, 'html.parser')
        name = soup.find('div', attrs={'class': 'di-title'}).text

        if 'Search suggestions for' in url.text or 'Get clear definitions and audio' in url.text:
            raise ValueError(f"This word {word} was typed correctly? We can't find it on Cambridge.")

        try:
            ipa = soup.select('span.us.dpron-i > span.pron.dpron', limit=1)[0].text
        except IndexError:
            word_to_list = self.word.split()
            phonetic = self.find_phonetic(word_to_list)
            ipa = '/{}/'.format(phonetic)

        definitions = [s.text for s in soup.find_all('div', class_='def ddef_d db')]
        examples = [s.text for s in soup.find_all('div', class_='examp dexamp')]

        dataset_examples = soup.find('div', attrs={'id': 'dataset-example'})

        if dataset_examples is not None:
            examples = [s.text.strip() for s in soup.find_all('span', class_='deg')]

        if not examples:
            raise IndexError("We haven't found a list of examples on Cambridge. I'll try the next one.")

        print(f'We have found {word} on Cambridge!')

        return {
            'name': name,
            'ipa': ipa,
            'definitions': definitions[:self.max_def],
            'examples': examples[0:self.max_examples]
        }

    @staticmethod
    def find_phonetic(*args):

        ipa, words = '', args[0]

        for word in words:
            html = requests.get('https://www.oxfordlearnersdictionaries.com/us/definition/english/' + word)
            soup = BeautifulSoup(html.text, 'html.parser')
            phonetic = soup.find('span', attrs={'class': 'phon'}).text
            ipa += '{} '.format(phonetic)

        return ''.join(a for a in ipa if a not in '\/').rstrip()

    def find_word(self):

        try:
            word_info = self.scrap_oxford()
            return word_info
        except IndexError as error:
            print(error)
        except ValueError as error:
            print(error)

        try:
            word_info = self.scrap_cambridge()
            return word_info
        except IndexError as error:
            print(error)
        except ValueError as error:
            print(error)
