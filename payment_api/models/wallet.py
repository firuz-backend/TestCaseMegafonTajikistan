from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from payment_api.backend.db import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'),
                      nullable=False, unique=True)
    balance = Column(Float, default=0.0)

    owner = relationship('User', back_populates='wallet')
