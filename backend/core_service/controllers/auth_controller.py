from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from user_schema import UserRegister, UserLogin, TokenResponse, UserResponse
from repositories import UserRepository
from services import hash_password, verify_password, create_access_token
from user_model import User


class AuthController:

    def __init__(self, db: Session):
        self.db   = db
        self.repo = UserRepository(db)

    def register(self, body: UserRegister) -> TokenResponse:
        if self.repo.get_by_email(body.email):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already registered")
        if self.repo.get_by_username(body.username):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Username already taken")

        user = self.repo.create(
            email           = body.email,
            username        = body.username,
            hashed_password = hash_password(body.password),
        )
        return TokenResponse(
            access_token = create_access_token(user.id),
            user         = UserResponse.model_validate(user),
        )

    def login(self, body: UserLogin) -> TokenResponse:
        user = self.repo.get_by_email(body.email)
        if not user or not verify_password(body.password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return TokenResponse(
            access_token = create_access_token(user.id),
            user         = UserResponse.model_validate(user),
        )

    def me(self, current_user: User) -> UserResponse:
        return UserResponse.model_validate(current_user)
