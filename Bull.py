import pyupbit
import pandas as pd

BTC = pyupbit.get_ohlcv('KRW-BTC', interval="day",count=39)
pd.set_option('display.float_format' ,lambda x: f'{x:.2df}')
#불린저 밴더 = 20일 이평선 - (20일 표준편차*곱)

#1. 20일 이평선
BTC['BTC_20'] = BTC['close'].rolling(20).mean()

#2. 20일 표준편차
BTC['BTC__20'] = BTC['close'].rolling(20).std()

#3. 볼린저밴드 20일 기준
print(BTC['BTC_20'])


