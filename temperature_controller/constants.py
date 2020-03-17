from decimal import Decimal


class Actions:
    COOLING = 'cooling'
    NO_ACTION = 'no_action'
    HEATING = 'heating'


class CurrentTempStatus:
    TOO_HOT = 'too_hot'
    TOO_COLD = 'too_cold'


class HysteresisStatus:
    WITHIN = 'within'
    OUT_OF = 'out_of'


NO_CONFIG_MESSAGE = 'Config file not found at given location'
CONFIG_NOT_JSON_MESSAGE = 'Config file is not valid JSON'
CONFIG_FILE_ERROR_MESSAGE = 'There should be only one config file, named fermentation_config_<id>.json'
NO_THERMOMETER_FILE_MESSAGE = 'Could not find thermometer file under path {}'


CONDITIONS_TO_ACTION = {
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.WITHIN}-{Actions.HEATING}':    Actions.NO_ACTION,
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.WITHIN}-{Actions.NO_ACTION}':  Actions.NO_ACTION,
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.WITHIN}-{Actions.COOLING}':    Actions.COOLING,
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.OUT_OF}-{Actions.HEATING}':    Actions.COOLING,
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.OUT_OF}-{Actions.NO_ACTION}':  Actions.COOLING,
    f'{CurrentTempStatus.TOO_HOT}-{HysteresisStatus.OUT_OF}-{Actions.COOLING}':    Actions.COOLING,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.WITHIN}-{Actions.HEATING}':   Actions.HEATING,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.WITHIN}-{Actions.NO_ACTION}': Actions.NO_ACTION,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.WITHIN}-{Actions.COOLING}':   Actions.NO_ACTION,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.OUT_OF}-{Actions.HEATING}':   Actions.HEATING,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.OUT_OF}-{Actions.NO_ACTION}': Actions.HEATING,
    f'{CurrentTempStatus.TOO_COLD}-{HysteresisStatus.OUT_OF}-{Actions.COOLING}':   Actions.HEATING
}

MIN_FRIDGE_TEMPERATURE = Decimal('6.0')
