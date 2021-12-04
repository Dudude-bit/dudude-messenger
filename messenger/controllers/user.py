import datetime
import uuid

from edgedb import AsyncIOClient, MissingRequiredError
from nats import NATS
import ujson

from messenger.models.user import CreateUserModel, CreatePasswordRecoveryModel, LoginModel
from messenger.service.utils import _create_user, _create_password_recover, _create_or_return_login_token


async def create_user(user_data: CreateUserModel, pool: AsyncIOClient, nats_client: NATS):
    data = user_data.dict()
    data['activation_code'] = uuid.uuid4()
    result = await _create_user(data, pool)
    query = """
    SELECT User{username, email, activation_code} FILTER .id = <uuid>$id
    """
    result = await pool.query_required_single_json(query, id=result['id'])
    await nats_client.publish('send-email-topic', ujson.dumps({
        'email-payload': str(data['activation_code']),
        'from-email': 'no-reply@dudude-bit.com',
        'to-email': data['email'],
        'email-subject': 'user-activation'
    }).encode())
    return ujson.loads(result)


async def activate_user(activation_code: uuid.UUID, pool: AsyncIOClient):
    raise NotImplementedError()


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
