"""Database migration helper. Run with: python -m app.db.migrate"""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings


async def ensure_pgvector_extension() -> None:
    """Ensure pgvector extension is available in the database."""
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL.replace("+asyncpg", ""))
    async with engine.connect() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.commit()


if __name__ == "__main__":
    import asyncio
    asyncio.run(ensure_pgvector_extension())
