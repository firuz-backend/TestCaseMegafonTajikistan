from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from payment_api.backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)

    wallet = relationship('Wallet', back_populates='owner', uselist=False)
