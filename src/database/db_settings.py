from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.settings import Settings

db_url = (f"postgresql+psycopg2://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}"
          f"@{Settings.POSTGRES_HOST}:{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}")

async_db_url = (f"postgresql+asyncpg://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}"
                f"@{Settings.POSTGRES_HOST}:{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}")

engine = create_async_engine(
    async_db_url,
    # echo=True,
    future=True,
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
