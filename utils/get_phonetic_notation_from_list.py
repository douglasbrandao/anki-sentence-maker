import os

import requests
from bs4 import BeautifulSoup

from anki_sentence_maker.headers import headers
from exceptions import PhoneticNotationNotFoundException


def get_phonetic_notation_from_list(words: list[str]) -> str:
    """Find a phonetic notation IPA on oxford dictionary"""

    full_phonetic_notation: str = ""

    for word in words:
        response = requests.get(
            f"{os.environ.get('OXFORD_URL')}{word}", headers=headers
        )
        soup = BeautifulSoup(response.text, "html.parser")
        phon_span_element = soup.find("span", attrs={"class": "phon"})

        if not phon_span_element:
            raise PhoneticNotationNotFoundException(
                "Phonetic Notation hasn't been found"
            )

        text = phon_span_element.text
        full_phonetic_notation += f"{text} "

    phonetic_notation = "".join(
        c for c in full_phonetic_notation if c not in "\\/"
    ).rstrip()

    return f"/{phonetic_notation}/"
