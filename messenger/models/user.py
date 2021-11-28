from pydantic import BaseModel, EmailStr


class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
