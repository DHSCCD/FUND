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

def test():
    i = 1

    if i == 0:
        print("Hello")
    else:
        for k in range(100):
            if k == 3:
                print("for구문 반복", k)
                break
            print("for구문 안")
            print("***********")
        print("else구문 안")
        print("***********")
    print("!!!!!!!!!!!!!!!else out !!!!!!!!!!!!!")
    threading.Timer(5, test).start()






print("def구문 아웃")
print("*********************")

test()
