from pydantic import BaseModel, Field


class CreateServices(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=1)


class ShowService(BaseModel):
    id: int
    name: str
    price: float


class ServiceResponse(BaseModel):
    message: str = 'Created Successfully'
    serive_id: int
