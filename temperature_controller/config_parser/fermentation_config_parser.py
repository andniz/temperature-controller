import json
import os
from datetime import datetime
from pathlib import Path
from typing import Union

import pytz
from marshmallow.exceptions import MarshmallowError

from temperature_controller.config_parser.config_schema import ConfigSchema
from temperature_controller.constants import CONFIG_NOT_JSON_MESSAGE, NO_CONFIG_MESSAGE
from temperature_controller.exceptions import FermentationConfigParserError
from temperature_controller.utils import get_logger


logger = get_logger(__name__)


class FermentationConfigParser:
    @classmethod
    def get_file_content(cls, filename: Path) -> dict:
        try:
            # noinspection PyTypeChecker
            with open(filename, 'r') as f:
                content = json.load(f)
        except FileNotFoundError:
            logger.error(NO_CONFIG_MESSAGE)
            raise FermentationConfigParserError(NO_CONFIG_MESSAGE)
        except json.decoder.JSONDecodeError:
            logger.error(CONFIG_NOT_JSON_MESSAGE)
            raise FermentationConfigParserError(CONFIG_NOT_JSON_MESSAGE)
        return content

    @classmethod
    def load_with_schema(cls, json_content: dict) -> dict:
        schema = ConfigSchema()
        return schema.load(json_content)

    @classmethod
    def parse_step_info(cls, config: dict) -> Union[dict, type(None)]:
        timezone_name = os.getenv('timezone', 'Europe/Warsaw')
        now = datetime.now(tz=pytz.timezone(timezone_name))
        if now < config['start_datetime']:
            logger.info("Scheduled fermentation hasn't begun")
            return None
        steps = config['steps']
        for step in steps:
            step_end = step['end_datetime']
            if now <= step_end:
                step['hysteresis'] = config['hysteresis']
                return step
        logger.info('Scheduled fermentation has finished')
        return None

    @classmethod
    def get_step_info(cls, filepath: Path) -> Union[dict, type(None)]:
        logger.info(f'Parser received a request to parse file {filepath}')
        content = cls.get_file_content(filepath)
        try:
            config = cls.load_with_schema(content)
        except MarshmallowError:
            logger.critical('Improperly constructed config file')
            raise FermentationConfigParserError('Config file is improperly constructed')
        step = cls.parse_step_info(config)
        logger.info(f'Parsed information: {step}')
        return step
