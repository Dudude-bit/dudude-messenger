from fastapi import APIRouter


from .routers import chat, messenge, user

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(
    chat.router,
    tags=['Chat']
)

router.include_router(
    messenge.router,
    tags=['Messenge']
)

router.include_router(
    user.router,
    tags=['User']
)

__all__ = ['router']