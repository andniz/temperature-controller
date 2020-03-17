import os
import re
from decimal import Decimal
from typing import Dict, Tuple, Union

from dotenv import load_dotenv

from temperature_controller.config_parser import FermentationConfigParser
from temperature_controller.constants import (
    Actions, CONFIG_FILE_ERROR_MESSAGE,
    CurrentTempStatus, HysteresisStatus, CONDITIONS_TO_ACTION, MIN_FRIDGE_TEMPERATURE
)
from temperature_controller.exceptions import FermentationConfigError
from temperature_controller.utils import get_logger, read_temperature
from pathlib import Path


logger = get_logger(__name__)


class FermentationTemperatureController:

    def get_config_filename(self) -> Path:
        data_path = Path('data')
        data_files = list(data_path.glob('fermentation_config_*.json'))
        if len(data_files) > 1:
            logger.error(CONFIG_FILE_ERROR_MESSAGE)
            raise FermentationConfigError(CONFIG_FILE_ERROR_MESSAGE)
        return data_files[0]

    def get_step_info(self, config_filename: Path) -> Union[Dict, None]:
        return FermentationConfigParser.get_step_info(config_filename)

    def read_current_action(self) -> str:
        # TODO: data needed to read this - from .env
        return Actions.NO_ACTION

    def read_current_temperatures(self) -> Tuple[Decimal, Decimal]:
        air_thermometer_id = os.getenv('air_thermometer_id')
        wort_thermometer_id = os.getenv('wort_thermometer_id')
        air_temperature = read_temperature(air_thermometer_id)
        wort_temperature = read_temperature(wort_thermometer_id)
        logger.info(f'Temperatures read: {air_temperature=}, {wort_temperature=}')
        return air_temperature, wort_temperature

    def get_needed_data(self):
        config_filename = self.get_config_filename()
        step_info = self.get_step_info(config_filename)
        current_action = self.read_current_action()
        current_temperatures = self.read_current_temperatures()
        return step_info, current_action, current_temperatures

    def determine_next_action(
            self, step_info: dict, current_action: str, current_temperatures: Tuple[Decimal, Decimal]
    ) -> str:
        air_temperature, wort_temperature = current_temperatures

        temp_status = (
            CurrentTempStatus.TOO_HOT
            if wort_temperature >= step_info['target_temperature']
            else CurrentTempStatus.TOO_COLD
        )
        logger.info(
            f'{temp_status=}, because {wort_temperature=}, and {step_info["target_temperature"]=}'
        )

        hysteresis_status = (
            HysteresisStatus.OUT_OF
            if abs(wort_temperature - step_info['target_temperature']) >= step_info['hysteresis']
            else HysteresisStatus.WITHIN
        )
        logger.info(
            f'{hysteresis_status=}, because {wort_temperature=}, {step_info["target_temperature"]=}'
            f', and {step_info["hysteresis"]=}'
        )

        conditions = f'{temp_status}-{hysteresis_status}-{current_action}'
        next_action = CONDITIONS_TO_ACTION[conditions]
        logger.info(f'Based on {conditions=}, chosen the next action as {next_action}')

        if next_action == Actions.COOLING and air_temperature <= MIN_FRIDGE_TEMPERATURE:
            next_action = Actions.NO_ACTION
            logger.info(f'{air_temperature=}, so {next_action=}')

        return next_action

    def make_action(self, action):
        pass

    def step(self):
        load_dotenv()
        step_info, current_action, current_temperatures = self.get_needed_data()
        action = self.determine_next_action(step_info, current_action, current_temperatures)
        self.make_action(action)

# TODO: wrap in try/excepts
