from typing import List

from fastapi import APIRouter, Depends, UploadFile

from config import BUCKET_NAME
from resume.models import ResumeModel
from resume.schemas import SearchRequest, SearchResponse
from resume.services import ResumeService
from s3.api import S3Worker

resume_router = APIRouter(tags=["resume"], prefix="/resume")


@resume_router.get("/{_id}")
async def get_resume(_id: str,
                     resume_service: ResumeService = Depends()) -> ResumeModel:
    return await resume_service.get(_id)


@resume_router.post("/search")
async def get_resumes(search_request: SearchRequest,
                      resume_service: ResumeService = Depends()):
    return await resume_service.search(search_request)


@resume_router.post("")
async def upload_resumes(files: List[UploadFile],
                         resume_service: ResumeService = Depends()):
    return await resume_service.upload(files)


@resume_router.get("/file/{filename}")
async def get_file_url(filename: str) -> str:
    return await S3Worker.get_file_url(BUCKET_NAME, filename)


@resume_router.post("/update")
async def update_resume(update_resume: ResumeModel,
                        resume_service: ResumeService = Depends()) -> ResumeModel:
    return await resume_service.update(update_resume)


@resume_router.get("/upload/{_id}")
async def get_resume(_id: str,
                     resume_service: ResumeService = Depends()):
    return await resume_service.get_upload(_id)


@resume_router.get("/match/{resume_id}")
async def get_resume(resume_id: str,
                     resume_service: ResumeService = Depends()):
    return await resume_service.get_match_vacancy(resume_id)
