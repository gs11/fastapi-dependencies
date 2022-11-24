from fastapi import APIRouter, Depends

from app.dependencies import postgres

router = APIRouter()


@router.get("/tables")
async def get_tables(
    table_store: postgres.TableStore = Depends(postgres.get_table_store),
):
    return await table_store.get_tables()


@router.get("/users")
async def get_users(user_store: postgres.UserStore = Depends(postgres.get_user_store)):
    return await user_store.get_users()
