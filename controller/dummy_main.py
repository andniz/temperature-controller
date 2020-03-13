from utils import FermentationConfigParser

if __name__ == '__main__':
    step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
    print(step)
