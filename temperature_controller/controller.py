import os
import re
from typing import Union

from dotenv import load_dotenv

from temperature_controller.constants import ActionTypes

from temperature_controller.utils import get_logger, read_temperature
from temperature_controller.config_parser import FermentationConfigParser


logger = get_logger(__name__)


class FermentationConfigError(Exception):
    pass


class FermentationTemperatureController:
    config_filename_pattern = r'^fermentation_config_[0-9]*.json$'

    def get_config_filename(self):
        data_files = os.listdir('data')
        if len(data_files) > 0:
            raise FermentationConfigError('Too many config files')
        if not re.match(self.config_filename_pattern, data_files[0]):
            raise FermentationConfigError('File is not properly named')
        return data_files[0]

    def get_step_info(self, config_filename: str) -> Union[dict, type(None)]:
        return FermentationConfigParser.get_step_info(config_filename)

    def read_actors_state(self):
        # TODO: data needed to read this - from .env
        pass

    def read_current_temperatures(self):
        air_thermometer_id = os.getenv('air_thermometer_id')
        wort_thermometer_id = os.getenv('wort_thermometer_id')
        air_temperature = read_temperature(air_thermometer_id)
        wort_temperature = read_temperature(wort_thermometer_id)
        logger.info(f'Temperatures read: {air_temperature=}, {wort_temperature=}')
        return air_temperature, wort_temperature

    def get_needed_data(self):
        config_filename = self.get_config_filename()
        step_info = self.get_step_info(config_filename)
        actors_state = self.read_actors_state()
        current_temperatures = self.read_current_temperatures()
        return step_info, actors_state, current_temperatures

    def determine_next_action(self, step_info, actors_state, current_temperature):
        return ActionTypes.COOLING

    def make_action(self, action):
        pass

    def step(self):
        load_dotenv()
        step_info, actors_state, current_temperatures = self.get_needed_data()
        action = self.determine_next_action(step_info, actors_state, current_temperatures)
        self.make_action(action)

# TODO: wrap in try/excepts
