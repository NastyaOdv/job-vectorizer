import logging

logger = logging.getLogger("vector_logger")
logger.setLevel(logging.DEBUG)  # Change to INFO in production

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Optional: file handler # Save only INFO+ logs to file

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)