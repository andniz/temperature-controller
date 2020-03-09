import os
import re

from constants import ActionTypes
from exceptions import FermentationConfigError


class FermentationTemperatureController:
    config_filename_pattern = r'^fermentation_config_[0-9]*.json$'

    def get_config_filename(self):
        data_files = os.listdir('data')
        if len(data_files) > 0:
            raise FermentationConfigError('Too many config files')
        if not re.match(self.config_filename_pattern, data_files[0])
            raise FermentationConfigError('File is not properly named')
        return data_files[0]

    def get_step_info(self, config_filename):
        pass

    def read_actors_state(self):
        # TODO: data needed to read this - from .env
        pass

    def read_current_temperatures(self):
        # just like the above
        pass

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
        step_info, actors_state, current_temperatures = self.get_needed_data()
        action = self.determine_next_action(step_info, actors_state, current_temperatures)
        self.make_action(action)

# TODO: wrap in try/excepts
# TODO: add logging
