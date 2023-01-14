from abc import ABC, abstractclassmethod
from type.data import Data


class DataSource(ABC):
    def __init__(self, word: str) -> None:
        self.word = word

    @abstractclassmethod
    def retrieve():
        pass


class ScrapeDataSource(DataSource):
    @abstractclassmethod
    def scrape():
        pass


class RestAPIDataSource(DataSource):
    @abstractclassmethod
    def get():
        pass
