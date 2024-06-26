from typing import List, Optional

from bson import ObjectId
from pymongo import ReturnDocument

from database import mongo_db
from utils.mongodb import is_document_found

from .models import VacancyModel
from .schemas import SearchResponse


class VacancyRepository:
    object_model = VacancyModel
    collection = mongo_db.Vacancy

    async def search(
        self,
        query: str,
        limit: int = 20,
        skip: int = 0,
    ) -> SearchResponse:

        filter_ = {}
        if query.strip():
            filter_["$text"] = {"$search": query.strip()}
        res = [
            document
            async for document in self.collection.find(filter_)
            .skip(skip)
            .limit(limit)
            .sort("is_close", 1)
        ]

        print(res)

        for r in res:
            r["_id"] = str(r["_id"])
            r["id"] = str(r["id"])

        return SearchResponse(result=res)

    async def get_all(
        self, limit=20, skip=0, filter_res: dict = None
    ) -> List[object_model]:
        if filter_res is None:
            filter_res = {}
        return [
            document
            async for document in self.collection.find(filter_res)
            .skip(skip)
            .limit(limit)
            .sort("is_close", 1)
        ]

    async def get_by_id(self, object_id: str) -> Optional[object_model]:
        return await is_document_found(
            await self.collection.find_one({"_id": ObjectId(object_id)})
        )

    async def create(self, object_create: VacancyModel):
        print(object_create.dict())
        res = await self.collection.insert_one(object_create.dict())

        r = await self.collection.find_one({"_id": res.inserted_id})

        obj = self.object_model(**r)

        return obj

    async def update(self, object_update: VacancyModel):
        res = await self.collection.find_one_and_update(
            {"_id": object_update.id},
            {"$set": object_update.dict(exclude={"_id", "id"})},
            return_document=ReturnDocument.AFTER,
        )

        return res

    async def delete(self, object_id: str) -> Optional[object_model]:
        return await is_document_found(
            await self.collection.find_one_and_delete({"_id": ObjectId(object_id)})
        )

    async def open_vacancy(self, object_id: str):
        return await is_document_found(
            await self.collection.find_one_and_update(
                {"_id": ObjectId(object_id)},
                {"$set": {"is_close": False}},
                return_document=ReturnDocument.AFTER,
            )
        )

    async def close_vacancy(self, object_id: str):
        return await is_document_found(
            await self.collection.find_one_and_update(
                {"_id": ObjectId(object_id)},
                {"$set": {"is_close": True}},
                return_document=ReturnDocument.AFTER,
            ),
        )
