from abc import ABC, abstractclassmethod
from type.data import Data


class DataSource(ABC):
    def __init__(self, word: str) -> None:
        self.word = word

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @abstractclassmethod
    def retrieve():
        pass


class ScrapeDataSource(DataSource):
    @abstractclassmethod
    def scrape():
        pass

    def retrieve(self):
        return self.scrape()


class RestAPIDataSource(DataSource):
    @abstractclassmethod
    def get():
        pass

    def retrieve(self):
        return self.get()

