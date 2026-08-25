from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.core.auth import hash_password, verify_password, create_access_token, get_current_user
from app.core.rate_limiter import limiter
from app.db.database import db_service

router = APIRouter(prefix="/api/auth", tags=["Authentication & RBAC"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=4, max_length=100)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str
    department: str
    expires_in_seconds: int = 86400

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, request: Request):
    # Rate limiting: Max 5 login attempts per 15 minutes per IP
    limiter.check_rate_limit(request, endpoint_type="auth_login", max_requests=5, window_seconds=900)

    username_clean = req.username.strip().lower()
    password_clean = req.password.strip()

    user = db_service.get_user_by_username(username_clean)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    pwd_hash = user.get("password_hash")
    # Verify password hash
    if not pwd_hash or not verify_password(password_clean, pwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT Token
    token_data = {
        "sub": user["username"],
        "user_id": user["user_id"],
        "role": user["role"],
        "department": user["department"]
    }
    access_token = create_access_token(token_data)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user["username"],
        role=user["role"],
        department=user["department"],
        expires_in_seconds=86400
    )

@router.get("/me")
def get_me(current_user: Optional[Dict[str, Any]] = Depends(get_current_user)):
    if not current_user:
        return {
            "authenticated": False,
            "username": "guest",
            "role": "PUBLIC_VIEWER",
            "department": "Public Access"
        }
    return {
        "authenticated": True,
        "username": current_user.get("sub"),
        "role": current_user.get("role"),
        "department": current_user.get("department")
    }

@router.post("/logout")
def logout():
    return {"status": "SUCCESS", "message": "Session invalidated successfully"}
