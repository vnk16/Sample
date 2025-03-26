from fastapi import FastAPI
from account.routes import router as account_router
import account.models  # Ensure models.py is imported to establish MongoDB connection

# FastAPI app setup
app = FastAPI()

# Include the account routes
app.include_router(account_router, prefix="/account", tags=["Account"])
