import sys
from csv import DictWriter
from datetime import date
from typing import Dict, List, Union

from anki_sentence_maker.maker import Maker
from logger import logger


def generate_csv(
    filename: str, sentences_list: List[Dict[str, Union[str, List[str]]]]
) -> None:
    """Generate a csv file with list of sentences"""
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        fieldnames: List[str] = ["sentence", "information"]
        writer: DictWriter = DictWriter(file, fieldnames=fieldnames)

        for sentence in sentences_list:
            for example in sentence["examples"]:
                name: str = sentence["name"]
                ipa: str = sentence["ipa"]
                definitions: str = ", ".join(sentence["definitions"])
                writer.writerow(
                    {
                        "sentence": example,
                        "information": "{} {}\n({})".format(name, ipa, definitions),
                    }
                )


def grab_sentences_from_args(
    words: List[str],
) -> List[Dict[str, Union[str, List[str]]]]:
    """Grab sentences with the words provided"""
    sentences_list = []

    for word in words:
        sentence = Maker(word=word)
        sentences_list.append(sentence.get())
    sentences_list = [s for s in sentences_list if s]

    return sentences_list


def main() -> None:
    # First parameter from args is the name of the script
    words_from_args: List[str] = sys.argv[1:]
    sentences_list = grab_sentences_from_args(words_from_args)

    if not sentences_list:
        logger.warning(
            "We haven't got any sentences with the list of words you provided"
        )
        return

    brazil_date_notation: str = date.today().strftime("%d-%m-%y")
    filename: str = f"sentences-{brazil_date_notation}.csv"
    generate_csv(filename, sentences_list)
    logger.info(f"{filename} file has been generated")


if __name__ == "__main__":
    main()
