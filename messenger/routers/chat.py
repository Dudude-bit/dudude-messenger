from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from messenger.controllers.create_chat import create_chat
from messenger.models.chat import CreateChatModel
from messenger.service.enums import NotSuccessDetailChoices
from messenger.service.utils import get_user_from_request, get_db_pool

router = APIRouter(
    prefix='/chat'
)


@router.post('/')
async def create_chat_view(data: CreateChatModel, user=Depends(get_user_from_request), pool=Depends(get_db_pool)):
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            NotSuccessDetailChoices.NOT_AUTHORISED
        )
    result = await create_chat(data, user, pool)
    return result
