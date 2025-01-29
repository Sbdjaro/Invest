import datetime

import pandas as pd
from tinkoff.invest import MoneyValue


def handle_types(dict_, to_dt=False):
    for k, v in dict_.items():
        if isinstance(v, datetime.datetime):
            v = pd.to_datetime(v.isoformat())
            if to_dt:
                v = v.date()
        elif isinstance(v, MoneyValue):
            v = v.units + v.nano / 1e9
        dict_[k] = v
    return dict_