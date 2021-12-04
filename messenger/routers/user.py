import uuid

from fastapi import APIRouter, Depends, Response, status

from messenger.controllers.user import create_user, recover_password, login, activate_user
from messenger.models.user import CreateUserModel, CreatePasswordRecoveryModel, ResponseUserModel, LoginModel, \
    ResponseLoginModel
from messenger.service.utils import get_db_pool, get_nats_client

router = APIRouter(
    prefix='/user'
)


@router.post('/', response_model=ResponseUserModel)
async def create_user_view(data: CreateUserModel,
                           pool=Depends(get_db_pool),
                           nats_client=Depends(get_nats_client)):
    result: dict = await create_user(data, pool, nats_client)
    return result


@router.post('/activate')
async def activate_user_view(activation_code: uuid.UUID, pool=Depends(get_db_pool)):
    await activate_user(activation_code, pool)
    return Response(
        status_code=status.HTTP_200_OK
    )



@router.post('/login', response_model=ResponseLoginModel)
async def login_view(data: LoginModel, pool=Depends(get_db_pool)):
    result: dict = await login(data, pool)
    return result


@router.post('/password-recovery')
async def password_recovery_view(data: CreatePasswordRecoveryModel,
                                 pool=Depends(get_db_pool),
                                 nats_client=Depends(get_nats_client)):
    await recover_password(data, pool, nats_client)

    return Response(
        status_code=status.HTTP_201_CREATED
    )
