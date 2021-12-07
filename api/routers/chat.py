from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from edgedb import Object

from messenger.controllers.chat import create_chat
from messenger.models.chat import CreateChatModel, ResponseChatModel
from messenger.service.enums import NotSuccessDetailChoices
from messenger.service.exceptions import MessengerException
from messenger.service.utils import get_user_from_request, get_db_pool

router = APIRouter(
    prefix='/chat'
)


@router.post('/', response_model=ResponseChatModel)
async def create_chat_view(data: CreateChatModel, user=Depends(get_user_from_request), pool=Depends(get_db_pool)):
    if user is None:
        raise MessengerException(
            status.HTTP_401_UNAUTHORIZED,
            NotSuccessDetailChoices.NOT_AUTHORISED
        )
    result: dict = await create_chat(data, user, pool)
    return result
