from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from .models import AdminUser
from .utils import create_access_token

router = APIRouter()

class CreateAdminUser(BaseModel):
    first_name: str
    last_name: str
    user_name: str = Field(..., min_length=1, max_length=50)  
    email: str
    phone: str
    status: bool
    roles: List[str]
    profile_image: str

def generate_user_id():
    
    user_count = AdminUser.objects.count() + 1  
    return f"user_{user_count}"

@router.post("/admin/update")
async def update_user(user_data: CreateAdminUser):
    
    if not user_data.user_name or user_data.user_name.strip() == "":
        raise HTTPException(status_code=400, detail="User name is required and cannot be empty")

    try:
        
        existing_user = AdminUser.objects(user_name=user_data.user_name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this user_name already exists.")

        
        user_id = generate_user_id()

        
        new_user = AdminUser(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            user_name=user_data.user_name,
            email=user_data.email,
            phone=user_data.phone,
            status=user_data.status,
            roles=user_data.roles,
            profile_image=user_data.profile_image,
            user_id=user_id
        )

        
        new_user.save()

        
        access_token = create_access_token(data={"sub": new_user.user_id})

        
        return {
            "status": True,
            "status_code": 200,
            "description": "Admin account created successfully",
            "data": [
                {
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                    "user_name": new_user.user_name,
                    "user_id": new_user.user_id,
                    "email": new_user.email,
                    "phone": new_user.phone,
                    "status": new_user.status,
                    "roles": new_user.roles,
                    "created_at": new_user.created_at,
                    "updated_at": new_user.updated_at,
                    "profile_image": new_user.profile_image,
                    "verification_status": new_user.verification_status,
                    "access_token": access_token  # Generated JWT Token
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
