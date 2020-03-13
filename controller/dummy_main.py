from dotenv import load_dotenv

from controller import FermentationTemperatureController
from utils import FermentationConfigParser, get_logger


logger = get_logger(__name__)


if __name__ == '__main__':
    load_dotenv()
    logger.info('Started main')
    controller = FermentationTemperatureController()
    air, wort = controller.read_current_temperatures()
    logger.info(f'Temps: {air=}, {wort=}')
    step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
    print(step)
