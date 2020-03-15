from decimal import Decimal

from temperature_controller.utils import read_temperature


class TestReadTemperature:
    def test_read_temperature(self):
        temperature = read_temperature()
        assert temperature == Decimal('20.375')
