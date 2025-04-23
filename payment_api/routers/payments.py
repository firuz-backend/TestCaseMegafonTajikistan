from typing import Annotated, cast

import asyncio
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from payment_api.backend.db_depends import get_db
from payment_api.schemas.payment import (
    PaymentCreate, PaymentResponse, PaymentStatus)
from payment_api.models.payment import Payment
from payment_api.models.wallet import Wallet
from payment_api.models.service import Service
from payment_api.services.payment_service import process_payment
from payment_api.auth import get_current_user

router = APIRouter(prefix='/v1/payments', tags=['Payments'])


@router.post('/', response_model=PaymentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_payment(
    db: Annotated[AsyncSession, Depends(get_db)],
    payload: PaymentCreate,
    current_user: dict = Depends(get_current_user)
):
    wallet = await db.scalar(
        select(Wallet).where(Wallet.owner_id == current_user['id'])
    )
    if not wallet:
        raise HTTPException(status_code=404, detail='Wallet not found')
    service = await db.scalar(
        select(Service).where(Service.id == payload.service_id))
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    payment_id = (
        await db.execute(
            insert(Payment)
            .values(
                wallet_id=wallet.id,
                service_id=payload.service_id,
                status='created',
                amount=service.price
            )
            .returning(Payment.id)
        )
    ).scalar_one()

    await db.commit()
    asyncio.create_task(process_payment(
        payment_id, payload.service_id, cast(int, wallet.id)))
    return PaymentResponse(
        payment_id=payment_id, status='created',
        amount=cast(float, service.price))


@router.get('/{payment_id}', response_model=PaymentStatus)
async def get_status(
    db: Annotated[AsyncSession, Depends(get_db)],
    payment_id: int,
    current_user: dict = Depends(get_current_user)
):
    payment = (await db.scalars(
        select(Payment).where(Payment.id == payment_id)
    )).first()
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    return PaymentStatus(
        payment_id=payment.id,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at
    )
