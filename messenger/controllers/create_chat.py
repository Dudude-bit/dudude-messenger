from edgedb import AsyncIOClient

from messenger.models.chat import CreateChatModel
from messenger.service.utils import _create_chat


async def create_chat(chat_data: CreateChatModel, user, pool: AsyncIOClient):
    data = chat_data.dict()
    data['user_id'] = user[0]['user']
    result = await _create_chat(data, pool)
    return result
