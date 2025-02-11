from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    email: EmailStr = Field(max_length=25)
    password: str = Field(max_length=30)
    referral_code: str

class TokenData(BaseModel):
    email: str