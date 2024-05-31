from .models import VacancyModel
from .repositories import VacancyRepository
from .schemas import SearchRequest, SearchResponse


class VacancyService:
    repository = VacancyRepository()

    async def creat(self, vacancy: VacancyModel):
        return await self.repository.create(vacancy)

    async def get(self, _id: str):
        return await self.repository.get_by_id(_id)

    async def search(self, sr: SearchRequest) -> SearchResponse:
        res = await self.repository.search(sr.query, sr.limit, sr.skip)

        return res

    async def update(self, vacancy: VacancyModel):
        return await self.repository.update(vacancy)

    async def open_vacancy(self, object_id: str):
        return await self.repository.open_vacancy(object_id)

    async def close_vacancy(self, object_id: str):
        return await self.repository.close_vacancy(object_id)
