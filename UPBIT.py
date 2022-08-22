import pyupbit
import time
#------------------------------------------
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
#-----------------------------------------------

Find_Window = uic.loadUiType("C:/Users/zzune/PycharmProjects/pythonProject/text.ui")[0]

class MyWindow(QMainWindow, Find_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.PP)

    def PP(self):

        # 이평선과 현재가 터치하는가

        Kind = pyupbit.get_tickers(fiat="KRW")
        # Kind = [s for s in CoinKind if "KRW" in s]

        # while True:
        for i in Kind:

            Price_now = pyupbit.get_current_price(i)  # 현재가

            # # 4시간봉 7일 이평선
            # av = pyupbit.get_ohlcv(i, interval="hours4", count=50)
            # close = av['close']
            # ma5_4 = close.rolling(42).mean()

            # 15분봉 7일 이평선
            # av = pyupbit.get_ohlcv(i, interval="minutes15", count=700)
            # close = av['close']
            # ma5_15 = close.rolling(672).mean()

            # 30분봉 7일 이평선
            # av = pyupbit.get_ohlcv(i, interval="minutes30", count=700)
            # close = av['close']
            # ma5_30 = close.rolling(336).mean()

            # 30분봉 7일 이평선
            # av = pyupbit.get_ohlcv(i, interval="hours1", count=700)
            # close = av['close']
            # ma5_1h = close.rolling(168).mean()

            av = pyupbit.get_ohlcv(i, interval="hours2", count=25)
            close = av['close']
            ma5_2h = close.rolling(21).mean()

            # if Price_now < ma5_15.iloc[-1] and Price_now < ma5_30.iloc[-1] and Price_now < ma5_1h.iloc[
            #     -1] and Price_now < ma5_2h.iloc[-1]:
                # self.Monitor.insertPlainText(float(i))
            #     print("---------------------")

            if Price_now < ma5_2h.iloc[-1]:

                print("출력시작")
                self.Monitor.append("**********************")
                print(i)
                print("출력종료")


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()



















# #현재가 조회
# price = pyupbit.get_current_price("KRW-BTC")
# print(price)
# print("\n")
#
#
#
#
#
#
# #현재가 조회
# price1 = pyupbit.get_current_price(["BTC-XRP", "KRW-XRP"])
# print(price1)
# print("\n")
#
#
#
#
#
#
#
# #과거 데이트 시가open, 고가high, 저가low, 종가close, 거래량volume 오전9시부터 시작   (interval을 추가하면 월/주/일/분 선택이 가능하다)
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute30", count=5)
# print(df)
# print("\n")
#
#
#
#
#
#
#
# #매수호가 매도호가
# orderbook = pyupbit.get_orderbook("KRW-BTC")
# print(orderbook)
# print("\n")
#
#
#
#
#
# access_key = "1gy5EpKHaCt0vyhyVzxC6K0EIuN4nVxv46LAAx37"
# secret_key = "8lfVspOwK0HryXANUBdMeXpHfgFe9K2PcaWkpus4"
#
# #나의 잔고
# upbit = pyupbit.Upbit(access_key,secret_key)
# print(upbit.get_balances())
#
# # # 예약 매수 취소
# # upbit = pyupbit.Upbit(access_key,secret_key)
# # ret = upbit.cancel_order('be0c4343-bd9d-4aef-b5fb-cf62f4ea5178')
# # print(ret)
#
# # 매수
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.buy_limit_order("KRW-XRP", 10, 1000)   #코인이름, 가격, 갯수
# print(ret)
#
# # #매도
# # upbit = pyupbit.Upbit(access_key,secret_key)
# # ret = upbit.buy_limit_order("KRW-XRP", 10, 1000)   #코인이름, 가격, 갯수
# # print(ret)