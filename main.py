import uvicorn
import asyncio
from fastapi import FastAPI
from endpoints import users, referral
import orm as db

app = FastAPI()

app.include_router(users.router)
app.include_router(referral.router)

async def main():
    await db.create_tables()

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run("main:app", reload=True)
