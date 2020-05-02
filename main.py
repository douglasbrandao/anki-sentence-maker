import csv
from datetime import date
from colorama import Fore, Style, init
from steps.maker import SentenceMaker
init()

if __name__ == '__main__':

    words_typed = input('Which words do you want to look up on the dictionaries?\n')
    words = words_typed.strip().split(',')
    words_infos_returned = []

    # SentenceMaker(word, maximum_definitions, minimum_examples, maximum_examples)
    for word in words:
        s = SentenceMaker(word, 2, 3, 10)
        words_infos_returned.append(s.find_word())

    words_infos_returned = [x for x in words_infos_returned if x is not None]

    brazil_date_format = date.today().strftime('%d-%m-%y')
    csv_name = f"sentences-{brazil_date_format}.csv"

    with open(csv_name, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['sentence', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if words_infos_returned:
            for info in words_infos_returned:
                for example in info['examples']:
                    writer.writerow({
                        'sentence': example,
                        'information': '{} {}\n'
                                       '({})'.format(info['name'], info['ipa'], ', '.join(info['definitions']))
                    })
            print(Fore.WHITE + Style.BRIGHT + f"[{csv_name}] file was generated!" + Style.RESET_ALL)
        else:
            print("\n")
            print("We didn't reiceve any return with the list of words you gave to us.")
