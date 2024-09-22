from db.__db import Database as DB

class Users(DB):
    def __init__(self):
        super().__init__('users')

    def _exists(self, _id: int):
        return self.find_one({"_id": _id} ) is not None

    def _new(self, _id: int, _language: str):
        self.insert_one(
            {
                "_id": _id, 
                "language": _language,
                "signed": False
            }
        )

    def _signedup(self, _id: int, _name: str, _age: int, _school: str):
        self.update_one(
            {"_id": _id}, 
            {
                "signed": True,
                "name": _name,
                "age": _age,
                "school": _school
            }
        )

    def user_lang(self, _id: int):
        return self.find_one({"_id": _id})["language"]