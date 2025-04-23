from fastapi import FastAPI, HTTPException, status
import random


app = FastAPI()


@app.post('/api/blacklist/check')
async def check_blacklist():
    chance = random.randint(1, 100)

    if chance <= 25:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='User is blacklisted'
        )
    return {
        'result': 'verified'
    }
