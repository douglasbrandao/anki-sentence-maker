import csv
from datetime import date
from colorama import Fore, Style, init
from sentence_maker.maker import SentenceMaker
init()

if __name__ == '__main__':

    words_typed_from_user = input('Which words do you want to look up on the dictionaries?\n')
    words_typed_to_list = words_typed_from_user.strip().split(',')
    list_of_sentences = []

    for word in words_typed_to_list:
        sentence = SentenceMaker(word, 2, 3, 10).grab_information_from_dictionary()
        list_of_sentences.append(sentence)

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
            print("We didn't reiceve any return with the list of words you gave to us.")