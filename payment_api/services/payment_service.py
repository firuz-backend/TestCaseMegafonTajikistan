import asyncio
import httpx
from sqlalchemy import select, update
from fastapi import HTTPException, status

from payment_api.models.service import Service
from payment_api.models.payment import Payment
from payment_api.models.wallet import Wallet
from payment_api.backend.db_depends import async_session_maker


async def process_payment(payment_id: int, service_id: int, wallet_id: int):

    async with async_session_maker() as db:
        service = await db.scalar(
            select(Service).where(Service.id == service_id))

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Service Not Found'
            )
        price = service.price

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            client.post('http://localhost:8001/api/verify'),
            client.post('http://localhost:8002/api/blacklist/check'),
            return_exceptions=True
        )

    success = all(
        not isinstance(r, Exception)
        and r.status_code == 200 for r in results  # type: ignore
    )

    async with async_session_maker() as db:
        await db.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status='success' if success else 'failed', amount=price))
        if success:
            wallet = (
                await db.scalar(select(Wallet).where(Wallet.id == wallet_id)))
            if not wallet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Wallet not found'
                )
            wallet.balance -= price  # type: ignore
        await db.commit()
