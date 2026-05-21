import asyncio
import sys

from pydantic import ValidationError
from models.schemas.jobs import RemotiveJob
from repositories.job_repo import create_job
from services.embedding_service import generate_embedding
from src.db.async_session_manager import sessionmanager
from src.logger.logger_config import logger

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def process_job_async(job_data: dict) -> None:
    try:
        remotive_job = RemotiveJob.model_validate(job_data)
    except ValidationError as e:
        logger.error(f"Invalid job payload: {e}")
        return

    tags = " ".join(remotive_job.tags)
    location = remotive_job.candidate_required_location or ""
    text = (
        f"{remotive_job.title} {remotive_job.description or ''} "
        f"{tags} {location}"
    ).strip()
    embedding = generate_embedding(text)

    async with sessionmanager.session() as db:
        await create_job(db, remotive_job, embedding)


def process_job(job_data: dict) -> None:
    asyncio.run(process_job_async(job_data))



