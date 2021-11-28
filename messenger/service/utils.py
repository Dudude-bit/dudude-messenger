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
        created_at := <datetime>$created_at,
        username := <str>$username,
        email := <email>$email,
        activation_code := <str>$activation_code
    }
    """
    result = pool.query(
        query,
        created_at=user_data['created_at'],
        username=user_data['username'],
        email=user_data['email'],
        activation_code=user_data['activation_code']
    )
    return result
