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
        self.pushButton.clicked.connect(self.printText)


        Coin = pyupbit.get_current_price("KRW-BTC")
        print('확인1')
        self.Monitor.insertPlainText(str(Coin))
        print("확인2")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()