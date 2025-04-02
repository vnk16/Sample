from mongoengine import Document, StringField, BooleanField, ListField, DateTimeField
from datetime import datetime

class AdminUser(Document):
    user_id = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    verification_status = BooleanField(default=False)
    email_note = StringField()
    approved_by = StringField()
    roles = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    created_by = StringField()
    updated_by = StringField()
    profile_image = StringField()

    meta = {'collection': 'admin_users'}
