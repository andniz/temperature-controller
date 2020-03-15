import os
import re
from decimal import Decimal

from temperature_controller.constants import NO_THERMOMETER_FILE_MESSAGE
from temperature_controller.exceptions import NoThermometerFileException
from temperature_controller.utils.logger import get_logger

THERMOMETER_PATH = '/sys/bus/w1/devices/{}/w1_slave'
DEV_THERMOMETER_PATH = 'tests/assets/thermometer_file.txt'


logger = get_logger(__name__)


def read_temperature(thermometer_id: str = None) -> Decimal:
    environment = os.getenv('environment', 'development')
    if environment == 'production' and thermometer_id:
        filepath = THERMOMETER_PATH.format(thermometer_id)
    else:
        filepath = DEV_THERMOMETER_PATH
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(NO_THERMOMETER_FILE_MESSAGE.format(filepath))
        raise NoThermometerFileException(NO_THERMOMETER_FILE_MESSAGE.format(filepath))
    temperature_string = re.findall('t=[0-9]*$', content)[0]
    return Decimal(temperature_string.split('=')[-1]) / 1000
