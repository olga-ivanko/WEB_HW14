from fastapi import FastAPI
import uvicorn

from src.routes import contacts, auth, users
from src.conf.config import settings

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(contacts.router_b, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")
async def startup():
    """
    Function to run on application startup.
    """
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
    """
    Root endpoint returning a greeting message.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
