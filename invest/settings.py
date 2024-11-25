import os
from dotenv import load_dotenv

def config():
    ans = {
        'sql_path': 'sqlite:///db.db'
    }
    return ans

def get_token():
    load_dotenv()
    token = os.environ.get('TOKEN')
    return token
