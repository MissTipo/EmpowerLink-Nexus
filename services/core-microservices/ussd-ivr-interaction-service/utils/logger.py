import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def info(message: str):
    logger.info(message)

def error(message: str):
    logger.error(message)

