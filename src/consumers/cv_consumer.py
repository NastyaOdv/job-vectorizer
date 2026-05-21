import asyncio

from consumers.kafka_consumer import KafkaConsumerManager
from db.async_session_manager import sessionmanager
from repositories import cv_repo, job_repo, task_repo
from services.embedding_service import file_embedding

cv_consumer = KafkaConsumerManager(topic="cv_tasks")

async def process_task(task_data: dict) -> None:
    vector = await file_embedding(task_data["file_path"])

    async with sessionmanager.session() as db:

        await cv_repo.update_cv_embedding(
            db,
            task_data["cv_id"],
            vector,
        )

        matches = await job_repo.find_best_job_matches(
            db,
            vector,
            limit=10
        )

        await task_repo.complete_task(
            db,
            task_data["task_id"],
            matches
        )


def start() -> None:
    cv_consumer.consume(lambda task_data: asyncio.run(process_task(task_data)))
