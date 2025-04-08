from mongoengine import Document, StringField, BooleanField, ListField, DateTimeField
import datetime


from mongoengine import connect
connect("new", host="localhost", port=27017)  

class AdminUser(Document):
    user_id = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    user_name = StringField(required=True, unique=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    status = BooleanField(default=True)
    roles = ListField(StringField(), default=["admin"])
    profile_image = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    verification_status = BooleanField(default=True)

    meta = {'indexes': ['user_name']}  
