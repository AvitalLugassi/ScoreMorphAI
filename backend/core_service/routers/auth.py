from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from user_model import User
from user_schema import UserRegister, UserLogin, TokenResponse, UserResponse
from services import get_current_user
from controllers import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: UserRegister, db: Session = Depends(get_db)):
    return AuthController(db).register(body)


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    return AuthController(db).login(body)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthController(db).me(current_user)
