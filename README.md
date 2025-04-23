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
SECRET_KEY = 'Ставьте_свой_секрет'

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
