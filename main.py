from fastapi import FastAPI
from mongoengine import connect
from account.routes import router


app = FastAPI()


connect(
    db="new",  
    host="localhost",  
    port=27017,  
    username=None,  
    password=None,  
    authentication_source=None,  
)


app.include_router(router)


