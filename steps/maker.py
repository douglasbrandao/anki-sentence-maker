import requests
from .utils.reformat_word import reformat_word
from .utils.split_word import split_word
from bs4 import BeautifulSoup


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
            phrasal_verb = split_word(self.word)
            verb = phrasal_verb[0]
            adverb = phrasal_verb[1]
            phonetic = self.find_phonetic(verb, adverb)
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
            phrasal_verb = split_word(self.word)
            verb = phrasal_verb[0]
            adverb = phrasal_verb[1]
            phonetic = self.find_phonetic(verb, adverb)
            ipa = '/{}/'.format(phonetic)

        definitions = [s.text for s in soup.find_all('div', class_='def ddef_d db')]
        examples = [s.text for s in soup.find_all('div', class_='examp dexamp')]

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
    def find_phonetic(word1, word2):
        verb = requests.get('https://www.oxfordlearnersdictionaries.com/us/definition/english/' + word1)
        adverb = requests.get('https://www.oxfordlearnersdictionaries.com/us/definition/english/' + word2)

        soup_verb = BeautifulSoup(verb.text, 'html.parser')
        soup_adverb = BeautifulSoup(adverb.text, 'html.parser')

        verb_ipa = soup_verb.find('span', attrs={'class': 'phon'}).text
        adverb_ipa = soup_adverb.find('span', attrs={'class': 'phon'}).text

        ipa = '{} {}'.format(verb_ipa, adverb_ipa)

        return ''.join(a for a in ipa if a not in '\/')

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
