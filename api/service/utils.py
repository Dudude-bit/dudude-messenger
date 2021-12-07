import uuid

import ujson
from edgedb import AsyncIOClient
from fastapi import Header, Request, Depends


def get_db_pool(request: Request):
    return request.state.pool


def get_nats_client(request: Request):
    return request.state.nats


async def get_user_from_request(pool: AsyncIOClient = Depends(get_db_pool), token: uuid.UUID = Header(None)):
    query = """
    SELECT User {id} filter .token.value = <uuid>$token
    """
    user = await pool.query_json(query, token=token)
    return ujson.loads(user) or None


async def _create_chat(chat_data, pool: AsyncIOClient):
    pass


async def _create_user(user_data, pool: AsyncIOClient):
    query = """
    INSERT User {
        created_at := datetime_of_statement(),
        username := <str>$username,
        email := <email>$email,
        password := <str>$password,
        activation_code := <uuid>$activation_code
    }
    """
    result = await pool.query_single_json(
        query,
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        activation_code=user_data['activation_code']
    )
    return ujson.loads(result)


async def _activate_user(activation_code, pool: AsyncIOClient):
    query = """
    UPDATE User FILTER .activation_code = <uuid>$activation_code
            SET
            {
                is_active := true
            }
    """
    await pool.query_required_single_json(query, activation_code=activation_code)


async def _create_or_return_login_token(login_data, pool: AsyncIOClient):
    query = """
    INSERT Token {
        created_at := datetime_of_statement(),
        user := (select User filter .username = <str>$username and .password = <str>$password),
        value := <uuid>$value
    }
    unless conflict on .user 
    else (select Token)
    """
    result = await pool.query_single_json(query, username=login_data['username'],
                                          password=login_data['password'],
                                          value=login_data['value']
                                          )

    return ujson.loads(result)


async def _create_password_recover(recover_data, pool: AsyncIOClient):
    query = """
    INSERT PasswordRecovery {
        created_at := datetime_of_statement(),
        expires := <duration>$expires,
        token := <uuid>$token,
        user := (select User filter .email = <email>$email)
    }
    """
    await pool.query_single_json(query,
                                 expires=recover_data['expires'],
                                 token=recover_data['token'],
                                 email=recover_data['email'])


async def _change_password(token, change_password_data, pool: AsyncIOClient):
    query = """
    UPDATE PasswordRecovery 
    FILTER .token = <uuid>$token 
    SET { .user.password := <str>$password }
    """
    await pool.query_single_json(query,
                                 token=token,
                                 password=change_password_data['password'])
