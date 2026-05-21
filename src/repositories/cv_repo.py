from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.cv import CV


async def update_cv_embedding(db: AsyncSession, cv_id: int, embedding: list[float]) -> None:
    stmt = (
        update(CV)
        .where(CV.id == cv_id)
        .values(embedding=embedding)
    )

    await db.execute(stmt)
    await db.commit()