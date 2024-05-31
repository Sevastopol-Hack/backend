import asyncio
import json
import uuid
from typing import List

from fastapi import UploadFile

from config import BUCKET_NAME
from s3.api import S3Worker
from .models import ResumeModel
from .repositories import ResumeRepository, UploadedResumeRepository
from .schemas import SearchRequest, SearchResponse
from utils import parse as resume_parser


class ResumeService:
    repository = ResumeRepository()

    async def update(self, resume: ResumeModel):
        return await self.repository.update(resume)

    @staticmethod
    async def get_s3_file_url(filename):
        return await S3Worker.get_file_url(BUCKET_NAME, filename)

    async def get(self, _id: str):
        return await self.repository.get_by_id(_id)

    async def search(self, sr: SearchRequest) -> SearchResponse:
        res = await self.repository.search(sr.limit, sr.skip, sr.experience_from,
                                           sr.experience_to, sr.stack)

        return res

    async def upload(self, files: List[UploadFile]):
        filenames = []
        resumes = []
        file_urls = []
        for file in files:
            filename = str(uuid.uuid4()) + "_" + file.filename
            _ = await S3Worker.upload_file(
                bucket=BUCKET_NAME, file=file, filename=filename
            )
            filenames.append(filename)

            file_url = await self.get_s3_file_url(filename)
            file_urls.append(file_url)

        tasks = await asyncio.gather(*[resume_parser(f) for f in file_urls])

        for fname, parse in tasks:
            print(parse)

            resume = ResumeModel(**{"created_at": 0,
                                    **json.loads(parse),
                                    "filename": fname,})
            # resume.filename = filename
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
