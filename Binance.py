import datetime
import pprint
import ccxt
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import threading

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

class MyWindow(QMainWindow, Window):
    appender = pyqtSignal(str)
    timeout = pyqtSignal(str)
    TableCoin = pyqtSignal(str)
    rci_result = pyqtSignal(str)
    account_count = 0
    coin = []
    # markets = binance.fetch_tickers()
    # coin = markets.keys()
    # coin_usdt = [s for s in coin if 'USDT' in s]
    # coin_usdt_500 = []
    # count = 0
    # for i in coin_usdt:
    #     close = binance.fetch_ticker(i)
    #     if close['close'] > 10:
    #         coin_usdt_500.append(close['symbol'])
    #         count += 1
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.StartButton.clicked.connect(self.start_tast)
        #self.BalanceButton.clicked.connect(self.mybalance)
        self.CoinAdd.clicked.connect(self.AddCoin)
        self.DeleteButton.clicked.connect(self.DeleteCoin)
        self.appender.connect(self.coin_append)
        self.timeout.connect(self.time2)      #시간 thread
        self.TableCoin.connect(self.ReAddCoin)
        self.rci_result.connect(self.rci_append)
    def start_tast(self):
        self.thread1 = threading.Thread(target=self.MovingAverage)
        self.thread1.start()

        self.thread2 = threading.Thread(target=self.time1)
        self.thread2.start()

        self.thread3 = threading.Thread(target=self.Trading)
        self.thread3.start()

        self.thread5 = threading.Thread(target=self.mybalance())
        self.thread5.start()

        self.thread6 = threading.Thread(target=self.buycoin())
        self.thread6.start()

        self.thread7 = threading.Thread(target=self.rci_3lines())
        self.thread7.start()

        self.StartButton.setEnabled(False)
    def coin_append(self, emit_str):
        self.monitor1.append(emit_str)
    def buycoin(self):
        # order = binance.create_market_buy_order(symbol="BTC/USDT", amount=0.001)
        print("확인용")
    def MovingAverage(self):
        print("test1")
        if len(self.coin)==0:
            print("test2")
            self.appender.emit("Please Add Coin")

        elif len(self.coin)!=0:
            print("test3")
            for a in self.coin:
                eth_ohlcv = binance.fetch_ohlcv(a, timeframe='1d', limit=5)
                df = pd.DataFrame(eth_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                df.set_index('datetime', inplace=True)

                ma5 = df['close'].rolling(window=5).mean()

                Price = binance.fetch_ticker(a)
                NowPrice = Price['close']

                if ma5[-1]==NowPrice:
                    self.appender.emit(a)
                    time.sleep(5)

                else:
                    self.appender.emit("Searching Again")
        threading.Timer(600, self.MovingAverage).start()
    def rci_3lines(self):
        if len(self.coin)==0:
            self.rci_result.emit("Please Add Coin")
        else:
            for kk in self.coin:
                # z-score (총합 - 평균)/표준편차
                pole_count = 14
                eth_ohlcv = binance.fetch_ohlcv(kk, timeframe='15m', limit=pole_count + 1)
                df = pd.DataFrame(eth_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                df.set_index('datetime', inplace=True)

                ma5av = df['close'].rolling(window=pole_count).mean()  # 평균
                av_list = ma5av.values.tolist()
                ma5st = df['close'].rolling(window=pole_count).std()  # 표준편차
                st_list = ma5st.values.tolist()

                test = []
                coin_close = [i[4] for i in eth_ohlcv]  # 마감값
                score = [0] * len(coin_close)
                num = 0

                for i in range(len(coin_close)):
                    if st_list[i] != 0:
                        score[i] = (coin_close[i] - av_list[i]) / st_list[i]
                        num += 1
                    else:
                        st_list[i] = "Zero"

                # RCI 3lines
                # RCI = [ 1 - 6*d / ( n * (n^2-1) ) ] * 100
                pole_count = [9, 13, 18]
                pole_result_15m = [0] * 3
                pole_result_30m = [0] * 3
                pole_result_1h = [0] * 3

                time = ['15m', '30m', '1h']

                for t in time:
                    count_result = 0
                    for pole in pole_count:
                        eth_ohlcv_RCI14 = binance.fetch_ohlcv(kk, timeframe=t, limit=pole)
                        coin_close_RCI14 = [i[4] for i in eth_ohlcv_RCI14]  # 마감값

                        high = sorted(coin_close_RCI14, reverse=True)  # 내림차순 큰수에서 작은수

                        grade_date = [0] * pole
                        grade_close = []

                        # 1. 날짜순위
                        for i in range(1, pole + 1):
                            grade_date[i - 1] = i
                        grade_date.reverse()

                        # 2. 점수순위
                        for i in high:
                            grade_close.append(coin_close_RCI14.index(i) + 1)  # 클수록 등수가 1에 수렴한다.
                        k = 0
                        for i in grade_close:
                            grade_close[k] = pole + 1 - grade_close[k]
                            k += 1

                        d = 0
                        for x, y in zip(grade_date, grade_close):
                            d += abs(x - y) ** 2

                        rci_result = -(1 - 6 * (d) / (pole * (pole ** 2 - 1))) * 100

                        if t == '15m':
                            pole_result_15m[count_result] = rci_result
                            count_result += 1

                        elif t == '30m':
                            pole_result_30m[count_result] = rci_result
                            count_result += 1


                        elif t == '1h':
                            pole_result_1h[count_result] = rci_result
                            count_result += 1

                if pole_result_15m[0]>70 and pole_result_15m[1]>50 and pole_result_15m[2]>50 and score[-1]>1.2 and\
                        pole_result_30m[0] > 70 and pole_result_30m[1] > 50 and pole_result_30m[2] > 50 and score[-1] > 1.2 and\
                                pole_result_1h[0] > 70 and pole_result_1h[1] > 70 and pole_result_1h[2] > 70 and score[-1] > 1.2:
                    self.coin.remove(kk)
                    self.rci_result.emit(kk)

                elif pole_result_15m[0]<-70 and pole_result_15m[1]<-50 and pole_result_15m[2]<-50 and score[-1]<-1.2 and\
                        pole_result_30m[0] <-70 and pole_result_30m[1] < -50 and pole_result_30m[2] < -50 and score[-1] <-1.2 and\
                                pole_result_1h[0] <-70 and pole_result_1h[1] < -70 and pole_result_1h[2] < -70 and score[-1] <-1.2:
                    self.coin.remove(kk)
                    self.rci_result.emit(kk)

                elif pole_result_15m[0]>90 and pole_result_15m[1]>50 and pole_result_15m[2]>50 and score[-1]>1.2 and\
                        pole_result_30m[0] >90 and pole_result_30m[1] > 50 and pole_result_30m[2] > 50 and score[-1] > 1.2 and\
                                pole_result_1h[0] > 70 and pole_result_1h[1] > 70 and pole_result_1h[2] > 70 and score[-1] > 1.2:
                    self.coin.remove(kk)
                    self.rci_result.emit(kk)

                elif pole_result_15m[0]<-90 and pole_result_15m[1]<-50 and pole_result_15m[2]<-50 and score[-1]<-1.2 and\
                        pole_result_30m[0] <-90 and pole_result_30m[1] < -50 and pole_result_30m[2] < -50 and score[-1] <-1.2 and\
                                pole_result_1h[0] <-70 and pole_result_1h[1] < -50 and pole_result_1h[2] < -50 and score[-1] <-1.2:
                    self.coin.remove(kk)
                    self.rci_result.emit(kk)

                else:
                    self.rci_result.emit("Searching Again")

        threading.Timer(600, self.rci_3lines).start()
    def rci_append(self, emit_str):
        self.monitor2.append(emit_str)
    def AddCoin(self):
        num = 0
        a = self.CoinName.text()
        self.coin.append(a)

        for i in self.coin:
            self.CoinList.setItem(0, num, QTableWidgetItem(i))
            num = num+1
    def ReAddCoin(self,kk):
        num = 0
        self.CoinList.clear()
        time.sleep(1)

        for i in self.coin:
             self.CoinList.setItem(0, num, QTableWidgetItem(i))
             num = num+1
    def DeleteCoin(self):
        a = self.CoinDelete.text()
        num = int(a)
        del self.coin[num - 1]
        time.sleep(2)
        self.TableCoin.emit("Delete")
    def Trading(self):          #매매표
        ScoreList = [[" " for i in range(8)] for j in range(10)]
        balance1 = binance.fetch_balance(params={"type": "future"})
        count = 0

        positions = balance1['info']['positions']
        for mine1 in positions:
            if mine1['initialMargin'] != '0':
                ScoreList[count][0]=mine1['symbol']
                self.TradingRecord.setItem(count, 0, QTableWidgetItem(mine1['symbol']))

                ScoreList[count][1]=mine1['leverage']
                self.TradingRecord.setItem(count, 1, QTableWidgetItem(mine1['leverage']))

                ScoreList[count][2]=mine1['isolated']
                if mine1==True:
                    isolated = "ISOLATED"
                else:
                    isolated = "CROSS"
                self.TradingRecord.setItem(count, 2, QTableWidgetItem(isolated))

                ScoreList[count][3]=mine1['entryPrice']
                self.TradingRecord.setItem(count, 3, QTableWidgetItem(str(round(float(mine1['entryPrice'])), )))

                ScoreList[count][4]=mine1['notional']
                self.TradingRecord.setItem(count, 4, QTableWidgetItem(str(round(float(mine1['notional'])), )))

                ScoreList[count][5]=mine1['initialMargin']
                self.TradingRecord.setItem(count, 5, QTableWidgetItem(str(round(float(mine1['initialMargin'])), )))

                ScoreList[count][6]=mine1['unrealizedProfit']
                self.TradingRecord.setItem(count, 6, QTableWidgetItem(str(round(float(mine1['unrealizedProfit'])), )))

                ScoreList[count][7]=str(round(float(mine1['unrealizedProfit']) * 100 / float(mine1['initialMargin']), 2))
                self.TradingRecord.setItem(count, 7, QTableWidgetItem(str(ScoreList[count][7])))
                count+=1
        threading.Timer(120, self.Trading).start()
    def mybalance(self):
        balance = binance.fetch_balance()
        balance_usdt=balance['USDT']
        free = balance_usdt['free']  #잔액
        used = balance_usdt['used']  #거래 잔액
        total = balance_usdt['total']  #총잔액
        self.Free.setText(f'{free}')
        self.Used.setText(f'{used}')
        self.Total.setText(f'{total}')
        #threading.Timer(2.5, self.mybalance()).start()
    def time1(self):
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")
        self.timeout.emit(today)
        threading.Timer(1, self.time1).start()
    def time2(self, nowtime):
        self.Time.setText(nowtime)
    def end_tast(self, end_str):
        print(f'{end_str}')
        self.startButton.setEnabled(True)
    def resp(self, market, leverage):
        resp = binance.fapiPrivate_post_leverage \
                ({
                'symbol': market['id'],
                'leverage': leverage
            })
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()









print("**********************************************************************")
print("*******")



























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

