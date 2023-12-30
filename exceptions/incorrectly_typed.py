class IncorrectlyTypedException(Exception):
    def __init__(self, class_name: str, word: str) -> None:
        super().__init__(
            f"{class_name} - Was this word [{word}] typed correctly?"
        )
