from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine)

