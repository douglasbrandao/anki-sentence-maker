from typing import NamedTuple


class Data(NamedTuple):
    name: str
    phonetic_notation: str
    definitions: list[str]
    examples: list[str]
