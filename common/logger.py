import logging
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "rag_platform.log")

logger = logging.getLogger("rag_platform")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers if imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Persistent file output
    # file_handler = logging.FileHandler(
    #     LOG_FILE,
    #     mode="a",          # append mode
    #     encoding="utf-8"
    # )

    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def log_step(step, value):
    logger.info(f"[{step}] => {value}")


def log_error(step, value):
    logger.error(f"[{step}] => {value}")


def log_warning(step, value):
    logger.warning(f"[{step}] => {value}")