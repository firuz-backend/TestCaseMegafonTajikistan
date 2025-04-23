from fastapi import FastAPI
from payment_api.routers import wallets, payments, services
from payment_api.auth import router as auth_router

app = FastAPI(title='Payment API')
app.include_router(auth_router)
app.include_router(wallets.router)
app.include_router(payments.router)
app.include_router(services.router)
