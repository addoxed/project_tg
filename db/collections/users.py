from db.__db__ import Database as DB

class Users(DB):
    def __init__(self):
        super().__init__('users')

    def _exists(self, _id: int):
        return self.find_one({"_id": _id}) is not None
    
    def _name(self, _id: int):
        return self.find_one({"_id": _id})["name"]

    def _signup(self, _id: int, language: str, name: str, age: int, school_id: str):
        self.insert_one({   
                "_id": _id,
                "language": language,
                "name": name,
                "age": age,
                "school_id": school_id
            })

    def _user_lang(self, _id: int):
        return self.find_one({"_id": _id})["language"]
    
    def _fetch_all(self):
        return self.find_all()