from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from store.core.config import settings


class MongoClient:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL,
            server_api=ServerApi("1"),
            uuidRepresentation="standard",
        )

    def get(self) -> AsyncIOMotorClient:
        return self.client


# Carregando o banco de dados
db_client = MongoClient()
