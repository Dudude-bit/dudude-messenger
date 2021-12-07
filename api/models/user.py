from pydantic import BaseModel, EmailStr


class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class ResponseUserModel(BaseModel):
    username: str
    email: EmailStr


class LoginModel(BaseModel):
    username: str
    password: str


class ResponseLoginModel(BaseModel):
    value: str


class CreatePasswordRecoveryModel(BaseModel):
    email: EmailStr


class ChangePasswordModel(BaseModel):
    password: str
