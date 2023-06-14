import os

from core.logger_class import Logger

if __name__ == "__main__":
    logger = Logger()
    logger.info(os.getcwd())
    logger.info("info")
    logger.error("info")
    logger.warning("warning")
