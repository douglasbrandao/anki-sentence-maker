from app.steps.maker import SentenceMaker
import csv

if __name__ == '__main__':

    words_from_user = 'run at, fall short'
    words = words_from_user.strip().split(',')

    words_infos_returned = []

    for word in words:
        s = SentenceMaker(word, 6)
        words_infos_returned.append(s.find_word())

    with open('sentences.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['sentence', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for info in words_infos_returned:
            for example in info['examples']:
                writer.writerow({
                    'sentence': example,
                    'information': '{} {}\n'
                                   '({})'.format(info['name'], info['ipa'], ', '.join(info['definitions']))
                })

    print("File generated...")
