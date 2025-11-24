from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

#Database setup:
DATABASE_URL = "postgresql+asyncpg://postgres:mypassword@localhost:5432/ai_job_assistant"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependancy for fastapi to get db session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session