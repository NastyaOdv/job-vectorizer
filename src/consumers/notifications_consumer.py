from consumers.kafka_consumer import KafkaConsumerManager
from src.logger.logger_config import logger

notifications_consumer = KafkaConsumerManager(topic="notifications")


def _handle_notification(payload: dict) -> None:
    logger.info(f"Notification received: {payload}")


def start() -> None:
    notifications_consumer.consume(_handle_notification)
