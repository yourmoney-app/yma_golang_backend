from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

import asyncpg
from asyncpg.pool import Pool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from .config import config


class DatabaseConnectionPool(object):
    pools: dict[str, Pool] = dict()

    async def get_master_db(self):
        if "main" not in self.pools:
            self.pools["main"] = await asyncpg.create_pool(
                min_size=1, max_size=20, max_inactive_connection_lifetime=300,
            )

        return await self.pools["main"].acquire()

    async def destroy_master_db(self, db):
        if "main" not in self.pools:
            return

        await self.pools["main"].release(db)

    async def get_customer_db(self, customer: str):
        if customer not in self.pools:
            self.pools[customer] = await asyncpg.create_pool(
                min_size=1, max_size=10, max_inactive_connection_lifetime=300,
            )

        return await self.pools[customer].acquire()

    async def destroy_customer_db(self, customer: str, db):
        if customer not in self.pools:
            return

        return await self.pools[customer].release(db)


class DatabaseMiddleware(BaseHTTPMiddleware):
    engines: dict[str, AsyncEngine] = dict()
    temporary_engines = []

    def __init__(self, app: FastAPI):
        self.app = app
        self.engines["main"] = create_async_engine(
            url=f"postgresql+asyncpg://{config.PGSQL_USER}:{config.REDIS_PWD}"
            + f"@{config.PGSQL_HOST}:{config.PGSQL_PORT}/{config.PGSQL_DB_CORE}",
            future=True,
            echo=True,
        )

    async def dispatch_func(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        session_maker = sessionmaker(self.engines["main"], class_=AsyncSession)
        async with session_maker() as session:
            async with session.begin():
                request.state.session = session
                response = await call_next(request)

        return response


database_pool = DatabaseConnectionPool()