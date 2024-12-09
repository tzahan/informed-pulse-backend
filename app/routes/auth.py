from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db import db
from app.security import authenticate_user, create_access_token, get_current_user, oauth2_scheme, token_blacklist
from app.models import LoginRequest

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": user["email"]})
#     return {"access_token": access_token, "token_type": "bearer"}


# Simulated in-memory blacklist (use Redis or database for production)
#token_blacklist = set()
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), current_user: dict = Depends(get_current_user)):
    """
    Adds the token to a blacklist to revoke it.
    """
    token_blacklist.add(token)
    return {"message": "Successfully logged out"}

