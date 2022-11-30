import json
import pprint
import threading
import json
import ccxt
from PyQt5 import uic
import pandas as pd
from datetime import datetime
import time
import ccxt

with open("C:/Users/zzune/PycharmProjects/FUND/api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()
Window = uic.loadUiType("C:/Users/zzune/PycharmProjects/FUND/BINANCE.ui")[0]
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
