class PhoneticNotationNotFoundException(Exception):
    def __init__(self, word: str) -> None:
        super().__init__(f'Phonetic Notation of the word [{word}] hasn\'t been found')
