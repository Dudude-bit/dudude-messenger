from pydantic import BaseModel, EmailStr


class CreateUserModel(BaseModel):
    username: str
    email: EmailStr


class ResponseUserModel(BaseModel):
    username: str
    email: EmailStr


class CreatePasswordRecoveryModel(BaseModel):
    email: EmailStr
