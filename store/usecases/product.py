from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.models.product import ProductModel
from store.mongodbAtlas import db_client
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database("store_db")
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())

        try:
            await self.collection.insert_one(product_model.model_dump())
        except Exception as ex:
            raise ex("Error: Product Not Inserted")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def query_filter_price(self, p_min: float, p_max: float) -> List[ProductOut]:
        return [
            ProductOut(**item)
            async for item in self.collection.find(
                filter={"price": {"$gte": p_min, "$lte": p_max}}
            )
        ]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        try:
            result = await self.collection.find_one_and_update(
                filter={"id": id},
                update={"$set": body.model_dump(exclude_none=True)},
                return_document=pymongo.ReturnDocument.AFTER,
            )
            return ProductUpdateOut(**result)
        except Exception:
            raise NotFoundException(message=f"Product not found with filter: {id}")

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
