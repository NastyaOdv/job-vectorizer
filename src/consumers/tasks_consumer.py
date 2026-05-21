from consumers.kafka_consumer import KafkaConsumerManager
from src.logger.logger_config import logger

tasks_consumer = KafkaConsumerManager(topic="tasks")


def _handle_task(payload: dict) -> None:
    logger.info(f"Task received: {payload}")


def start() -> None:
    tasks_consumer.consume(_handle_task)
