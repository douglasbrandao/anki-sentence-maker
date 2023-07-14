class NoExamplesFoundException(Exception):
    def __init__(self, word: str) -> None:
        super().__init__(f'Couldn\'t find a good number of examples of [{word}]')
