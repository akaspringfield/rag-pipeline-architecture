import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("rag_platform")


def log_step(step, value):

    logger.info(
        f"[{step}] => {value}"
    )