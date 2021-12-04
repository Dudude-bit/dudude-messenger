import nats
import edgedb
from edgedb import AsyncIOClient


class EdgeDatabase:

    def __init__(self, dsn):
        self.dsn = dsn

    async def create_pool(self):
        self.pool: AsyncIOClient = edgedb.create_async_client(
            self.dsn
        )
        ping_query = 'select 1'
        await self.pool.query(ping_query)

    async def close_pool(self):
        await self.pool.aclose()


class NatsQueue:

    def __init__(self, dsn):
        self.client = None
        self.dsn = dsn

    async def connect(self):
        self.client = await nats.connect([self.dsn])
    
    async def close_connection(self):
        await self.client.close()
