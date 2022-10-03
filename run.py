import datetime

import ccxt     #바이낸스
import pprint      #딕셔너리를 보기 좋게 출력하기 위한 모듈
import pandas as pd
import pandas as pd
import pyupbit
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import threading

with open("api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()


binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

coin = binance.fetch_ohlcv("BTC/USDT")

markets=binance.load_markets()
print(markets)