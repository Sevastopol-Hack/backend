import uuid
from typing import List

from fastapi import UploadFile

from config import BUCKET_NAME
from s3.api import S3Worker
from .models import ResumeModel
from .repositories import ResumeRepository, UploadedResumeRepository
from .schemas import SearchRequest, SearchResponse


class ResumeService:
    repository = ResumeRepository()

    async def update(self, resume: ResumeModel):
        return await self.repository.create(resume)

    async def get(self, _id: str):
        return await self.repository.get_by_id(_id)

    async def search(self, sr: SearchRequest) -> SearchResponse:
        res = await self.repository.search(sr.limit, sr.skip, sr.experience_from,
                                           sr.experience_to, sr.stack)

        return res

    async def upload(self, files: List[UploadFile]):
        filenames = []
        resumes = []
        for file in files:
            filename = str(uuid.uuid4()) + "_" + file.filename
            _ = await S3Worker.upload_file(
                bucket=BUCKET_NAME, file=file, filename=filename
            )
            filenames.append(filename)

            resume = ResumeModel(**{"created_at": 0,
                                    "fio": "string",
                                    "age": 0,
                                    "experience": 0,
                                    "stack": [
                                        "string"
                                    ],
                                    "jobs": [
                                        {
                                            "name": "string",
                                            "post": "string",
                                            "start": 0,
                                            "end": 0
                                        }
                                    ],
                                    "filename": "string"})
            resume.filename = filename
            resumes.append(resume.dict())
        await self.repository.save_many(resumes)
        ur = await UploadedResumeRepository().create(
            user_id=1,
            resumes=[str(r["_id"]) for r in resumes]
        )

        return ur

    async def get_upload(self, ur_id: str):
        return await UploadedResumeRepository().get_by_id(ur_id)

    async def get_match_vacancy(self, resume_id: str):
        return await self.repository.get_match_vacancy(resume_id)
