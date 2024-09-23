from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from webapp.server.router import Router
from config import settings

class FastAPIServer():
    def __init__(self):
        self.app = FastAPI()

        self.client = AsyncIOMotorClient(settings.DB_URL)
        self.db = self.client[settings.DB_CLUSTER]
        self.collection = self.db['users']
        
        self.app.include_router(Router(self.collection).router)


app = FastAPIServer().app