from typing import List, Optional

import aiopg
from psycopg2.extras import RealDictCursor

connection_pool: Optional[aiopg.pool.Pool] = None


async def get_connection_pool() -> aiopg.pool.Pool:
    global connection_pool
    if connection_pool is None:
        connection_pool = await aiopg.create_pool(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            minsize=1,
            maxsize=10,
        )
    return connection_pool


async def teardown_connection_pool():
    connection_pool.close()
    await connection_pool.wait_closed()


async def _fetch(query: str):
    connection_pool = await get_connection_pool()
    async with connection_pool.acquire() as connection:
        async with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            await cursor.execute(query)
            return [dict(row) for row in await cursor.fetchall()]


class TableStore:
    async def get_tables(self) -> List[str]:
        return [
            row["table_name"]
            for row in await _fetch(
                query="SELECT table_name FROM information_schema.tables"
            )
        ]


class UserStore:
    async def get_users(self) -> List[str]:
        return [
            row["usename"]
            for row in await _fetch(query="SELECT usename FROM pg_catalog.pg_user")
        ]


table_store = TableStore()
user_store = UserStore()


def get_table_store():
    return table_store


def get_user_store():
    return user_store
