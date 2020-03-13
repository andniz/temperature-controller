import json
import os
from datetime import datetime

import pytz
from marshmallow.exceptions import MarshmallowError

from .config_schema import ConfigSchema
from .exceptions import FermentationConfigParserError


class FermentationConfigParser:
    @classmethod
    def get_file_content(cls, filename):
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
            return None
        steps = config['steps']
        for step in steps:
            step_end = step['end_datetime']
            if now <= step_end:
                return step
        return None

    @classmethod
    def get_step_info(cls, filename):
        content = cls.get_file_content(filename)
        try:
            config = cls.load_with_schema(content)
        except MarshmallowError:
            raise FermentationConfigParserError('Config file is improperly constructed')
        return cls.parse_step_info(config)

# 28-0315937bbdff - z dłuższym kablem

# jak podłączyć? komenda pinout -> czerwony na 5V, szary na GMD, niebieski na GPIO4
# https://tutorials-raspberrypi.com/raspberry-pi-temperature-sensor-1wire-ds18b20/
