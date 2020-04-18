import requests
import json


class SentenceMaker:

    def __init__(self, app_id, app_key, word, language):
        self.app_id = app_id
        self.app_key = app_key
        self.word = word
        self.language = language

    def make_request(self):
        url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + self.language + "/" + self.word.lower()
        return requests.get(url, headers={"app_id": self.app_id, "app_key": self.app_key})

    def get_data(self):
        data = self.make_request().json()
        infos = {
            'word': data['results'][0]['word'], #string
            'phonetic': data['results'][0]['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling'], #string
            'definition': data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'], #array
            'examples': data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'] #array
        }
        return infos
