from abc import ABC
from typing import Literal, cast
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

INDICES = Literal["movies", "persons", "genres"]


class ServiceABC(ABC):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _get_from_elastic(self, index: INDICES, id: UUID) -> dict | None:
        try:
            data = await self.elastic.get(index=index, id=id)
            return cast(dict, data)["_source"]
        except NotFoundError:
            return None
        