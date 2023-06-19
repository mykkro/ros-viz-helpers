import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
    


def maketimestamp():
    dt = datetime.now()
    return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")


def reformat_date(dt, from_format, to_format):
    d = datetime.strptime(dt, from_format)
    return datetime.strftime(d, to_format)