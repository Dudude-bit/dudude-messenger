from fastapi import APIRouter, Depends, Response, status
from edgedb import Object

from messenger.controllers.user import create_user, recover_password
from messenger.models.user import CreateUserModel, CreatePasswordRecoveryModel, ResponseUserModel
from messenger.service.utils import get_db_pool

router = APIRouter(
    prefix='/user'
)


@router.post('/', response_model=ResponseUserModel)
async def create_user_view(data: CreateUserModel, pool=Depends(get_db_pool)):
    result: Object = await create_user(data, pool)
    return result


@router.post('/password-recovery')
async def password_recovery_view(data: CreatePasswordRecoveryModel, pool=Depends(get_db_pool)):
    await recover_password(data, pool)

    return Response(
        status_code=status.HTTP_201_CREATED
    )
