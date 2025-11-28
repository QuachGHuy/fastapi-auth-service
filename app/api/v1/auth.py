from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter()
user_service = UserService()
auth_service = AuthService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Handle user registration.
    """
    return await user_service.create_user(db=db, user_in=user_in)


@router.post("/login/form", response_model=Token, status_code=status.HTTP_200_OK)
async def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Swagger UI Login (Form Data).
    Required for the 'Authorize' button in API docs.
    """
    return await auth_service.login_oauth2(db=db, form_data = form_data)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_js(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Frontend/API Login (JSON Body).
    """
    return await auth_service.login(db=db, form_data=login_data)