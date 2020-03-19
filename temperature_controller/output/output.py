import os

import RPi.GPIO as GPIO
from dotenv import load_dotenv

from temperature_controller.constants import Actions


class OutputController:
    def __init__(self):
        load_dotenv()
        self.heating_channel = os.getenv('heating')
        self.cooling_channel = os.getenv('cooling')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.heating_channel, GPIO.out)
        GPIO.setup(self.cooling_channel, GPIO.out)

    def read_output(self) -> str:
        is_heating = GPIO.input(self.heating_channel)
        is_cooling = GPIO.input(self.cooling_channel)
        if is_heating and is_cooling:
            self.set_output(Actions.NO_ACTION)
            raise ValueError('Both actors on - shutting down')
        if is_cooling:
            return Actions.COOLING
        if is_heating:
            return Actions.HEATING
        return Actions.NO_ACTION

    def set_output(self, action: str):
        set_heating = action == Actions.HEATING
        set_cooling = action == Actions.COOLING
        GPIO.output(self.heating_channel, set_heating)
        GPIO.output(self.cooling_channel, set_cooling)
