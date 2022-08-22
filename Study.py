import pyupbit
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time

Find_Window = uic.loadUiType("C:/Users/zzune/PycharmProjects/pythonProject/text.ui")[0]

class MyWindow(QMainWindow, Find_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        time.sleep(3)
        self.pushButton.clicked.connect(self.PP)

    def PP(self):
        Kind = pyupbit.get_tickers(fiat="KRW")

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
