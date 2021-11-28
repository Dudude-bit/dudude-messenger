import os
from typing import Callable

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.requests import Request

from database import EdgeDatabase, ExtendedKafkaProducer
from exceptions import NotImproperlyConfigure
import messenger


def create_app():

    app = FastAPI(default_response_class=UJSONResponse)

    app.include_router(messenger.router)

    edgedb_instance = os.getenv('edgedb_instance', None)

    kafka_bootstrap_host = os.getenv('kafka_host', None)

    if edgedb_instance is None:
        raise NotImproperlyConfigure('define edgedb instance name')

    if kafka_bootstrap_host is None:
        raise NotImproperlyConfigure('define kafka host')

    db = EdgeDatabase(edgedb_instance)

    kafka_queue = ExtendedKafkaProducer(bootstrap_servers=[kafka_bootstrap_host])

    @app.middleware('http')
    async def add_db_pool(request: Request, call_next: Callable):
        request.state.pool = db.pool
        request.state.kafka = kafka_queue
        response = await call_next(request)
        return response

    @app.on_event('startup')
    async def on_startup_event():
        await db.create_pool()
        await kafka_queue.check_for_connection()

    @app.on_event('shutdown')
    async def on_shutdown_event():
        await db.close_pool()
        await kafka_queue.close_connection()

    return app


if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(
        app
    )
