import datetime
import uuid

from edgedb import AsyncIOClient, MissingRequiredError

from messenger.models.user import CreateUserModel, CreatePasswordRecoveryModel
from messenger.service.utils import _create_user, _create_password_recover


async def create_user(user_data: CreateUserModel, pool: AsyncIOClient):
    data = user_data.dict()
    data['activation_code'] = uuid.uuid4()
    return (await _create_user(data, pool))[0]


async def recover_password(recover_data: CreatePasswordRecoveryModel, pool: AsyncIOClient):
    data = recover_data.dict()
    data['expires'] = datetime.timedelta(hours=1)
    data['token'] = uuid.uuid4()
    try:
        await _create_password_recover(data, pool)
    except MissingRequiredError:
        pass
