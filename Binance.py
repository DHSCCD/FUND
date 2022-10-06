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



# 파일로부터 apiKey, Secret 읽기
with open("api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

# 창 불러오기
Window = uic.loadUiType("C:/Users/zzune/PycharmProjects/FUND/BINANCE.ui")[0]

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

class MyWindow(QMainWindow, Window):
    appender = pyqtSignal(str)
    timeout = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btc = binance.fetch_ticker("ETH/USDT")

        self.StartButton.clicked.connect(self.start_tast)
        self.BalanceButton.clicked.connect(self.mybalance)
        self.CoinAdd.clicked.connect(self.AddCoin)

        self.appender.connect(self.coin_append)

        self.timeout.connect(self.time2)      #시간 thread






    def AddCoin(self):
        coin = []

        a = self.CoinName.text()
        coin.append(a)
        print(coin)


        #for printCoin in coin:


        #    self.tableWidget.setItem(0,0, QTableWidgetItem(printCoin))





    def Trading(self):
        a = "Hello"
        # set.TradingRecord.setItem(0,0,QTableWidgetItem(str(a)))
        self.TradingRecord.setItem(0, 0, QTableWidgetItem("출력확인"))


    def mybalance(self):
        balance = binance.fetch_balance()
        balance_usdt=balance['USDT']
        free = balance_usdt['free']  #잔액
        used = balance_usdt['used']  #거래 잔액
        total = balance_usdt['total']  #총잔액
        self.Free.setText(f'{free}')
        self.Used.setText(f'{used}')
        self.Total.setText(f'{total}')

    def start_tast(self):
        self.thread1 = threading.Thread(target=self.run_test)
        self.thread1.start()

        self.thread2 = threading.Thread(target=self.time1)
        self.thread2.start()

        self.thread3 = threading.Thread(target=self.Trading)
        self.thread3.start()

        self.StartButton.setEnabled(False)

    def time1(self):

        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")

        print(type(today))
        self.timeout.emit(today)



        time.sleep(5)
        threading.Timer(5000, self.time1()).start()

    def time2(self, nowtime):
        print(f'{nowtime}')
        self.Time.setText(nowtime)




    def end_tast(self, end_str):
        print(f'{end_str}')
        self.startButton.setEnabled(True)


    def run_test(self):

        eth_ohlcv = binance.fetch_ohlcv("ETH/USDT",timeframe='30m', limit=241)
        df = pd.DataFrame(eth_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        # print(df)

        ma5 = df['close'].rolling(window=240).mean()
        self.appender.emit(f'{ma5[-1]}')

        time.sleep(5)

        threading.Timer(5000,self.run_test()).start()

    def coin_append(self, emit_str):
         self.monitor.append(emit_str)

         # time.sleep(5)

    print("문장 끝")


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
                                                                                                                        #선물
                                                                               #잔고조회


# # binance 객체 생성
# binance = ccxt.binance(config=
# {
#     'apiKey': api_key,
#     'secret': secret
# })

# # USDT의 잔고 조회
# balance = binance.fetch_balance()
# my_balance=balance['USDT']
























#                                                         #마켓 조회
# with open("../api.txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     secret  = lines[1].strip()
#
# binance = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': secret,
#     'enableRateLimit': True,
#     'options': {
#         'defaultType': 'future'
#     }
# })
#
# markets = binance.load_markets()   #load_markets 메서드를 통해 티커를 얻어온다.
# for m in markets:
#     print(m)





#                                                     #잔고조회 -선물
# with open("api.txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     secret = lines[1].strip()
#
# # binance 객체 생성
# binance = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': secret,
#     'enableRateLimit': True,
# })
#
# balance = binance.fetch_balance(params={"type": "future"})
# print(balance['USDT'])




#                                                 #현재가 조회-선물
# with open("../api.txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     secret  = lines[1].strip()
#
# binance = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': secret,
#     'enableRateLimit': True,
#     'options': {
#         'defaultType': 'future'
#     }
# })
#
# btc = binance.fetch_ticker("BTC/USDT")      #현재가 불러오는 메서드
# print(btc)




#                                                 #과거 데이터 -선물
# import ccxt
# import pprint
# import time
# import pandas as pd
#
# with open("../api.txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     secret  = lines[1].strip()
#
# binance = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': secret,
#     'enableRateLimit': True,
#     'options': {
#         'defaultType': 'future'
#     }
# })
#
# btc = binance.fetch_ohlcv(
#     symbol="BTC/USDT",
#     timeframe='1d',
#     since=None,
#     limit=10)
#
# df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)



















#                                                                                     호가조회
# exchange = ccxt.binance()
# orderbook = exchange.fetch_order_book('ETH/USDT')
# print(orderbook['asks'])
# print(orderbook['bids'])




#                                                                                분봉 데이터를 500개까지 얻을 수 있다.
# #바이낸스의 거래소 기준 시간은 UTC이므로 국내보다 9시간 느리다.
#             #분봉조회
# binance = ccxt.binance()
# btc_ohlcv = binance.fetch_ohlcv("BTC/USDT")
#
# df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)
#
#             #일봉조회
# binance = ccxt.binance()
# btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d')
#
# df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)
#
#             #특정 갯수 봉만 조회
# binance = ccxt.binance()
# btc_ohlcv = binance.fetch_ohlcv(symbol="BTC/USDT", timeframe='1d', limit=10)
#
# df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)












# binance = ccxt.binance()
# markets= binance.load_markets() #딕셔너리 형태로 리턴된다.


# #코인 종류 example) 'ETH/BTC
# binance = ccxt.binance()
# markets= binance.load_markets() #딕셔너리 형태로 리턴된다.
# print(markets.keys())
# print(len(markets))







#                                                                                              코인 정보 불러오기
# binance = ccxt.binance()
# markets= binance.load_markets() #딕셔너리 형태로 리턴된다.
# btc = binance.fetch_ticker("BTC/USDT")
# pprint.pprint(btc)
#
# # {'ask': 60613.1,
# #  'askVolume': 1.97582,
# #  'average': None,
# #  'baseVolume': 82442.606919,
# #  'bid': 60613.09,
# #  'bidVolume': 0.054132,
# #  'change': 3343.1,
# #  'close': 60613.09,
# #  'datetime': '2021-03-14T07:57:23.025Z',
# #  'high': 61844.0,
# #  'info': {'askPrice': '60613.10000000',
# #           'askQty': '1.97582000',
# #           'bidPrice': '60613.09000000',
# #           'bidQty': '0.05413200',
# #           'closeTime': 1615708643025,
# #           'count': 2503963,
# #           'firstId': 702386522,
# #           'highPrice': '61844.00000000',
# #           'lastId': 704890484,
# #           'lastPrice': '60613.09000000',
# #           'lastQty': '0.01905700',
# #           'lowPrice': '57126.20000000',
# #           'openPrice': '57269.99000000',
# #           'openTime': 1615622243025,
# #           'prevClosePrice': '57270.00000000',
# #           'priceChange': '3343.10000000',
# #           'priceChangePercent': '5.837',
# #           'quoteVolume': '4955222213.14148946',
# #           'symbol': 'BTCUSDT',
# #           'volume': '82442.60691900',
# #           'weightedAvgPrice': '60105.11310020'},
# #  'last': 60613.09,
# #  'low': 57126.2,
# #  'open': 57269.99,
# #  'percentage': 5.837,
# #  'previousClose': 57270.0,
# #  'quoteVolume': 4955222213.141489,
# #  'symbol': 'BTC/USDT',
# #  'timestamp': 1615708643025,




# ask	매도 1호가
# askVolume	매도 1호과 물량
# bid	매수 1호가
# bidVolume	매수 1호과 물량
# datetime	현재시간
# timestamp	타임 스탬프
# open	시가
# high	고가
# low	저가
# close	종가
# symbol	심볼

