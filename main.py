from fastapi import FastAPI
from account.routes import router as account_router

app = FastAPI()

# Include routes from the account module
app.include_router(account_router)
