import os
from dotenv import load_dotenv
from tinkoff.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX 


def config():
    ans = {
        'sql_path': 'sqlite:///db.db'
    }
    return ans

def get_token():
    load_dotenv()
    token = os.environ.get('TOKEN')
    return token

def get_target():
    load_dotenv()
    mode = os.environ.get('MODE')
    print(mode)
    if mode == 'real':
        return INVEST_GRPC_API
    elif mode == 'sandbox':
        print(1)
        return INVEST_GRPC_API_SANDBOX
    else:
        return INVEST_GRPC_API