from anki_sentence_maker.headers import headers
from bs4 import BeautifulSoup
from exceptions import PhoneticNotationNotFoundException

import re
import requests


def get_phonetic_notation_from_list(words: list[str]) -> str:
    """Find a phonetic notation IPA on oxford dictionary"""
    phonetic_notation = ''

    for word in words:
        response = requests.get(f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        phon = soup.find('span', attrs={'class': 'phon'})

        if not phon:
            raise PhoneticNotationNotFoundException(word)

        phonetic_notation += f'{phon.get_text()} '

    phonetic_notation = re.sub('[\\/]', '', phonetic_notation).strip()
    return f'/{phonetic_notation}/'
