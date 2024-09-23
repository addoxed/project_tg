from fastapi import APIRouter, HTTPException
from webapp.server.models import *

class Router():
    def __init__(self, collection):
        self.router = APIRouter(
            prefix="/students"
        )
        self.collection = collection


        @self.router.get(
            "",
            response_description="List all students",
            response_model=StudentCollection
        )
        async def list_students():
            return StudentCollection(students=await self.collection.find().to_list(10))

        @self.router.get(
            "/{id}",
            response_description="Get a single student",
            response_model=StudentModel
        )
        async def show_student(id: int):
            if (
                student := await self.collection.find_one({"_id": id})
            ) is not None:
                return student

            raise HTTPException(status_code=404, detail=f"Student {id} not found")