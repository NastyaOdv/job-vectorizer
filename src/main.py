import asyncio
import signal
import sys
import threading

from consumers.cv_consumer import cv_consumer, start as start_cv_consumer
from consumers.jobs_consumer import jobs_consumer, start as start_jobs_consumer
from src.logger.logger_config import logger

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ALL_CONSUMERS = [
    jobs_consumer,
    cv_consumer
]

_shutdown_started = False


def shutdown_consumers(*_) -> None:
    global _shutdown_started
    if _shutdown_started:
        return
    _shutdown_started = True

    logger.info("Shutting down Kafka consumers...")
    for consumer in ALL_CONSUMERS:
        consumer.close()


def main() -> None:
    signal.signal(signal.SIGINT, shutdown_consumers)
    signal.signal(signal.SIGTERM, shutdown_consumers)

    threads = [
        threading.Thread(target=start_jobs_consumer, name="jobs-consumer"),
        threading.Thread(target=start_cv_consumer, name="cv-consumer")
    ]

    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        shutdown_consumers()


if __name__ == "__main__":
    main()
