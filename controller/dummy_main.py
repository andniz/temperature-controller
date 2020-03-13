from utils import FermentationConfigParser, get_logger


logger = get_logger(__name__)


if __name__ == '__main__':
    logger.info('Started main')
    step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
    print(step)
