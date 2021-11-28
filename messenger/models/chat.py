from enum import Enum

from pydantic import BaseModel, validator, root_validator


class ChatTypes(str, Enum):
    PRIVATE = 'private'
    GROUP = 'group'
    CHANNEL = 'channel'


class CreateChatModel(BaseModel):
    type: ChatTypes
    name: str = None

    @root_validator
    def validate_data(cls, values):
        type = values.get('type')
        name = values.get('name')

        if type == ChatTypes.PRIVATE:
            assert name is None, 'can\'t set name to a private chat'

        return values


class ResponseChatModel(BaseModel):
    type: ChatTypes
    name: str = None
