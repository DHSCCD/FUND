import pyupbit
import pandas as pd

# BTC = pyupbit.get_ohlcv('KRW-BTC')
# pd.set_option('display.float_format', lambda x: '%.2f' % x)
#
# #불린저 밴더 = 20일 이평선 - (20일 표준편차*곱)
#
# #1. 20일 이평선
# BTC['20일_이평선'] = BTC['close'].rolling(20).mean()
#
# #2. 20일 표준편차
# BTC['표준편차']= BTC['close'].rolling(20).std()
#
# #3. 볼린저밴드 20일 기준
# BTC['볼린저밴드_하한가'] = BTC['20일_이평선'] - 2*BTC['표준편차']
# print(BTC)
# print(BTC['20일_이평선'])

BTC = pyupbit.get_ohlcv('KRW-BTC')


av_20 = BTC['close'].rolling(20).mean()

av__20= BTC['close'].rolling(20).std()

final = av_20 - 2*av__20

print(final)

