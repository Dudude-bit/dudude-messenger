from fastapi import APIRouter, Depends

from messenger.controllers.create_user import create_user
from messenger.models.user import CreateUserModel
from messenger.service.utils import get_db_pool

router = APIRouter(
    prefix='/user'
)


@router.post('/', response_model=)
async def create_user_view(data: CreateUserModel, pool=Depends(get_db_pool)):
    result = await create_user(data, pool)

    return result
