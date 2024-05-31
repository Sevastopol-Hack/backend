from typing import List, Optional

from bson import ObjectId

from database import mongo_db
from .schemas import SearchResponse
from utils.mongodb import is_document_found
from .models import VacancyModel


class VacancyRepository:
    object_model = VacancyModel
    collection = mongo_db.Vacancy

    async def search(self, query: str, limit: int = 20,
                     skip: int = 0, ) -> SearchResponse:
        # filter_ = {
        #     "$text": {"$search": query.strip()}
        # }
        filter_ = {}
        if query.strip():
            filter_["$text"] = {"$search": query.strip()}
        res = [document async for document in self.collection.find(filter_)
        .skip(skip)
        .limit(limit)]

        print(res)

        for r in res:
            r["_id"] = str(r["_id"])
            r["id"] = str(r["id"])

        return SearchResponse(result=res)

    async def get_all(self, limit=20, skip=0, filter_res: dict = None) -> List[
        object_model]:
        if filter_res is None:
            filter_res = {}
        return [document async for document in
                self.collection.find(filter_res).skip(skip).limit(limit)]

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

    async def delete(self, object_id: str) -> Optional[object_model]:
        return await is_document_found(
            await self.collection.find_one_and_delete({"_id": ObjectId(object_id)}))
