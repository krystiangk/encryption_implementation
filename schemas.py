from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str


class EncryptMsg(BaseModel):
    public_key: str
    message: str


class DecryptMsg(BaseModel):
    message: str
