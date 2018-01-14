import json
import datetime


def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def pretty_json(**kwargs):
    return json.dumps(kwargs, sort_keys=True, default=converter,
                      indent=4, separators=(',', ': '))
