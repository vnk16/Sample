# account/models.py
from mongoengine import Document, StringField, ListField, BooleanField, DateTimeField, connect
from datetime import datetime

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

# MongoEngine User Model
class User(Document):
    user_id = StringField(default="")
    firstname = StringField(default="")
    middlename = StringField(default="")
    lastname = StringField(default="")
    nickname = StringField(default="")
    username = StringField(default="")
    password = StringField(default="")
    dob = StringField(default="")
    phone = StringField(default="")
    gender = StringField(default="")
    contactNumber = StringField(default="")
    email = StringField(default="")
    communicationAddress = StringField(default="")
    billingAddress = StringField(default="")
    updated_date = DateTimeField(default=datetime.utcnow)
    created_date = DateTimeField(default=datetime.utcnow)
    currentAddress = StringField(default="")
    permanentAddress = StringField(default="")
    status = StringField(default="Active")
    signupSource = StringField(default="")
    auth_token = StringField(default="")
    role = ListField(default=[])
    about = StringField(default="")
    created_by = StringField(default="")
    online = BooleanField(default=False)
    firebase_token = StringField(default="")
    employee_type = StringField(default="")
    account_otp = StringField(default="1234")

    meta = {
        'collection': 'users'  # Specify the collection name
    }
