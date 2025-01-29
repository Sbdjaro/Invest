from .instruments import get_figi_by_ticker
from tinkoff.invest import Client
from .settings import get_token
from .utils import handle_types

import pandas as pd


def get_bond_coupons(ticker, from_='2020-01-01', to_='2030-01-01'):
    figi = get_figi_by_ticker(ticker)
    with Client(get_token()) as client:
        coupons = client.instruments.get_bond_coupons(figi=figi, 
                                                      from_=pd.to_datetime(from_), 
                                                      to=pd.to_datetime(to_))
        res = pd.DataFrame()
        for num, cup in enumerate(coupons.events):
            data = {'dt': cup.coupon_date,
                   'coupon_number': cup.coupon_number,
                   'amt': cup.pay_one_bond,
                   'period_in_days': cup.coupon_period}
            data = handle_types(data, to_dt=True)
            data = pd.DataFrame.from_dict(data, orient='index').T
            res = pd.concat([res, data])
        return res
    

def get_bond_info(ticker):
    figi = get_figi_by_ticker(ticker)
    with Client(get_token()) as client:
        data = client.instruments.bond_by(id_type=1, id=figi)
        res = {'figi': data.instrument.figi,
            'ticker': data.instrument.ticker,
            'name': data.instrument.name,
            'placement_date': data.instrument.placement_date,
            'maturity_date': data.instrument.maturity_date,
            'nominal': data.instrument.nominal,
            'nkd': data.instrument.aci_value,
            'frequency': data.instrument.coupon_quantity_per_year,
            }
        res = handle_types(res, to_dt=True)
        return res