from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from payment_api.models.service import Service
from payment_api.schemas.services import (
    CreateServices, ShowService)
from payment_api.backend.db_depends import get_db


router = APIRouter(prefix='/v1/services', tags=['Services'])


@router.get('/list', response_model=List[ShowService])
async def services_list(db: Annotated[AsyncSession, Depends(get_db)]):
    list_of_services = await db.scalars(select(Service))
    return list_of_services.all()


@router.post('/create', response_model=ShowService,
             status_code=status.HTTP_201_CREATED)
async def create_service(
        db: Annotated[AsyncSession, Depends(get_db)],
        service_data: CreateServices):
    service_id = (
        await db.execute(
            insert(Service)
            .values(
                name=service_data.name,
                price=service_data.price
            ).returning(Service.id)
        )
    ).scalar_one()
    await db.commit()

    return ShowService(
        id=service_id, name=service_data.name, price=service_data.price)
