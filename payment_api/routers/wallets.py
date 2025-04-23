from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from payment_api.backend.db_depends import get_db
from payment_api.schemas.wallet import WalletTopUp, WalletSchema
from payment_api.models.wallet import Wallet
from payment_api.auth import get_current_user

router = APIRouter(prefix='/v1/wallets', tags=['Wallets'])


@router.post('/top-up', response_model=WalletSchema)
async def top_up(
    db: Annotated[AsyncSession, Depends(get_db)], data: WalletTopUp,
    current_user=Depends(get_current_user)
):
    wallet = await db.scalar(
        select(Wallet).where(Wallet.owner_id == current_user['id']))
    if not wallet:
        raise HTTPException(status_code=404, detail='Wallet not found')
    new_balance = wallet.balance + data.amount
    await db.execute(
        update(Wallet)
        .where(Wallet.id == wallet.id)
        .values(balance=new_balance))
    await db.commit()
    return WalletSchema(
        id=cast(int, wallet.id),
        balance=cast(float, new_balance))


@router.get('/me', response_model=WalletSchema)
async def get_my_wallet(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user=Depends(get_current_user)
):
    result = await db.scalars(
        select(Wallet).where(Wallet.owner_id == current_user['id']))
    wallet = result.first()
    if not wallet:
        raise HTTPException(status_code=404, detail='Wallet not found')
    return WalletSchema(
        id=cast(int, wallet.id),
        balance=cast(int, wallet.balance))
