from fastapi import FastAPI
from account.routes import router

app = FastAPI()


app.include_router(router)
