from edgedb import AsyncIOClient
from fastapi import Header, Request


async def get_user_from_request(request: Request, token=Header(None)):
    pool = request.state.pool
    query = """
    SELECT User {id} filter .token.value = <uuid>$token
    """
    user = await pool.query(query, token=token)
    return user


def get_db_pool(request: Request):
    return request.state.pool


async def _create_chat(chat_data, pool: AsyncIOClient):
    pass


async def _create_user(user_data, pool: AsyncIOClient):
    query = """
    INSERT User {
        created_at := datetime_of_statement(),
        username := <str>$username,
        email := <email>$email,
        activation_code := <uuid>$activation_code
    }
    """
    result = await pool.query(
        query,
        username=user_data['username'],
        email=user_data['email'],
        activation_code=user_data['activation_code']
    )
    return result


async def _create_password_recover(recover_data, pool: AsyncIOClient):
    query = """
    INSERT PasswordRecovery {
        created_at := datetime_of_statement(),
        expires := <duration>$expires,
        token := <uuid>$token,
        user := (select User filter .email = <email>$email)
    }
    """
    await pool.query(query,
                     expires=recover_data['expires'],
                     token=recover_data['token'],
                     email=recover_data['email'])
