
from sqlalchemy import select

from app.database.database import async_session
from app.database.models import Users, Persons


async def check_user(tg_id: str):
    async with async_session() as session:
        is_reg = await session.scalar(select(Users).where(Users.tg_id==tg_id))
        if is_reg:
            return True
        return False


async def get_persons_with_id():
    async with async_session() as session:
        result = await session.execute(
            select(Persons.id, Persons.image, Persons.name)
        )
        return result.all()

async def get_all_data():
    async with async_session() as session:
        return await session.scalars(select(Persons))

async def check_admin(tg_id: str):
    async with async_session() as session:
        result = await session.scalar(
            select(Users).where(
                (Users.tg_id == tg_id) & Users.is_permission
            )
        )
        return result is not None

async def check_stars(tg_id):
    async with (async_session() as session):
        user = await session.scalar(
            select(Users).where(Users.tg_id == tg_id)
        )
        if not user:
            return False
        if user.stars >= 100:
            user.stars = user.stars - 100
            await session.commit()
            return True
        else:
            return False

async def show_profile_user(tg_id:str):
    async with async_session() as session:
        result = await session.execute(
            select(Users).where(Users.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        return user

async def get_person_by_id(person_id:int):
    async with async_session() as session:
        result = await session.execute(
            select(Persons).where(Persons.id==person_id)
        )
        return result.scalar_one_or_none()


async def check_to_buy_admin(tg_id:str):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id==tg_id))


        if not user:
            return False
        if user.is_permission:
            return True
        if user.stars >= 350:
            user.stars = user.stars - 350
            user.is_permission = True
            await session.commit()
            return True
        else:
            return False

