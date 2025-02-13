from fastapi import APIRouter, Depends, HTTPException
from auth import oauth2_scheme, get_current_user
import orm as db

router = APIRouter()

@router.post('/create-referral-code')
async def create_referral_code(token: str = Depends(oauth2_scheme)) -> dict:
    user = await get_current_user(token)
    referral_code = await db.get_referral_code(user.id)
    if not referral_code:
        new_code  = await db.set_referral_code(user.id)
        return {"success": True, "message": "Реферальный код создан", "code": new_code}
    else:
        return {"success": False, "message": "У пользователя уже есть активный реферальный код"}


@router.get('/referals-code/emails/{email}')
async def get_referral_code_by_email(email: str, token: str = Depends(oauth2_scheme)) -> str | None:
    res = await db.get_referrer_by_email(email)
    return res

@router.get('/referrers/{referrer_id}/referrals')
async def get_referrals_by_id_referrer(referrer_id: int, token: str = Depends(oauth2_scheme)) -> list | None:
    res = await db.get_referrals(referrer_id)
    return res

