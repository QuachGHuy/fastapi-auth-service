from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserLogin, UserResponse 
from app.database import get_db
from app.crud import get_user_by_email, get_user_by_username, create_user
from app.security import verify_password, create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    **Process**
    1. Check if the email is already registered.
    2. Check if the username is already taken.
    3. Hash the password and save the new user to the database

    - **user**: Registration data (username, email, password).
    - **return**: The newly created user object (excluding password).
    """
    # 1. Check for duplicate Email
    existing_email = await get_user_by_email(db=db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Check for duplicate Username
    existing_username = await get_user_by_username(db=db, username=user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 3. Create new User (Password hashing is handled within the CRUD layer)
    new_user = await create_user(db=db, user=user)
    return new_user

@router.post("/login/form", status_code=status.HTTP_200_OK)
async def login(data_form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    **Note:** This endpoint expects `application/x-www-form-urlencoded` data.
    It is primarily used for Swagger UI integration (the "Authorize" button).
    """
    # 1. Retrieve user from Database
    user = await get_user_by_username(db=db, username=data_form.username)

    # 2. Verify credentials (User existence AND Password match)
    # SECURITY NOTE: Use a generic error message to prevent User Enumeration attacks.
    # We do not want to reveal if the username exists or not.
    if not user or not verify_password(data_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 3. Generate Access Token
    # Choose user_id for generating Access Token (user_id is primary key) 
    # Convert user_id to string because JWT 'sub' claim must be a string
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token,
            "token_type": "Bearer"}

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_json(data_form: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Standard JSON login endpoint.
    
    **Usage:** Preferred by Frontend (React/Vue) and Mobile Apps.
    
    - **username**: Unique username.
    - **password**: Plain text password.
    """
    # 1. Retrieve user
    user = await get_user_by_username(db=db, username=data_form.username)

    # 2. Authenticate
    if not user or not verify_password(data_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 3. Generate Token
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token,
            "token_type": "Bearer"}