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


class ExtendedKafkaProducer(KafkaProducer):
    
    def __init__(self, **kwargs):
        super(ExtendedKafkaProducer, self).__init__(**kwargs)

    async def check_for_connection(self):
        assert self.bootstrap_connected(), 'Can\'t connect to Kafka'
    
    async def close_connection(self):
        self.close()
