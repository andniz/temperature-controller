import os
import re
from decimal import Decimal


THERMOMETER_PATH = '/sys/bus/w1/devices/{}/w1_slave'
DEV_THERMOMETER_PATH = 'tests/assets/thermometer_file.txt'


def read_temperature(thermometer_id: str = None) -> Decimal:
    environment = os.getenv('environment', 'development')
    if environment == 'production' and thermometer_id:
        filepath = THERMOMETER_PATH.format(thermometer_id)
    else:
        filepath = DEV_THERMOMETER_PATH
    with open(filepath, 'r') as f:
        content = f.read()
    temperature_string = re.findall('t=[0-9]*$', content)[0]
    return Decimal(temperature_string.split('=')[-1]) / 1000
