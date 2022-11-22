import pprint
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



markets = binance.load_markets()
symbol = "ETH/USDT"
market = binance.market(symbol)
leverage = 5
#레버리지 설정
resp = binance.fapiPrivate_post_leverage\
        ({
            'symbol': market['id'],
            'leverage': leverage
        })




order = binance.create_market_buy_order(
    symbol=symbol,
    amount=0.001
)#티커, 수량, 가격
order = binance.create_market_sell_order(
    symbol="BTC/USDT",
    amount=0.001
)

order = binance.create_market_sell_order(
    symbol="BTC/USDT",
    amount=0.001,
)
order = binance.create_market_buy_order(
    symbol="BTC/USDT",
    amount=0.001,
)























# #binance = ccxt.binance()
# #ohlcvs = binance.fetch_ohlcv('BTC/USDT', timeframe="1h", limit=1000)
# #pprint.pprint(ohlcvs)
# #count = 1
# #print("------------------------------")
# #for ohlc in ohlcvs:
# #    print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'), ohlc[1], ohlc[2], ohlc[3], "종가--", ohlc[4], "--", ohlc[5])
# #    count +=1
# #    #일자, 시가, 고가, 저가, 종가, 거래량
# #print("확인하기: ", type(ohlc))
# #ma5 = ohlc[5].rolling(window=5).mean()
#
#
# markets = binance.fetch_tickers()
# coin = markets.keys()
# coin_usdt = [s for s in coin if 'USDT' in s]
# coin_usdt_500 = []
# count = 0
# for i in coin_usdt:
#     close = binance.fetch_ticker(i)
#     if close['close']>10:
#         coin_usdt_500.append(close['symbol'])
#         count +=1
#
# # markets = binance.fetch_ticker
#
# while True:
#     for kk in coin_usdt_500:
#         # z-score (총합 - 평균)/표준편차
#         pole_count = 14
#         eth_ohlcv = binance.fetch_ohlcv(kk, timeframe='15m', limit=pole_count + 1)
#         df = pd.DataFrame(eth_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#         df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#         df.set_index('datetime', inplace=True)
#
#         ma5av = df['close'].rolling(window=pole_count).mean()  # 평균
#         av_list = ma5av.values.tolist()
#         ma5st = df['close'].rolling(window=pole_count).std()  # 표준편차
#         st_list = ma5st.values.tolist()
#
#         test = []
#         coin_close = [i[4] for i in eth_ohlcv]  # 마감값
#         score = [0] * len(coin_close)
#         num = 0
#
#         for i in range(len(coin_close)):
#             if st_list[i]!=0:
#                 score[i] = (coin_close[i] - av_list[i]) / st_list[i]
#                 num += 1
#             else:
#                 st_list[i] = "Zero"
#
#
#         # RCI 3lines
#         # RCI = [ 1 - 6*d / ( n * (n^2-1) ) ] * 100
#         pole_count = [9, 13, 18]
#         pole_result_15m =[0]*3
#         pole_result_30m =[0]*3
#         pole_result_1h =[0]*3
#
#         time = ['15m', '30m', '1h']
#         for t in time:
#             count_result = 0
#             for pole in pole_count:
#                 eth_ohlcv_RCI14 = binance.fetch_ohlcv(kk, timeframe=t, limit=pole)
#                 coin_close_RCI14 = [i[4] for i in eth_ohlcv_RCI14]  # 마감값
#
#                 high = sorted(coin_close_RCI14, reverse=True)  # 내림차순 큰수에서 작은수
#
#                 grade_date = [0] * pole
#                 grade_close = []
#
#                 # 1. 날짜순위
#                 for i in range(1, pole + 1):
#                     grade_date[i - 1] = i
#                 grade_date.reverse()
#
#                 # 2. 점수순위
#                 for i in high:
#                     grade_close.append(coin_close_RCI14.index(i) + 1)  # 클수록 등수가 1에 수렴한다.
#                 k = 0
#                 for i in grade_close:
#                     grade_close[k] = pole + 1 - grade_close[k]
#                     k += 1
#
#
#
#                 d = 0
#                 for x, y in zip(grade_date, grade_close):
#                     d += abs(x - y) ** 2
#
#                 rci_result = -(1 - 6 * (d) / (pole * (pole ** 2 - 1))) * 100
#
#                 if t == '15m':
#                     pole_result_15m[count_result] = rci_result
#                     count_result +=1
#
#                 elif t == '30m':
#                     pole_result_30m[count_result] = rci_result
#                     count_result += 1
#
#
#                 elif t == '1h':
#                     pole_result_1h[count_result] = rci_result
#                     count_result += 1
#
#
#         if pole_result_15m[0]>70 and pole_result_15m[1]>50 and pole_result_15m[2]>50 and score[-1]>1.2 and\
#                 pole_result_30m[0] > 70 and pole_result_30m[1] > 50 and pole_result_30m[2] > 50 and score[-1] > 1.2 and\
#                         pole_result_1h[0] > 70 and pole_result_1h[1] > 70 and pole_result_1h[2] > 70 and score[-1] > 1.2:
#             coin_usdt_500.remove(kk)
#             print("Please short ,,,", kk)
#             print(coin_usdt_500)
#
#         elif pole_result_15m[0]<-70 and pole_result_15m[1]<-50 and pole_result_15m[2]<-50 and score[-1]<-1.2 and\
#                 pole_result_30m[0] <-70 and pole_result_30m[1] < -50 and pole_result_30m[2] < -50 and score[-1] <-1.2 and\
#                         pole_result_1h[0] <-70 and pole_result_1h[1] < -70 and pole_result_1h[2] < -70 and score[-1] <-1.2:
#             coin_usdt_500.remove(kk)
#             print("Please long ,,,", kk)
#             print(coin_usdt_500)
#
#         elif pole_result_15m[0]>90 and pole_result_15m[1]>50 and pole_result_15m[2]>50 and score[-1]>1.2 and\
#                 pole_result_30m[0] >90 and pole_result_30m[1] > 50 and pole_result_30m[2] > 50 and score[-1] > 1.2 and\
#                         pole_result_1h[0] > 70 and pole_result_1h[1] > 70 and pole_result_1h[2] > 70 and score[-1] > 1.2:
#             coin_usdt_500.remove(kk)
#             print("**********You have to a  short**********  ", kk)
#             print(coin_usdt_500)
#
#         elif pole_result_15m[0]<-90 and pole_result_15m[1]<-50 and pole_result_15m[2]<-50 and score[-1]<-1.2 and\
#                 pole_result_30m[0] <-90 and pole_result_30m[1] < -50 and pole_result_30m[2] < -50 and score[-1] <-1.2 and\
#                         pole_result_1h[0] <-70 and pole_result_1h[1] < -50 and pole_result_1h[2] < -50 and score[-1] <-1.2:
#             coin_usdt_500.remove(kk)
#             print("**********You have a long**********  ", kk)
#             print(coin_usdt_500)
#
#         else:
#             print("Nothing")

#
#
#
#
#
#
#
#
#
#
#
#
#
#     print("---------------------------------------------")













#print("--------------------------------------------")
#eth_ohlcv = binance.fetch_ohlcv("BTC/USDT", timeframe='1h', limit=20)
#df = pd.DataFrame(eth_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#df.set_index('datetime', inplace=True)
#
#ma5 = df['close'].rolling(window=20).mean()
#print("------------------------------------------------------")
#
#
#ma55 = 2*df['close'].rolling(window=20).std()
#bol_upper = ma5 + 2*df['close'].rolling(window=20).std()
#bol_down =  ma5 - 2*df['close'].rolling(window=20).std()
#
#btc = binance.fetch_ticker('BTC/USDT')
#btc_now = btc['last']
#
###불린저 밴드
##while True:
##    if bol_upper[-1]*0.998 == btc_now:
##        print("short - leverage5")
##
##    elif bol_down[-1]*1.002 == btc_now:
##        print("long - leverage5")
#print("--------------------------------------------")








