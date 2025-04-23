from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from payment_api.backend.db import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='created')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
