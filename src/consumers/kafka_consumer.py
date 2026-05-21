import json
from typing import Any, Callable, Optional

from kafka import KafkaConsumer

from exceptions.jobs import DuplicateJobError
from src.logger.logger_config import logger


class KafkaConsumerManager:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str = "localhost:9092",
        group_id: str | None = None,
        consumer_kwargs: dict[str, Any] | None = None,
    ) -> None:
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers
        self._group_id = group_id or f"job-vectorizer-{topic}"
        self._consumer_kwargs = consumer_kwargs or {}
        self._consumer: Optional[KafkaConsumer] = None
        self._running = False

    def _get_consumer(self) -> KafkaConsumer:
        if self._consumer is None:
            logger.debug(f"Connecting Kafka consumer to {self._bootstrap_servers}")

            try:
                self._consumer = KafkaConsumer(
                    self._topic,
                    bootstrap_servers=self._bootstrap_servers,
                    group_id=self._group_id,
                    auto_offset_reset="earliest",
                    enable_auto_commit=False,
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                    **self._consumer_kwargs,
                )

                logger.info(
                    f"✅ Kafka consumer created for topic '{self._topic}'"
                )

            except Exception as e:
                logger.exception(f"❌ Failed to create Kafka consumer: {e}")
                raise

        return self._consumer

    def consume(self, handler: Callable[[dict], None]) -> None:
        consumer = self._get_consumer()
        self._running = True

        logger.info(f"🚀 Kafka consumer started on topic '{self._topic}'")

        try:
            while self._running:
                batch = consumer.poll(timeout_ms=500)
                if not batch:
                    continue

                for messages in batch.values():
                    for message in messages:
                        if not self._running:
                            return

                        try:
                            payload = message.value
                            logger.info(
                                f"📥 Received message from '{self._topic}'"
                            )

                            handler(payload)
                            consumer.commit()
                        except DuplicateJobError:
                            logger.warning("⚠️ Duplicate job, skipping")
                            consumer.commit()
                        except Exception as e:
                            logger.exception(
                                f"❌ Error processing message: {e}"
                            )
        finally:
            self._running = False
            logger.info(f"Consumer loop stopped for topic '{self._topic}'")

    def close(self) -> None:
        self._running = False

        if self._consumer is None:
            return

        logger.info(f"🔻 Closing Kafka consumer for topic '{self._topic}'")
        self._consumer.close()
        self._consumer = None
        logger.info("✅ Kafka consumer closed")
