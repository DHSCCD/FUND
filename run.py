import pandas as pd
import pyupbit
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import threading

access_key = "1gy5EpKHaCt0vyhyVzxC6K0EIuN4nVxv46LAAx37"
secret_key = "8lfVspOwK0HryXANUBdMeXpHfgFe9K2PcaWkpus4"

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)


# # 예약 매수 취소
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.cancel_order('be0c4343-bd9d-4aef-b5fb-cf62f4ea5178')
# print(ret)

# 매수
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.buy_limit_order("KRW-XRP", 10, 1000)   #코인이름, 가격, 갯수
# print(ret)

# #매도
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.buy_limit_order("KRW-XRP", 10, 1000)   #코인이름, 가격, 갯수
# print(ret)

Find_Window=uic.loadUiType("C:/Users/zzune/PycharmProjects/FUND/text.ui")[0]

class MyWindow(QMainWindow, Find_Window):
    ticker_selected = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kind = pyupbit.get_tickers(fiat = "KRW")

        self.pushButton.clicked.connect(self.start_task)

        self.ticker_selected.connect(self.ticker_append)
        self.finished.connect(self.end_task)

    def start_task(self):
        self.thread = threading.Thread(target=self.run_test)
        self.thread.start()
        self.pushButton.setEnabled(False)

    def end_task(self, end_str):
        # print(f'{end_str}')
        self.pushButton.setEnabled(True)

    def run_test(self):
        for i in self.kind:
            # 일봉 20일 이평선
            Price_now = pyupbit.get_current_price(i)
            av = pyupbit.get_ohlcv(i, interval="hours2", count=25)
            close = av['close']
            ma5_2h = close.rolling(21).mean()
            print(ma5_2h)

            # 4시간봉 7일 이평선
            av = pyupbit.get_ohlcv(i, interval="hours4", count=50)
            close = av['close']
            ma5_4 = close.rolling(42).mean()

            # 15분봉 7일 이평선
            av = pyupbit.get_ohlcv(i, interval="minutes15", count=700)
            close = av['close']
            ma5_15 = close.rolling(672).mean()

            # 30분봉 14일 이평선
            av = pyupbit.get_ohlcv(i, interval="minutes30", count=700)
            close = av['close']
            ma14_30 = close.rolling(672).mean()

            # 30분봉 25일 이평선
            av = pyupbit.get_ohlcv(i, interval="minutes30", count=1300)
            close = av['close']
            ma25_30 = close.rolling(1200).mean()

            # 1분봉 7일 이평선
            av = pyupbit.get_ohlcv(i, interval="hours1", count=700)
            close = av['close']
            ma5_1h = close.rolling(168).mean()

            # 1시간봉 200일 이평선
            av = pyupbit.get_ohlcv(i, interval="hours1", count=5000)
            close = av['close']
            ma200_1h = close.rolling(4800).mean()

            # 1시간봉 150 이평선
            av = pyupbit.get_ohlcv(i, interval="hours4", count=3800)
            close = av['close']
            ma150_1h = close.rolling(3600).mean()

            #볼린저밴드 test
            av_20 = close.rolling(20).mean()
            av__20 = close.rolling(20).std()
            final = av_20 - 2 * av__20


            if Price_now >final[-1]:
                print(f'{i}')
                self.ticker_selected.emit("Hello")
                # if  Price_now>ma5_2h:
                #      print(f'{i}')


            time.sleep(0.3)


    def ticker_append(self,emit_str):
        self.Monitor.append(emit_str)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()