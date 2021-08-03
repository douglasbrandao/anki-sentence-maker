import os
import sys
from csv import DictWriter
from datetime import date
from colorama import Fore, Style, init
from typing import List
from sentence_maker.maker import Maker
from dotenv import load_dotenv

init()
load_dotenv()

if __name__ == '__main__':

    ''' First parameter from args is the name of the script'''
    words_from_args: List[str] = sys.argv[1:]
    list_of_sentences: list = []

    external_data = {
        'word': '',
        'max_definitions': os.environ.get('MAX_DEFINITIONS'),
        'min_examples': os.environ.get('MINIMUM_EXAMPLES'),
        'max_examples': os.environ.get('MAXIMUM_EXAMPLES')
    }

    for word in words_from_args:
        external_data['word'] = word
        sentence = Maker(**external_data)
        list_of_sentences.append(sentence.get())

    list_of_sentences: List[dict] = [s for s in list_of_sentences if s]

    brazil_date_notation: str = date.today().strftime('%d-%m-%y')
    csv_filename: str = f"sentences-{brazil_date_notation}.csv"

    with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as file:
        fieldnames: List[str] = ['sentence', 'information']
        writer: DictWriter = DictWriter(file, fieldnames=fieldnames)

        if list_of_sentences:
            for sentence in list_of_sentences:
                for example in sentence['examples']:
                    name: str = sentence['name']
                    ipa: str = sentence['ipa']
                    definitions: str = ', '.join(sentence['definitions'])
                    writer.writerow({
                        'sentence': example,
                        'information': '{} {}\n({})'.format(name, ipa, definitions)
                    })
            print(Fore.WHITE + Style.BRIGHT + f"[{csv_filename}] file was generated!" + Style.RESET_ALL)
        else:
            print("\n")
            print("We didn't receive any return with the list of words you have provided")
