from csv import DictWriter
from datetime import date

from anki_sentence_maker.maker import Maker
from logger import logger
from type.data import Data

import sys


def generate_csv(filename: str, sentences: list[Data]) -> None:
    """Generate a csv file with list of sentences"""
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        fieldnames: list[str] = ["sentence", "information"]
        writer: DictWriter = DictWriter(file, fieldnames=fieldnames)

        for s in sentences:
            for e in s.examples:
                example = e
                info = f"{s.name}  \
                {s.phonetic_notation}\n \
                ({', '.join(s.definitions)})"
                writer.writerow({
                    "sentence": example,
                    "information": info
                })


def get_sentences_from_args(
    words: list[str],
) -> list[Data]:
    """Get sentences with the words provided"""
    sentences_list = []

    for word in words:
        maker = Maker(word=word)
        sentences_list.append(maker.sentence)
    sentences_list = [s for s in sentences_list if s]

    return sentences_list


def main() -> None:
    words: list[str] = sys.argv[1:]
    sentences: list[Data] = get_sentences_from_args(words=words)

    if not sentences:
        logger.warning("We haven't got any sentences")
    else:
        brazil_date_notation: str = date.today().strftime("%d-%m-%y")
        filename: str = f"sentences-{brazil_date_notation}.csv"
        generate_csv(filename, sentences)
        logger.info(f"{filename} file has been generated")


if __name__ == "__main__":
    main()
