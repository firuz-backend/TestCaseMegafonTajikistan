from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from payment_api.models.user import User
from payment_api.schemas.user import UserCreate
from payment_api.models.wallet import Wallet
from payment_api.backend.db_depends import get_db


"""
SECRET_KEY - вставьте пожалуйста свой SECRET_KEY, получив по команде
openssl rand -hex 32
"""
SECRET_KEY = 'Вставьте свой секретный ключ'
ALGORITHM = 'HS256'

router = APIRouter(prefix='/v1/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/token')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)], create_user: UserCreate
):
    result = await db.execute(
        insert(User).values(
            username=create_user.username,
            hashed_password=bcrypt_context.hash(create_user.password)
        )
    )
    user_id = result.inserted_primary_key[0]
    await db.execute(
        insert(Wallet).values(
            owner_id=user_id, balance=0.0
        )
    )
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'}


async def authentiate_user(
    db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str
):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def create_access_token(
    username: str, user_id: int,
    expires_delta: timedelta
):
    expire_dt = datetime.now(timezone.utc) + expires_delta
    exp_ts = int(expire_dt.timestamp())
    payload = {'sub': username, 'id': user_id, 'exp': exp_ts}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post('/token')
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authentiate_user(db, form_data.username, form_data.password)
    token = await create_access_token(
        user.username, user.id,
        expires_delta=timedelta(minutes=20)
    )
    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        expire = payload.get('exp')
        if not username or not user_id or not expire:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user')
        if expire < int(datetime.now(timezone.utc).timestamp()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired!')
        return {'username': username, 'id': user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired!')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user')


@router.get('/read_current_user')
async def read_current_user(user: dict = Depends(get_current_user)):
    return {'user': user}
