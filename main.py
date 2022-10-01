import sys
from csv import DictWriter
from datetime import date

from anki_sentence_maker.maker import Maker
from logger import logger


def generate_csv(
    filename: str, sentences_list: list[dict[str, str | list[str]]]
) -> None:
    """Generate a csv file with list of sentences"""
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        fieldnames: list[str] = ["sentence", "information"]
        writer: DictWriter = DictWriter(file, fieldnames=fieldnames)

        for sentence in sentences_list:
            for example in sentence["examples"]:
                name: str = sentence["name"]
                ipa: str = sentence["ipa"]
                definitions: str = ", ".join(sentence["definitions"])
                writer.writerow(
                    {
                        "sentence": example,
                        "information": f"{name} {ipa}\n({definitions})",
                    }
                )


def get_sentences_from_args(
    words: list[str],
) -> list[dict[str, str | list[str]]]:
    """Get sentences with the words provided"""
    sentences_list = []

    for word in words:
        maker = Maker(word=word)
        sentences_list.append(maker.sentence)
    sentences_list = [s for s in sentences_list if s]

    return sentences_list


def main() -> None:
    words_from_args: list[str] = sys.argv[1:]
    sentences = get_sentences_from_args(words=words_from_args)

    if not sentences:
        logger.warning("We haven't got any sentences")
    else:
        brazil_date_notation: str = date.today().strftime("%d-%m-%y")
        filename: str = f"sentences-{brazil_date_notation}.csv"
        generate_csv(filename, sentences)
        logger.info(f"{filename} file has been generated")


if __name__ == "__main__":
    main()
