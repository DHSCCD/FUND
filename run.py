import pyupbit
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import threading

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
        print(f'{end_str}')
        self.pushButton.setEnabled(True)

    def run_test(self):
        for i in self.kind:
            Price_now = pyupbit.get_current_price(i)
            av = pyupbit.get_ohlcv(i, interval="hours2", count=25)
            close = av['close']
            ma5_2h = close.rolling(21).mean()

            if Price_now<ma5_2h.iloc[-1]:
                print(f'ok{i}')
                self.ticker_selected.emit(f'{i}')

            time.sleep(0.3)
        self.finished.emit('end_task')

    def ticker_append(self,emit_str):
        self.Monitor.append(emit_str)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()