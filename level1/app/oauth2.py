from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from datetime import datetime,timedelta
from jose import JWTError,jwt
from app import schemas,models
from sqlalchemy.orm import Session
from app.database import(get_db)
from app.logger import logger
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes

def create_access_token(data: dict):
    logger.info("Creating access token")
    to_encode= data.copy()
    expire= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    logger.info("Access token created successfully")
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    logger.info("Verifying access token")


    try:
        payload= jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str=payload.get("user_id")
        if id is None:
            logger.warning("Token verification failed: user_id missing")
            raise credentials_exception
        logger.info("Access token verified successfully")
        token_data= schemas.Token_data(id=id)
    except JWTError:
        logger.warning("Token verification failed: invalid or expired token")
        raise credentials_exception
    return token_data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):
    logger.info("User authorization started")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    if token.user_type != "user":
        logger.warning("Authorization failed: not a user token")
        raise HTTPException(status_code=403, detail="Not authorized as user")

    user = db.query(models.User).filter(models.User.id == token.id).first()
    if not user:
        logger.warning("Authorization failed: user not found")
        raise credentials_exception
    logger.info(f"User authorized successfully user_id={user.id}")
    return user

def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    logger.info("Admin authorization started")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized as admin",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        user_type: str = payload.get("user_type")

        if user_id is None or user_type != "admin":
            logger.warning("Admin authorization failed: invalid token type")
            raise credentials_exception

    except JWTError:
        logger.warning("Admin authorization failed: invalid or expired token")
        raise credentials_exception

    admin = db.query(models.Admin).filter(models.Admin.id == user_id).first()
    if admin is None:
        logger.warning("Admin authorization failed: admin not found")
        raise credentials_exception
    logger.info(f"Admin authorized successfully admin_id={admin.id}")
    return admin
