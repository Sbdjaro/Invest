from tinkoff.invest import CandleInterval, Client
import pandas as pd
from .settings import get_token, get_target
from .instruments import get_figi_by_ticker
from .candle import Candle

from tinkoff.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX 


def interval_transcription():
    transcription =  {
        '1m': CandleInterval.CANDLE_INTERVAL_1_MIN,
        '2m': CandleInterval.CANDLE_INTERVAL_2_MIN,
        '3m': CandleInterval.CANDLE_INTERVAL_3_MIN,
        '5m': CandleInterval.CANDLE_INTERVAL_5_MIN,
        '10m': CandleInterval.CANDLE_INTERVAL_10_MIN,
        '15m': CandleInterval.CANDLE_INTERVAL_15_MIN,
        '30m': CandleInterval.CANDLE_INTERVAL_30_MIN,
        '1h': CandleInterval.CANDLE_INTERVAL_HOUR,
        '2h': CandleInterval.CANDLE_INTERVAL_2_HOUR,
        '4h': CandleInterval.CANDLE_INTERVAL_4_HOUR,
        'day': CandleInterval.CANDLE_INTERVAL_DAY,
        'week': CandleInterval.CANDLE_INTERVAL_WEEK,
        'month': CandleInterval.CANDLE_INTERVAL_MONTH,
    }
    return transcription

def interval_to_t(interval):
    return interval_transcription()[interval]

def t_to_interval(interval):
    return {v: k for k, v in interval_transcription().items()}[interval]

def load_candles(tiker, interval, from_, to_):
    ans = pd.DataFrame()
    with Client(get_token(), target=get_target()) as client:
    #with Client('1', target=INVEST_GRPC_API_SANDBOX) as client:
        for candle in client.get_all_candles(
            figi=get_figi_by_ticker(tiker),
            from_=from_,
            to=to_,
            interval=interval_to_t(interval),
        ):
            candle = Candle.from_t_candle(candle, interval)
            ans = pd.concat([ans, candle.to_df()])
    ans['datetime'] = pd.to_datetime(ans['datetime'])
    return ans.reset_index(drop=True).sort_values('datetime')