from pydantic import BaseModel
from typing import List


class StudentModel(BaseModel):
    _id: int
    name: str
    age: int
    school_id: int


class StudentCollection(BaseModel):
    students: List[StudentModel]