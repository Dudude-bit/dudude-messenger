from enum import Enum


class NotSuccessDetailChoices(str, Enum):
    NOT_AUTHORISED = 'not_authorised'
    NO_SUCH_TOKEN = 'no_such_token'
