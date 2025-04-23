

# Test Case - Megafon Tajikistan
This repository contains my solution for the Backend Developer test assignment in Python for Megafon Tajikistan.



# Payment API Project 0.1.0

**Docs UI:** http://127.0.0.1:8000/docs


## Описание
REST API для регистрации пользователей, управления кошельками и платежами.  
Поддерживает асинхронную проверку:  
- две внутренние проверки (наличие пользователя и баланса в PostgreSQL)  
- два внешних HTTP-запроса (случайный сбой ~10% и ~25%)  

## Требования
- Python 3.12+
- PostgreSQL

## Установка
```bash
git clone https://github.com/firuz-backend/TestCaseMegafonTajikistan
cd TestCaseMegafonTajikistan
pip install -r requirements.txt
```

## Конфигурация
В файлах `payment_api/backend/db.py`,  `payment_api/auth.py` и `alembic.ini` замените заглушки:
```python
# db.py
async_engine = create_async_engine(
    'postgresql+asyncpg://user:password@localhost:5432/your_db',
    echo=True
)

# auth.py
SECRET_KEY = 'Ставьте_свой_секрет' (в терминале пропещите чтоб получить секретный ключ - openssl rand -hex 32)

# alembic.ini
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/your_db
```

## Миграции
```bash
alembic upgrade head
```

## Запуск
1. Запустите внешние сервисы:
   ```bash
   uvicorn external_service_1.main:app --port 8001 --reload
   uvicorn external_service_2.main:app --port 8002 --reload
   ```
2. Запустите API:
   ```bash
   uvicorn payment_api.main:app --port 8000 --reload
   ```

## Маршруты API
Все маршруты начинаются с `/v1`.

### Аутентификация
- POST `/v1/auth/` — Create User (без авторизации)
- POST `/v1/auth/token` — Login (форм‑данные)
- GET  `/v1/auth/read_current_user` — Read Current User (Bearer)

### Кошельки
- POST `/v1/wallets/top-up` — Top Up (Bearer)
- GET  `/v1/wallets/me` — Get My Wallet (Bearer)

### Сервисы
- GET  `/v1/services/list` — Services List (без авторизации)
- POST `/v1/services/create` — Create Service (без авторизации)

### Платежи
- POST `/v1/payments/` — Create Payment (Bearer)
- GET  `/v1/payments/{payment_id}` — Get Status (Bearer)

## Как это работает
1. Создайте пользователя: `POST /v1/auth/`  
2. Войдите: через пользовательский интерфейс, и в дальнейшем браузер сам будет запросы отправлять с токеном 
3. Пополните баланс: `POST /v1/wallets/top-up`  
4. (Опционально) Создайте услугу: `POST /v1/services/create`  (если нету активной услуги, то процесс не пройдет)
5. Убедитесь, что external_service_1 и external_service_2 запущены  
6. Проведите платёж: `POST /v1/payments/`  
7. Узнайте статус: `GET /v1/payments/{payment_id}`

## ENGLISH VERSION

# Test Case - Megafon Tajikistan
This repository contains my solution for the Backend Developer test assignment in Python for Megafon Tajikistan.



# Payment API Project 0.1.0

**Docs UI:** http://127.0.0.1:8000/docs


## Description
A REST API for user registration, wallet management, and payments.  
Supports asynchronous checking:  
- two internal checks (user existence and balance in PostgreSQL)  
- two external HTTP requests (random failure ~10% and ~25%)   


## Requirements
- Python 3.12+
- PostgreSQL

## Installation
```bash
git clone https://github.com/firuz-backend/TestCaseMegafonTajikistan
cd TestCaseMegafonTajikistan
pip install -r requirements.txt
```

## Configuration
In the files payment_api/backend/db.py, payment_api/auth.py, and alembic.ini, replace the placeholders:
```python
# db.py
async_engine = create_async_engine(
    'postgresql+asyncpg://user:password@localhost:5432/your_db',
    echo=True
)

# auth.py
SECRET_KEY = 'Put_your_secret_here' (openssl rand -hex 32)

# alembic.ini
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/your_db
```

## Database Migrations
Apply existing migrations with:
```bash
alembic upgrade head
```

## Running the Services
1. Start the external mock services:
   ```bash
   uvicorn external_service_1.main:app --port 8001 --reload
   uvicorn external_service_2.main:app --port 8002 --reload
   ```
2. Start the main API:
   ```bash
   uvicorn payment_api.main:app --port 8000 --reload
   ```

## API Routes (v1)
All endpoints are prefixed with `/v1`.

### Authentication
- **POST** `/v1/auth/` — Create User (no auth)
- **POST** `/v1/auth/token` — Login (form data)
- **GET**  `/v1/auth/read_current_user` — Read Current User (Bearer)

### Wallets
- **POST** `/v1/wallets/top-up` — Top Up Wallet (Bearer)
- **GET**  `/v1/wallets/me` — Get My Wallet (Bearer)

### Services
- **GET**  `/v1/services/list` — List Services (no auth)
- **POST** `/v1/services/create` — Create Service (no auth)

### Payments
- **POST** `/v1/payments/` — Create Payment (Bearer, idempotent)
- **GET**  `/v1/payments/{payment_id}` — Get Payment Status (Bearer)

## How It Works
1. **Create a user**: `POST /v1/auth/` via Swagger UI (`/docs`).  
2. **Log in**: `POST /v1/auth/token` to obtain a Bearer token.  
3. **Top up wallet**: `POST /v1/wallets/top-up`.  
4. **(Optional) Create a service**: `POST /v1/services/create`.  
5. **Ensure external services** are running on ports 8001 and 8002.  
6. **Initiate a payment**: `POST /v1/payments/`.  
7. **Check payment status**: `GET /v1/payments/{payment_id}`.

