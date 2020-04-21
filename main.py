from sentenceMaker import SentenceMaker
import csv

if __name__ == '__main__':

    words_from_user = 'fall short,run at,eve,gig,cram'
    words = words_from_user.split(',')

    words_infos_returned = []

    for word in words:
        s = SentenceMaker(word)
        words_infos_returned.append(s.find_word())

    with open('sentences.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['sentence', 'informations']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for info in words_infos_returned:
            for example in info['examples']:
                writer.writerow({
                    'sentence': example,
                    'informations': '{} {}\n'
                                    '({})'.format(info['name'], info['ipa'], ', '.join(info['definitions']))
                })

    print("File generated...")
