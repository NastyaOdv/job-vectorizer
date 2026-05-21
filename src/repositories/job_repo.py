from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.jobs import DuplicateJobError
from models.job import Job
from models.schemas.jobs import RemotiveJob


async def create_job(db: AsyncSession, remotive_job: RemotiveJob, embedding: list[float]) -> Job:
    try:
        stmt = (
            insert(Job)
            .values(
                title=remotive_job.title,
                description=remotive_job.description,
                company=remotive_job.company_name,
                tags=remotive_job.tags,
                candidate_location=remotive_job.candidate_required_location,
                job_type=remotive_job.job_type,
                category=remotive_job.category,
                salary=remotive_job.salary,
                remotive_id=remotive_job.id,
                embedding=embedding,
            )
            .returning(Job)
        )

        result = await db.execute(stmt)
        job = result.scalar_one()

        await db.commit()

        return job
    except IntegrityError as e:
        await db.rollback()
        if "jobs_remotive_id_key" in str(e.orig):
            raise DuplicateJobError(f"Job already exists: {remotive_job.id}")

    except Exception as e:
        await db.rollback()


async def find_best_job_match(db: AsyncSession, embedding: list[float]) -> Job | None:
    stmt = (
        select(Job)
        .order_by(Job.embedding.cosine_distance(embedding))
        .limit(1)
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def find_best_job_matches(db: AsyncSession, embedding: list[float], limit: int = 10) -> list[dict]:
    stmt = (
        select(
            Job.id,
            Job.embedding.cosine_distance(embedding).label("distance"),
        )
        .order_by("distance")
        .limit(limit)
    )

    result = await db.execute(stmt)

    rows = result.all()

    matches = []

    for row in rows:
        similarity = round(1 - row.distance, 4)

        matches.append(
            {
                "job_id": row.id,
                "score": similarity,
            }
        )

    return matches