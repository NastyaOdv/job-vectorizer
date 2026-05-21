from consumers.kafka_consumer import KafkaConsumerManager
from services.job_ingest_service import process_job

jobs_consumer = KafkaConsumerManager(topic="job")


def start() -> None:
    jobs_consumer.consume(process_job)
