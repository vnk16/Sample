from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime
import uuid
from account.models import AdminUser, User
from fastapi.responses import JSONResponse
from account.auth import create_access_token, verify_token  # Import JWT functions
from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer defines the way the token should be passed in the request
# It expects the token in the 'Authorization' header (e.g., "Bearer <token>")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Request Body Schema for Admin User
class AdminUserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str

# Response Body Schema for Admin User
class AdminUserResponse(BaseModel):
    first_name: str
    last_name: str
    user_id: str
    email: str
    phone: str
    status: bool
    roles: list
    created_at: str  # Change to str
    created_by: str
    updated_at: str  # Change to str
    updated_by: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, admin_user):
        return cls(
            first_name=admin_user.first_name,
            last_name=admin_user.last_name,
            user_id=admin_user.user_id,
            email=admin_user.email,
            phone=admin_user.phone,
            status=admin_user.status,
            roles=admin_user.roles,
            created_at=admin_user.created_at.isoformat(),  # Convert to string
            created_by=admin_user.created_by,
            updated_at=admin_user.updated_at.isoformat(),  # Convert to string
            updated_by=admin_user.updated_by
        )

# Request Body Schema for Regular User
class UserCreateRequest(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    phone: str
    password: str
    dob: str
    gender: str

# Response Body Schema for Regular User
class UserResponse(BaseModel):
    user_id: str
    firstname: str
    lastname: str
    username: str
    email: str
    phone: str
    dob: str
    gender: str
    status: str
    created_date: str  # Change to str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, user):
        return cls(
            user_id=user.user_id,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            phone=user.contactNumber,
            dob=user.dob,
            gender=user.gender,
            status=user.status,
            created_date=user.created_date.isoformat()  # Convert to string
        )

# FastAPI Router for account management
router = APIRouter()

# Function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify the token and decode it
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # Return the decoded payload (user ID or other relevant info)

# Create Admin User (POST Endpoint)
@router.post("/admin/create")
async def create_admin_user(admin_user: AdminUserCreateRequest):
    try:
        # Generate user_id
        user_id = str(uuid.uuid4())

        # Create the Admin User in MongoDB
        admin = AdminUser(
            first_name=admin_user.first_name,
            last_name=admin_user.last_name,
            email=admin_user.email,
            phone=admin_user.phone,
            user_id=user_id,
            roles=["Admin", "Editor"],  # Default roles
            created_by="",  # You can add user who created this
            updated_by="",
        )

        # Save the user in the database
        admin.save()

        # Create an access token
        access_token = create_access_token(data={"sub": admin.user_id})

        # Prepare the response data
        response_data = AdminUserResponse.from_orm(admin)

        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "description": "Profile created successfully",
                "status": True,
                "data": response_data.dict(),  # Not inside a list
                "access_token": access_token,  # Only once
                "token_type": "bearer",
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status_code": 400,
                "description": f"Failed to create user: {str(e)}",
                "status": False,
                "data": []
            }
        )


# Create Regular User (POST Endpoint)
@router.post("/user/create")
async def create_user(user: UserCreateRequest):
    try:
        # Generate user_id
        user_id = str(uuid.uuid4())

        # Create the User in MongoDB
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            phone=user.phone,
            user_id=user_id,
            password=user.password,  # In a real app, don't store raw passwords!
            dob=user.dob,
            gender=user.gender,
            status="Active",  # Default status
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow(),
        )

        # Save the user in the database
        new_user.save()

        # Create an access token
        access_token = create_access_token(data={"sub": new_user.user_id})

        # Prepare the response data
        response_data = UserResponse.from_orm(new_user)

        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "description": "User created successfully",
                "status": True,
                "data": response_data.dict(),  # Not inside a list
                "access_token": access_token,  # Only once
                "token_type": "bearer",
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status_code": 400,
                "description": f"Failed to create user: {str(e)}",
                "status": False,
                "data": []
            }
        )


# Protected route (example)
@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are authorized", "user_id": current_user["sub"]}
