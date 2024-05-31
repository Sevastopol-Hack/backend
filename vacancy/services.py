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
