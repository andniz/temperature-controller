from dotenv import load_dotenv

from temperature_controller import FermentationTemperatureController
from temperature_controller.config_parser import FermentationConfigParser
from temperature_controller.utils import get_logger


if __name__ == '__main__':
    load_dotenv()
    logger = get_logger(__name__)
    logger.info('Started main')
    controller = FermentationTemperatureController()
    air, wort = controller.read_current_temperatures()
    logger.info(f'Temps: {air=}, {wort=}')
    step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
    print(step)



# jak podłączyć? komenda pinout -> czerwony na 5V, szary na GMD, niebieski na GPIO4
# https://tutorials-raspberrypi.com/raspberry-pi-temperature-sensor-1wire-ds18b20/
