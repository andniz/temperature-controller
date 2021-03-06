import logging
import os

from dotenv import load_dotenv


def get_logger(name):
    load_dotenv()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    env = os.getenv('environment', 'development')
    if env == 'production':
        handler = logging.FileHandler('logs/controller.log')
    else:
        handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
