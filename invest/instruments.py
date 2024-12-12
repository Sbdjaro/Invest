from tinkoff.invest import Client
from .settings import get_token, get_target
from .sql import has_table, get_connetion, to_sql
import pandas as pd

def get_dataframe_of_instruments():
    """Получаем таблицу соответствия figi, тикера и названия инструмента"""
    l=[]
    with Client(get_token(), target=get_target()) as client:
        instruments = client.instruments
        market_data = client.market_data
        for method in ['shares', 'bonds', 'etfs', 'currencies', 'futures']:
            len_ = len(l)
            print(f'Получения инструментов {method}...', end='\n')
            for item in getattr(instruments, method)().instruments:
                l.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })
            print(f'\tБыло получено {len(l) - len_} инструментов.')
        l = pd.DataFrame(l)
    
    return l

def get_sql_instruments(engine=get_connetion(), force=False):
    if force or not has_table('instruments', engine):
        df = get_dataframe_of_instruments()
        to_sql('instruments', df, engine)
    else:
        df = pd.read_sql_table('instruments', con=engine)
    return df

def get_figi_by_ticker(ticker, engine=get_connetion()):
    df = get_sql_instruments(engine)
    return df[df['ticker'] == ticker]['figi'].iloc[0]

def get_ticker_by_figi(figi, engine=get_connetion()):
    df = get_sql_instruments(engine)
    return df[df['figi'] == figi]['ticker'].iloc[0]