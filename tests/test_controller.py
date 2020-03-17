from decimal import Decimal

from temperature_controller.constants import Actions
from temperature_controller.controller import FermentationTemperatureController

DUMMY_STEP_INFO = {
    'target_temperature': Decimal('17.0'),
    'hysteresis': Decimal('0.5')
}


class TestFermentationTemperatureController:
    def test_determine_next_action(self):
        current_action = Actions.NO_ACTION
        current_temperatures = (Decimal('19.0'), Decimal('20.0'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.COOLING

    def test_no_cooling_when_low_air_temp(self):
        current_action = Actions.NO_ACTION
        current_temperatures = (Decimal('5.0'), Decimal('28.0'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.NO_ACTION

    def test_cools_right_on_hysteresis(self):
        current_action = Actions.NO_ACTION
        current_temperatures = (Decimal('16.0'), Decimal('17.5'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.COOLING

    def test_heats_right_on_hysteresis(self):
        current_action = Actions.NO_ACTION
        current_temperatures = (Decimal('16.0'), Decimal('16.5'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.HEATING

    def test_stops_heating_on_target(self):
        current_action = Actions.HEATING
        current_temperatures = (Decimal('22.0'), Decimal('17.0'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.NO_ACTION

    def test_doesnt_stop_cooling_on_target(self):
        current_action = Actions.COOLING
        current_temperatures = (Decimal('13.0'), Decimal('17.0'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.COOLING

    def test_stops_cooling_below_target(self):
        current_action = Actions.COOLING
        current_temperatures = (Decimal('13.0'), Decimal('16.9375'))
        controller = FermentationTemperatureController()
        next_action = controller.determine_next_action(
            DUMMY_STEP_INFO, current_action, current_temperatures
        )
        assert next_action == Actions.NO_ACTION
