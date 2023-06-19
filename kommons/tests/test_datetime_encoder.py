from kommons.datetime import DateTimeEncoder
import pytest
import datetime
import json


def test_datetime_encoder():
    dt = "2023-04-05"
    dtt = datetime.datetime.strptime(dt, "%Y-%m-%d")
    obj = dict(date=dtt)
    obj_str = json.dumps(obj, cls=DateTimeEncoder)
    assert(obj_str == '{"date": "2023-04-05T00:00:00"}')
