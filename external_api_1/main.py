from fastapi import FastAPI, HTTPException, status
import random


app = FastAPI()


@app.post('/api/verify')
async def verify():
    chance = random.randint(1, 100)

    if chance <= 10:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Verification failed'
        )
    return {
        'result': 'verified'
    }
