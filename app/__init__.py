from typing import Callable

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api import router


def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def init_routers(app: FastAPI):
    app.include_router(router)


def create_app():
    settings = Settings()

    app = FastAPI(default_response_class=UJSONResponse)

    app.include_router(messenger.router)

    db = EdgeDatabase(settings.edgedb_instance)

    nats_queue = NatsQueue(settings.nats_dsn)

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

    uvicorn.run(
        create_app()
    )

# TODO add expiring logic to user token
# TODO add hash function on password in user model
# TODO think about not to query info again
#  after creating instance at edgedb and get it from request json (not possible every time)
# TODO change Depends(get_user_from_request) to Security(get_user_from_request)
# TODO change logic to deny no user not in view
# TODO handle no user found on login
# TODO think about move all queries to one place
