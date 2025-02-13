from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from schemas import UserSchema
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import orm as db
import auth

router = APIRouter()

@router.post('/create-user')
async def create_user(new_user: UserSchema) -> dict:
    try:
        await db.create_user(new_user)
        return {"success": True, "message": "Новый пользователь создан"}
    except IntegrityError:
        return {"success": False, "message": "Пользователь с указанным адресом уже зарегистрирован!"}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await db.get_user_by_email(email=form_data.username)
    if not user or not await db.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=404,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
