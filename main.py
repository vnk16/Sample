from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import Document, StringField, ListField, BooleanField, DateTimeField, connect
from datetime import datetime
import uuid
import logging

# Connect to MongoDB (without authentication)
connect(
    db="new",  # Database name
    host="localhost",  # MongoDB host
    port=27017,  # MongoDB default port
    username=None,  # No username needed
    password=None,  # No password needed
    authentication_source=None,  # No authentication source
)

# MongoEngine AdminUser Model
class AdminUser(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    user_id = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True)
    roles = ListField(StringField(), default=["Admin"])
    status = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    created_by = StringField(default="")
    updated_at = DateTimeField(default=datetime.utcnow)
    updated_by = StringField(default="")

    meta = {
        'collection': 'admin_users'  # Specify the collection name
    }

# FastAPI app setup
app = FastAPI()

# Request Body Schema (Pydantic)
class AdminUserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str

# Response Body Schema (Pydantic)
class AdminUserResponse(BaseModel):
    first_name: str
    last_name: str
    user_id: str
    email: str
    phone: str
    status: bool
    roles: list
    created_at: datetime
    created_by: str
    updated_at: datetime
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
            created_at=admin_user.created_at,
            created_by=admin_user.created_by,
            updated_at=admin_user.updated_at,
            updated_by=admin_user.updated_by
        )

# Create Admin User (POST Endpoint)
@app.post("/admin/create", response_model=AdminUserResponse)
async def create_admin_user(admin_user: AdminUserCreateRequest):
    try:
        # Generate user_id (or you can use any UUID generation)
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

        # Return response
        return AdminUserResponse.from_orm(admin)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
