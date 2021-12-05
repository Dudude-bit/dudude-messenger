import datetime
import uuid

from edgedb import AsyncIOClient, MissingRequiredError, NoDataError
from nats import NATS
import ujson
from starlette import status

from messenger.models.user import CreateUserModel, CreatePasswordRecoveryModel, LoginModel, ChangePasswordModel
from messenger.service.enums import NotSuccessDetailChoices
from messenger.service.exceptions import MessengerException
from messenger.service.utils import _create_user, _create_password_recover, _create_or_return_login_token, \
    _activate_user, _change_password


async def create_user(user_data: CreateUserModel, pool: AsyncIOClient, nats_client: NATS):
    data = user_data.dict()
    data['activation_code'] = uuid.uuid4()
    result = await _create_user(data, pool)

    query = """
    SELECT User{username, email, activation_code} FILTER .id = <uuid>$id
    """

    result = ujson.loads(await pool.query_required_single_json(query, id=result['id']))

    await nats_client.publish('send-email-topic', ujson.dumps({
        'email-payload': result['activation_code'],
        'from-email': 'no-reply@dudude-bit.com',
        'to-email': result['email'],
        'email-subject': 'user-activation'
    }).encode())

    return result


async def activate_user(activation_code: uuid.UUID, pool: AsyncIOClient):
    try:
        await _activate_user(activation_code, pool)
    except NoDataError:
        raise MessengerException(status.HTTP_404_NOT_FOUND, NotSuccessDetailChoices.NO_SUCH_TOKEN)


async def login(login_data: LoginModel, pool: AsyncIOClient):
    data = login_data.dict()
    data['value'] = uuid.uuid4()
    result = await _create_or_return_login_token(data, pool)
    query = """
    SELECT Token{value} FILTER .id = <uuid>$id
    """
    result = await pool.query_required_single_json(query, id=result['id'])

    return ujson.loads(result)


async def recover_password(recover_data: CreatePasswordRecoveryModel, pool: AsyncIOClient, nats_client: NATS):
    data = recover_data.dict()
    data['expires'] = datetime.timedelta(hours=1)
    data['token'] = uuid.uuid4()
    try:
        await _create_password_recover(data, pool)
    except MissingRequiredError:
        pass
    else:
        await nats_client.publish('send-email-topic', ujson.dumps({
            'email-payload': str(data['token']),
            'from-email': 'no-reply@dudude-bit.com',
            'to-email': data['email'],
            'email-subject': 'password-recovery'
        }).encode())


async def change_password(token: uuid.UUID, change_password_data: ChangePasswordModel, pool: AsyncIOClient):
    data = change_password_data.dict()
    try:
        await _change_password(token, data, pool)
    except NoDataError:
        raise MessengerException(status.HTTP_404_NOT_FOUND, NotSuccessDetailChoices.NO_SUCH_TOKEN)
