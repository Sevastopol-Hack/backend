from typing import List

from fastapi import APIRouter, Depends, UploadFile

from config import BUCKET_NAME
from .models import VacancyModel
from .schemas import SearchRequest, SearchResponse
from .services import VacancyService

vacancy_router = APIRouter(tags=["vacancy"], prefix="/vacancy")


@vacancy_router.get("/{_id}")
async def get_vacancy(_id: str,
                      vacancy_service: VacancyService = Depends()) -> VacancyModel:
    return await vacancy_service.get(_id)


@vacancy_router.post("/search")
async def get_vacancys(search_request: SearchRequest,
                       vacancy_service: VacancyService = Depends()):
    return await vacancy_service.search(search_request)


@vacancy_router.post("")
async def upload_vacancy(vacancy: VacancyModel,
                         vacancy_service: VacancyService = Depends()):
    return await vacancy_service.creat(vacancy)


@vacancy_router.put("/")
async def update_vacancy(vacancy: VacancyModel,
                         vacancy_service: VacancyService = Depends()) -> VacancyModel:
    return await vacancy_service.update(vacancy)
