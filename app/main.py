from fastapi import FastAPI
from app.routes import user, auth
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Informed Pulse backend API",
    description="An API to manage user registration, login, and news data retrive from DB",
    version="1.0.0"
)

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,  # Allow cookies to be included
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routes
app.include_router(user.router, prefix="/user", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")

# Run this file with the following command:
# uvicorn app.main:app --reload

