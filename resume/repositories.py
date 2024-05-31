from typing import List, Optional

from bson import ObjectId

from resume.models import ResumeModel, UploadedResume
from database import mongo_db
from resume.schemas import SearchResponse, SearchResume
from utils.mongodb import is_document_found


class ResumeRepository:
    object_model = ResumeModel
    collection = mongo_db.Resumes

    async def save_many(self, resumes: list[dict]):
        await self.collection.insert_many(resumes)
        for r in resumes:
            r["_id"] = str(r["_id"])
        return resumes

    async def search(self, limit: int = 20, skip: int = 0, experience_from: int = 0,
                     experience_to: int = 100,
                     stack: set[str] = None) -> SearchResponse:
        if stack is None:
            stack = []
        filter_ = {
            "experience": {"$gte": experience_from, "$lte": experience_to},
        }
        if stack:
            filter_["$or"] = [
                {"stack": {"$in": list(stack)}},
                {"stack": {"$regex": "|".join(stack)}}
            ]
            # filter_["stack"] = {
            #     "$or": [{"$in": list(stack)}, {"$regex": "|".join(stack)}]}

        # resume = self.collection.find(filter_).
        # self.collection.find_one
        resumes = [SearchResume(**document) async for document in
                   self.collection.find(filter_)
                   .skip(skip)
                   .limit(limit)]

        resume_with_percent = []
        # if stack:
        for resum in resumes:
            if stack:

                resum.percent = len(
                    (set(stack) & set(resum.stack))) / len(stack)
            else:
                resum.percent = 1

            resum.id = str(resum.getId())
            # resum._id = str(resum._id)

            resume_with_percent.append(resum)
        print(resume_with_percent)
        resume_with_percent.sort(key=lambda x: (x.percent, x.created_at), reverse=True)
        return SearchResponse(result=resume_with_percent)

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

    async def create(self, object_create: ResumeModel):
        res = await self.collection.insert_one(object_create.dict())

        r = await self.collection.find_one({"_id": res.inserted_id})

        obj = self.object_model(**r)

        return obj

    async def delete(self, object_id: str) -> Optional[object_model]:
        return await is_document_found(
            await self.collection.find_one_and_delete({"_id": ObjectId(object_id)}))

    # async def uploa


class UploadedResumeRepository:
    object_model = UploadedResume
    collection = mongo_db.UploadedResume

    async def create(self, user_id: int, resumes: List[str]) -> UploadedResume:
        ur = UploadedResume(
            user_id=user_id,
            resumes=resumes
        )
        res = await self.collection.insert_one(ur.dict())
        r = await self.collection.find_one({"_id": res.inserted_id})

        obj = self.object_model(**r)

        return obj

    async def get_by_id(self, object_id: str) -> Optional[object_model]:
        res =  await is_document_found(
            await self.collection.find_one({"_id": ObjectId(object_id)})
        )
        del res["id"]
        res["_id"] = str(res["_id"])
        return res
