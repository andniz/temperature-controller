import json
import os
from datetime import datetime

import pytz
from marshmallow.exceptions import MarshmallowError

from .config_schema import ConfigSchema
from .exceptions import FermentationConfigParserError
from .logger import get_logger


logger = get_logger(__name__)


class FermentationConfigParser:
    @classmethod
    def get_file_content(cls, filename):
        logger.debug(f'')
        try:
            with open(filename, 'r') as f:
                content = json.load(f)
        except FileNotFoundError:
            raise FermentationConfigParserError('Config file not found at given location')
        except json.decoder.JSONDecodeError:
            raise FermentationConfigParserError('Config file is not valid JSON')
        return content

    @classmethod
    def load_with_schema(cls, json_content):
        schema = ConfigSchema()
        return schema.load(json_content)

    @classmethod
    def parse_step_info(cls, config):
        timezone_name = os.getenv('timezone', 'Europe/Warsaw')
        now = datetime.now(tz=pytz.timezone(timezone_name))
        if now < config['start_datetime']:
            logger.info("Scheduled fermentation hasn't begun")
            return None
        steps = config['steps']
        for step in steps:
            step_end = step['end_datetime']
            if now <= step_end:
                return step
        logger.info('Scheduled fermentation has finished')
        return None

    @classmethod
    def get_step_info(cls, filename):
        logger.info(f'Parser received a request to parse file {filename}')
        content = cls.get_file_content(filename)
        try:
            config = cls.load_with_schema(content)
        except MarshmallowError:
            logger.critical('Improperly constructed config file')
            raise FermentationConfigParserError('Config file is improperly constructed')
        step = cls.parse_step_info(config)
        logger.info(f'Parsed information: {step}')
        return step

# 28-0315937bbdff - z dłuższym kablem

# jak podłączyć? komenda pinout -> czerwony na 5V, szary na GMD, niebieski na GPIO4
# https://tutorials-raspberrypi.com/raspberry-pi-temperature-sensor-1wire-ds18b20/
