import os
import logging
from typing import Callable

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.requests import Request

from database import EdgeDatabase, NatsQueue
from exceptions import NotImproperlyConfigure
import messenger


def create_app():
    app = FastAPI(default_response_class=UJSONResponse)

    app.include_router(messenger.router)

    edgedb_instance = os.getenv('edgedb_instance', None)

    nats_dsn = os.getenv('nats_dsn', None)

    if edgedb_instance is None:
        raise NotImproperlyConfigure('define edgedb instance name')

    if nats_dsn is None:
        raise NotImproperlyConfigure('define nats dsn')

    db = EdgeDatabase(edgedb_instance)

    nats_queue = NatsQueue(nats_dsn)

    @app.middleware('http')
    async def add_db_pool(request: Request, call_next: Callable):
        request.state.pool = db.pool
        request.state.nats = nats_queue.client
        response = await call_next(request)
        return response

    @app.on_event('startup')
    async def on_startup_event():
        await db.create_pool()
        await nats_queue.connect()

    @app.on_event('shutdown')
    async def on_shutdown_event():
        await db.close_pool()
        await nats_queue.close_connection()

    return app


if __name__ == '__main__':
    import uvicorn

    app = create_app()
    uvicorn.run(
        app
    )

# TODO add expiring logic to user token
# TODO add hash function on password in user model
# TODO think about not to query info again
#  after creating instance at edgedb and get it from request json (not possible every time)
# TODO change Depends(get_user_from_request) to Security(get_user_from_request)
# TODO change logic to deny no user not in view
# TODO handle no user found on login
# TODO think about move all queries to one place
