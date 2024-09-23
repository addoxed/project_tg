import json

class FromJson():
    def __init__(self):
        ...

    def get_schools(self, language: str):
        with open('src/schools.json', 'r', encoding='utf-8') as f:
            return json.load(f)[language]
        
    def get_school(self, language: str, id: int):
        with open('src/schools.json', 'r', encoding='utf-8') as f:
            all = json.load(f)[language]
            one = next((s for s in all if s["id"] == id), None)
            return one["title"]
        

from_json = FromJson()