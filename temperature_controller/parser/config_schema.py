import os
from datetime import datetime, timedelta

import pytz
from marshmallow import Schema, fields, pre_load


class StepSchema(Schema):
    target_temperature = fields.Decimal(required=True, data_key='targetTemperature')
    end_datetime = fields.DateTime(required=False, data_key='endDatetime')


class ConfigSchema(Schema):
    id = fields.Integer(required=True, data_key='id')
    start_datetime = fields.DateTime(required=True, data_key='startDatetime')
    hysteresis = fields.Decimal(required=True, data_key='hysteresis')
    number_of_steps = fields.Integer(required=True, data_key='numberOfSteps')
    steps = fields.List(fields.Nested(StepSchema), required=True)

    @pre_load
    def allow_empty_end_datetime_in_last_step(self, data, **kwargs):
        if data['steps'][-1]['endDatetime'] == '':
            timezone = pytz.timezone(os.getenv('timezone', 'Europe/Warsaw'))
            end_datetime = timezone.localize(datetime.max - timedelta(days=1))
            data['steps'][-1]['endDatetime'] = end_datetime.isoformat()
        return data
