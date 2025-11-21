import logging 
import datetime
from typing import Annotated, Literal
from database import users_table, database
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

__name__="storeapi.main"
logger=logging.getLogger(__name__)

pwd_context=CryptContext(schemes=["bcrypt"])

def hash_password(password:str)->str:
    return(pwd_context.hash(password))

def verify_password(plain_password:str,hashed_password:str)->bool:
    return(pwd_context.verify(plain_password,hashed_password))

SECRET_KEY="cae7ed63dd93fe2c3913c317e401ac662d461c9c8cb251f6ebb535ad570eecea"
ALGORITHM="HS256"
oauth2scheme=OAuth2PasswordBearer(tokenUrl="token")

def access_token_expire_minutes()->int:
    return 30

def confirmation_token_expire_minutes()->int:
    return 1440


def create_access_token(email:str):
    logger.info("Creating access token", extra={"email":email})
    expire=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=access_token_expire_minutes())
    content={"sub":email,"expire":expire, "type":"access"}
    jwt_encoded=jwt.encode(content,key=SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encoded

def create_confirmation_token(email:str):
    logger.info("Creating confirmation token", extra={"email":email})
    expire=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=confirmation_token_expire_minutes())
    content={"sub":email,"expire":expire,"type":"confirmation"}
    jwt_encoded=jwt.encode(content,key=SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encoded


def credential_error(description:str): HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=description,
        headers={"WWW-Authenticate":"Bearer"}
    )

async def verify_token(token:str,token_type:Literal["access","confirmation"]):
    logger.info("Getting current user from token")
    try:
        payload=jwt.decode(token=token,key=SECRET_KEY,algorithm=ALGORITHM)
    except ExpiredSignatureError as e:
        raise credential_error("Token has expired") from e
    except jwt.JWTError as e:
        raise credential_error("Invalid Token") from e
    type=payload.get("type")
    if(type is None or type!=token_type): 
        raise credential_error("Invalid Token Type")
    email=payload.get("sub")
    if email is None:
        raise credential_error("Token is missing 'sub' field")
    return email

async def authenticate_user(email:str,password:str):
    logger.info("Authenticating user", extra={"email":email})
    user=await get_user(email)
    if user is None:
        raise credential_error("Incorrect email or password")
    if not verify_password(password,user['password']):
        raise credential_error("Incorrect email or password")
    if user["confirmation"] is False:
        raise credential_error("Email not confirmed")
    return user


async def get_user(email:str):
    logger.info("Fetching user with email", extra={"email":email})
    query=users_table.select().where(users_table.c.email==email)
    result=await database.fetch_one(query)
    return result

async def get_current_user(token: Annotated[str, Depends(oauth2scheme)]):
    email=await verify_token(token,token_type="access")
    user=await get_user(email)
    if user is None:
        raise credential_error("Could not find user for this token")
    return user


