from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mongoengine import connect
from datetime import datetime
from jose import JWTError, jwt

# Import models
from .models import AdminUser

# JWT Secret Key for token creation and validation
SECRET_KEY = "erw#4342@rewrwer"
ALGORITHM = "HS256"

# Create router
router = APIRouter()

# Pydantic model for the request body validation
class AdminApprovalRequest(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    verification_status: bool
    email_note: str
    approved_by: str

class AdminApprovalResponse(BaseModel):
    status: bool
    status_code: int
    description: str
    data: list

# Connect to MongoDB
connect('new')

# Function to create JWT token (for simplicity)
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Route to approve or reject admin account (and create if not found)
@router.post("/admin/account/approval", response_model=AdminApprovalResponse)
async def approve_admin_account(request: AdminApprovalRequest):
    # Find the user by ID, if exists
    user = AdminUser.objects(user_id=request.user_id).first()

    if not user:
        # If user doesn't exist, create a new one
        user = AdminUser(
            user_id=request.user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            verification_status=request.verification_status,
            email_note=request.email_note,
            approved_by=request.approved_by,
            roles=["Admin"],  # default roles
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user.save()  # Save the newly created user in the database

    # Update the user details (in case the user was found)
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email
    user.phone = request.phone
    user.verification_status = request.verification_status
    user.email_note = request.email_note
    user.approved_by = request.approved_by
    user.updated_at = datetime.utcnow()

    # Save the updated user record
    user.save()

    # Return response with the updated user information
    response_data = {
        "status": True,
        "status_code": 200,
        "description": "Admin account created/updated",
        "data": [{
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": user.user_id,
            "email": user.email,
            "phone": user.phone,
            "status": user.verification_status,
            "roles": user.roles,
            "created_at": user.created_at.isoformat(),
            "created_by": user.created_by,
            "updated_at": user.updated_at.isoformat(),
            "updated_by": user.updated_by,
            "profile_image": user.profile_image,
            "verification_status": user.verification_status
        }]
    }

    return response_data
