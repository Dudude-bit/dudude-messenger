import os

from fastapi import FastAPI
from starlette.requests import Request

from database import EdgeDatabase
from exceptions import NotImproperlyConfigure


def create_app():

    app = FastAPI()

    edgedb_dsn = os.getenv('edgedb_dsn', None)

    if edgedb_dsn is None:
        raise NotImproperlyConfigure('define edgeb dsn')

    db = EdgeDatabase(edgedb_dsn)

    @app.middleware('http')
    async def add_db_pool(request: Request, call_next):
        request.state.db_pool = db.pool
        response = await call_next(request)
        return response

    @app.on_event('startup')
    async def on_startup_event():
        await db.create_pool()

    @app.on_event('shutdown')
    async def on_shutdown_event():
        await db.close_pool()

    return app


if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(
        app
    )
