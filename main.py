import csv
import sys
from datetime import date
from colorama import Fore, Style, init
from sentence_maker.maker import Maker
from constants import MAX_DEFINITIONS, MAXIMUM_EXAMPLES, MINIMUM_EXAMPLES
init()

if __name__ == '__main__':

    ''' First parameter from args is the name of the script'''
    words_from_args = sys.argv[1:]
    list_of_sentences = []

    for word in words_from_args:
        sentence = Maker(word, MAX_DEFINITIONS, MINIMUM_EXAMPLES, MAXIMUM_EXAMPLES)
        examples = sentence.grab_examples()
        list_of_sentences.append(examples)

    list_of_sentences = [x for x in list_of_sentences if x is not None]

    brazil_date_notation = date.today().strftime('%d-%m-%y')
    csv_filename = f"sentences-{brazil_date_notation}.csv"

    with open(csv_filename, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['sentence', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if list_of_sentences:
            for sentence in list_of_sentences:
                for example in sentence['examples']:
                    name = sentence['name']
                    ipa = sentence['ipa']
                    definitions = ', '.join(sentence['definitions'])
                    writer.writerow({
                        'sentence': example,
                        'information': '{} {}\n({})'.format(name, ipa, definitions)
                    })
            print(Fore.WHITE + Style.BRIGHT + f"[{csv_filename}] file was generated!" + Style.RESET_ALL)
        else:
            print("\n")
            print("We didn't receive any return with the list of words you gave to us.")
