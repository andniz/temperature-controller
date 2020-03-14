from decimal import Decimal

from temperature_controller import read_temperature


class TestReadTemperature:
    temperature = read_temperature()
    assert temperature == Decimal('20.375')