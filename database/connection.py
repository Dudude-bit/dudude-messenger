import edgedb
from edgedb import AsyncIOClient
from kafka import KafkaProducer


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


class KafkaQueue(KafkaProducer):

    def __init__(self):
        pass
