import sys
from unittest.mock import Mock, patch

import pytest

sys.modules['RPi.GPIO'] = Mock()
from temperature_controller.constants import Actions
from temperature_controller.output import OutputController


class TestOutputController:
    # in read_output we check heating first
    @pytest.fixture
    def mock_gpio(self):
        with patch('temperature_controller.output.output.GPIO') as mock:
            mock.set_output = Mock()
            yield mock

    @pytest.fixture
    def output(self):
        output = OutputController()
        output.heating_channel = 8
        output.cooling_channel = 13
        yield output

    def test_reads_heating(self, mock_gpio, output):
        mock_gpio.input.side_effect = [True, False]
        assert output.read_output() == Actions.HEATING

    def test_reads_cooling(self, mock_gpio, output):
        mock_gpio.input.side_effect = [False, True]
        assert output.read_output() == Actions.COOLING

    def test_reads_no_action(self, mock_gpio, output):
        mock_gpio.input.side_effect = [False, False]
        assert output.read_output() == Actions.NO_ACTION

    def test_raises_error_with_both_actors_on(self, mock_gpio, output):
        mock_gpio.input.side_effect = [True, True]
        with pytest.raises(ValueError):
            output.read_output()
            output.set_output.assert_called_with(Actions.NO_ACTION)

    def test_set_heating(self, mock_gpio, output):
        output.set_output(Actions.HEATING)
        mock_gpio.output.assert_any_call(output.heating_channel, True)
        mock_gpio.output.assert_any_call(output.cooling_channel, False)

    def test_set_cooling(self, mock_gpio, output):
        output.set_output(Actions.COOLING)
        mock_gpio.output.assert_any_call(output.heating_channel, False)
        mock_gpio.output.assert_any_call(output.cooling_channel, True)

    def test_set_no_action(self, mock_gpio, output):
        output.set_output(Actions.NO_ACTION)
        mock_gpio.output.assert_any_call(output.heating_channel, False)
        mock_gpio.output.assert_any_call(output.cooling_channel, False)
