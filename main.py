from fastapi import Depends, FastAPI
import uvicorn

from src.routes import contacts, auth
from src.conf.config import settings

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter


app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(contacts.router_b, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=0, 
        encoding="utf-8", 
        decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
