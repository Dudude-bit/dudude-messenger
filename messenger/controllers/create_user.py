import datetime
import uuid

from edgedb import AsyncIOClient

from messenger.models.user import CreateUserModel
from messenger.service.utils import _create_user


async def create_user(user_data: CreateUserModel, pool: AsyncIOClient):
    data = user_data.dict()
    data['activation_code'] = uuid.uuid4()
    data['created_at'] = datetime.datetime.now()
    return _create_user(data, pool)
