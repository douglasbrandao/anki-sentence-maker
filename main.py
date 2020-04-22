from steps.maker import SentenceMaker
import csv
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Look up words in a dictionary')
    parser.add_argument('lookup', type=str, nargs='+')
    args = parser.parse_args()

    words = args.lookup
    words_infos_returned = []

    for word in words:
        s = SentenceMaker(word, 3)
        words_infos_returned.append(s.find_word())

    words_infos_returned = [x for x in words_infos_returned if x is not None]

    with open('sentences.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['sentence', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        if words_infos_returned:
            for info in words_infos_returned:
                for example in info['examples']:
                    writer.writerow({
                        'sentence': example,
                        'information': '{} {}\n'
                                       '({})'.format(info['name'], info['ipa'], ', '.join(info['definitions']))
                    })
            print("File generated...")
        else:
            print("\n")
            print("We didn't reiceve any return with the list of words you gave to us.")
