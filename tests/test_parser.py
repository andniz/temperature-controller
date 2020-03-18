import json
from decimal import Decimal
from pathlib import Path

import pytest
from freezegun import freeze_time

from temperature_controller.config_parser import FermentationConfigParserError, FermentationConfigParser


class TestParserGetFileContent:
    def test_no_file(self):
        with pytest.raises(
                FermentationConfigParserError,
                match=r'^Config file not found at given location$'
        ):
            FermentationConfigParser.get_file_content('tests/assets/dummy_thicc_config.json')

    def test_invalid_file(self):
        with pytest.raises(
                FermentationConfigParserError,
                match=r'^Config file is not valid JSON$'
        ):
            FermentationConfigParser.get_file_content('tests/assets/invalid_json.json')

    def test_valid_file(self):
        content = FermentationConfigParser.get_file_content('tests/assets/dummy_config.json')
        assert content['id'] == 2137


class TestParserParseStep:
    @pytest.fixture
    def config(self):
        with open(Path('tests/assets/dummy_config.json'), 'r') as f:
            return FermentationConfigParser.load_with_schema(json.load(f))

    @freeze_time('2020-03-12')
    def test_first_step(self, config):
        step = FermentationConfigParser.parse_step_info(config)
        assert step['target_temperature'] == Decimal('17.0')
        assert step['hysteresis'] == Decimal('0.5')

    @freeze_time('2020-03-21')
    def test_step_in_the_middle(self, config):
        step = FermentationConfigParser.parse_step_info(config)
        assert step['target_temperature'] == Decimal('24.0')
        assert step['hysteresis'] == Decimal('0.5')

    @freeze_time('2020-05-20')
    def test_step_without_end_date(self, config):
        step = FermentationConfigParser.parse_step_info(config)
        assert step['target_temperature'] == Decimal('6.0')
        assert step['hysteresis'] == Decimal('0.5')

    @freeze_time('2020-02-12')
    def test_too_early(self, config):
        step = FermentationConfigParser.parse_step_info(config)
        assert step is None

    @freeze_time('2020-04-20')
    def test_all_steps_finished(self):
        with open(Path('tests/assets/dummy_config_with_end_datetime.json'), 'r') as f:
            config = FermentationConfigParser.load_with_schema(json.load(f))
        step = FermentationConfigParser.parse_step_info(config)
        assert step is None


class TestParserE2E:
    @freeze_time('2020-03-21')
    def test_end_to_end(self):
        step = FermentationConfigParser.get_step_info('tests/assets/dummy_config.json')
        assert step['target_temperature'] == Decimal('24.0')
        assert step['hysteresis'] == Decimal('0.5')
