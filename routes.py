from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from account.models import AdminUser
from typing import List
import bcrypt  
from jose import JWTError, jwt
from datetime import datetime


SECRET_KEY = "b93c6c66032d4bbfe528953f1f9de4232b213ed9e52a505b1bbfa5d68c6b8b3f"
ALGORITHM = "HS256"

router = APIRouter()


class AdminUserLoginRequest(BaseModel):
    email: str
    password: str


class AdminUserLoginResponse(BaseModel):
    status: bool
    status_code: int
    description: str
    data: dict


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/admin/login", response_model=AdminUserLoginResponse)
async def login_admin_user(admin_user: AdminUserLoginRequest):
    try:
        
        admin = AdminUser.objects(email=admin_user.email).first()

        if not admin:
            raise HTTPException(status_code=404, detail="Admin user not found")

        
        if not bcrypt.checkpw(admin_user.password.encode('utf-8'), admin.password_hash.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect password")

       
        access_token = create_access_token({"sub": admin.user_id})

        
        return AdminUserLoginResponse(
            status=True,
            status_code=200,
            description="We have sent you access code via mail verification",
            data={
                "email": admin.email,
                "user_id": admin.user_id,
                "access_token": access_token
            }
        )

    except Exception as e:
        logging.error(f"Error logging in admin user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
