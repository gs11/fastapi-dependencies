from fastapi import FastAPI

from app.dependencies import postgres
from app.routers import default

app = FastAPI()


app.include_router(default.router)


@app.on_event("startup")
async def startup_event():
    await postgres.get_connection_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await postgres.teardown_connection_pool()
