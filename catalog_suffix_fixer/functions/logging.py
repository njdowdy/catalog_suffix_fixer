from loguru import logger
import sys


def log_test():
    logger.debug("Hello, World!")


def log_start(user: str = "anonymous", log_location: str = "catalog_suffix_fixer/logs/"):
    """
    Log when the script was run and who initiated it
    """
    logger.add(f"{log_location}file_" + "{time}.log")
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


def log_end(user: str = "anonymous", log_location: str = "catalog_suffix_fixer/logs/"):
    """
    Log when the script was completed and who initiated it
    """
    logger.add(f"{log_location}file_" + "{time}.log")
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
