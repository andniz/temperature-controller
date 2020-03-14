from dotenv import load_dotenv

from controller import FermentationTemperatureController
from parser.fermentation_config_parser import FermentationConfigParser
from utils.logger import get_logger


if __name__ == '__main__':
    load_dotenv()
    logger = get_logger(__name__)
    logger.info('Started main')
    controller = FermentationTemperatureController()
    air, wort = controller.read_current_temperatures()
    logger.info(f'Temps: {air=}, {wort=}')
    step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
    print(step)
