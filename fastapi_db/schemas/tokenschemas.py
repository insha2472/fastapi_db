from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    refresh_token: str

class loginSchema(BaseModel):
    email: str
    password: str

