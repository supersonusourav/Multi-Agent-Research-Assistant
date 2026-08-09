import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "workflow.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("research_workflow")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def log(message: str, state=None):
    """
    Logs to:
    1. workflow.log
    2. state["logs"] (optional)
    """

    logger.info(message)

    if state is not None:

        state.setdefault("logs", []).append(message)