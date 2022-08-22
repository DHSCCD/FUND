import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
# --------------------------------------------------
from PyQt5.QtWidgets import QTableWidgetItem, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
# ---------------------------------------------------
import time


class OrderbookWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            data = pyupbit.get_orderbook(self.ticker)
            time.sleep(10)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False


class OrderbookWidget(QWidget):
    def __init__(self, ticker="KRW-BTC"):
        super().__init__()
        uic.loadUi("C:/Users/zzune/PycharmProjects/pythonProject/orderbook.ui", self)
        # ---------------------------------------------추가
        self.asksAnim = []
        self.bidsAnim = []

        for i in range(self.tableBids.rowCount()):
            # 매도호가
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 1, item_1)

            item_2 = QProgressBar(self.tableAsks)
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_2.setStyleSheet("""
            QProgressBar {background-color : rgba(0,0,0,0%);border : 1}
            QProgressBar::Chunk {background-color : rgba(255, 0,0,50%);border : 1}
            """)
            self.tableAsks.setCellWidget(i, 2, item_2)

            # 매도호가
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 1, item_1)

            item_2 = QProgressBar(self.tableBids)
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_2.setStyleSheet("""
                QProgressBar {background-color : rgba(0,0,0,0%);border : 1}
                QProgressBar::Chunk {background-color : rgba(255, 0,0,40%);border : 1}
                """)
            self.tableBids.setCellWidget(i, 2, item_2)

            # ----------------------------------------------추가
            self.ticker = ticker

            # -----------------------------
            self.ow = OrderbookWorker(ticker)
            self.ow.dataSent.connect(self.updateData)
            self.ow.start()

    def updateData(self, data):
        print(data)

    def closeEvent(self, event):
        self.ow.close()


    # #교재 답지
    # def updateData(self, data):
    #     tradingBidValues = [ ]
    #     for v in data['bids']:
    #         tradingBidValues.append(float(v['price'] * v['quantity']))
    #     tradingAskValues = [ ]
    #     for v in data['asks'][::-1]:
    #         tradingAskValues.append(float(v['price'] * v['quantity']))
    #     maxtradingValue = max(tradingBidValues + tradingAskValues)
    #
    #     for i, v in enumerate(data['asks'][::-1]):
    #         item_0 = self.tableAsks.item(i, 0)
    #         item_0.setText(f"{v['price']:,}")
    #         item_1 = self.tableAsks.item(i, 1)
    #         item_1.setText(f"{v['quantity']:,}")
    #         item_2 = self.tableAsks.cellWidget(i, 2)
    #         item_2.setRange(0, maxtradingValue)
    #         item_2.setFormat(f"{tradingAskValues[i]:,}")
    #         # item_2.setValue(tradingAskValues[i])
    #         # ----------------- 추 가 ------------------
    #         self.asksAnim[i].setStartValue(item_2.value() if item_2.value() > 0 else 0)
    #         self.asksAnim[i].setEndValue(tradingAskValues[i])
    #         self.asksAnim[i].start()
    #         # ------------------------------------------
    #
    #     for i, v in enumerate(data['bids']):
    #         item_0 = self.tableBids.item(i, 0)
    #         item_0.setText(f"{v['price']:,}")
    #         item_1 = self.tableBids.item(i, 1)
    #         item_1.setText(f"{v['quantity']:,}")
    #         item_2 = self.tableBids.cellWidget(i, 2)
    #         item_2.setRange(0, maxtradingValue)
    #         item_2.setFormat(f"{tradingBidValues[i]:,}")
    #         # item_2.setValue(tradingBidValues[i])
    #         # ----------------- 추 가 ------------------
    #         self.bidsAnim[i].setStartValue(item_2.value() if item_2.value() > 0 else 0)
    #         self.bidsAnim[i].setEndValue(tradingBidValues[i])
    #         self.bidsAnim[i].start()
    #         # ------------------------------------------


    def updateData(self, data):
        tradingValues = []
        for v in data['bids']:
            tradingValues.append(float(v['price'] * v['quantity']))
        maxTradingVlue = max(tradingValues)

        for i, v in enumerate(data['asks'][::-1]):
            item_0 = self.tableAsks.item(i, 0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableAsks.item(i, 1)
            item_1.setText(f"{v['price']:,}")
            item_2 = self.tableAsks.cellWidget(i, 2)
            item_2.setRange(0, maxTradingVlue)
            item_2.setFormat((f"{tradingValues[i]:,}"))
            item_2.setValue(tradingValues[i])

        for i, v in enumerate(data['asks'][::-1]):
            item_0 = self.tableBids.item(i, 0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableBidss.item(i, 1)
            item_1.setText(f"{v['price']:,}")
            item_2 = self.tableBids.cellWidget(i, 2)
            item_2.setRange(0, maxTradingVlue)
            item_2.setFormat((f"{tradingValues[i]:,}"))
            item_2.setValue(tradingValues[i])


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ow = OrderbookWidget(ticker='KRW-BTC')
    ow.show()
    sys.exit(app.exec_())




# # ui 파일을 불러온 후 그림을 넣는 방법
# #ui 파일을 불러오는 코드
# # 위에 점을 없애는 방법
# import sys
# from PyQt5 import uic
# #-----------------------------------
# from PyQt5.QtChart import QLineSeries, QChart       #series 글려질 데이터(선) chart 도화지(공간)
# #-----------------------------------------
# from PyQt5.QtGui import QPainter
# -----------------------------------------
# from PyQt5.QtChart import QValueAxis, QDateTimeAxis
# from PyQt5.QtCore import Qt, QDateTime      # X축을 시간으로 표현하기 위하여 Time 추가
# #-----------------------------------------
#
#
# import time
# import pybithumb
# from PyQt5.QtCore import QThread, pyqtSignal
# from PyQt5.QtWidgets import QWidget
#
# class PriceWorker(QThread):             #QThread를 상속받은 PriceWorker
#     dataSent = pyqtSignal(float)
#
#     def __init__(self, ticker):
#         super().__init__()
#         self.ticker = ticker
#         self.alive = True
#
#     def run(self):
#         while self.alive:
#             data = pybithumb.get_current_price(self.ticker)
#             time.sleep(1)
#             self.dataSent.emit(data)            #값을 내보낸다.
#
#     def close(self):
#         self.alive = False
#
#
#
#
#
#
#
# class ChartWidget(QWidget):
#     def __init__(self, parent=None, ticker="BTC"):
#         super().__init__(parent)                                                        #QWidget의 parent 함수를 호출함
#         uic.loadUi("C:/Users/zzune/PycharmProjects/pythonProject/chart.ui", self)
#         self.ticker = ticker
#         #----------------------------------
#         self.viewLimit = 128
#
#         self.priceData = QLineSeries()  #선을 그리겠다고 선언
#         self.priceChart = QChart()
#         self.priceChart.addSeries(self.priceData)   #데이터를 차트 객체로 전달해서 시각화
#         self.priceChart.legend().hide()
#
#         self.pw = PriceWorker(ticker)
#         self.pw.dataSent.connect(self.appendData)
#         self.pw.start()
#         # ------------------------------------------------ 가로, 세로 축 지정, 시간 추가
#         axisX = QDateTimeAxis()                     #날씨축을 관리하는 객체를 선언
#         axisX.setFormat("hh:mm:ss")                 #시,분,초 선언
#         axisX.setTickCount(4)                       # 시,분,초를 한 그래프에 몇 개를 나타낼 것인가
#         dt = QDateTime.currentDateTime()            # 현재 시간 정보를 QDataTime을 통해서 현재 시간을 얻어옵니다.
#         axisX.setRange(dt, dt.addSecs(self.viewLimit))
#         #시간 범위를 현재부터 120초 이후까지 설정합니다. addSec은 지정된 초 이후의 시간을 QDataTime으로 반환한다.
#
#         axisY = QValueAxis()
#         axisY.setVisible(False)
#
#         self.priceChart.addAxis(axisX, Qt.AlignBottom)
#         self.priceChart.addAxis(axisY, Qt.AlignRight)
#         self.priceData.attachAxis(axisX)
#         self.priceData.attachAxis(axisY)
#         self.priceChart.layout().setContentsMargins(0, 0, 0, 0)
#         # ---------------------------------------------------
#         self.priceView.setChart(self.priceChart)    #차트를 ui로 전송
#         self.priceView.setRenderHints(QPainter.Antialiasing)
#
#     def appendData(self, currPrice):
#         if len(self.priceData) == self.viewLimit:               #정해진 갯수만큼 저장되어 있을때 0번의 인덱스를 삭제.
#             self.priceData.remove(0)
#         dt = QDateTime.currentDateTime()
#         self.priceData.append(dt.toMSecsSinceEpoch(), currPrice)
#         self.__updateAxis()
#
#     def __updateAxis(self):
#         pvs = self.priceData.pointsVector()                         #pvs리스트 안에는 QPointF 객체로 위치??? 정보가 정장돼 있습니다.
#         dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))
#         if len(self.priceData) == self.viewLimit:
#             dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
#         else:
#             dtLast = dtStart.addSecs(self.viewLimit)
#
#         ax = self.priceChart.axisX()
#         ax.setRange(dtStart, dtLast)
#
#         ay = self.priceChart.axisY()
#         dataY = [v.y() for v in pvs]
#         ay.setRange(min(dataY), max(dataY))
#
#
#
#
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)        #프로그램 실행
#     cw = ChartWidget()      #class 실행
#     cw.show()               # cw 동작
#     exit(app.exec_())


# #뭐지?
#
#     def my_exception_hook(exctype, value, traceback):
#         print(exctype, value, traceback)
#         sys._excepthook(exctype, value, traceback)
#
#         sys._excepthook = sys.excepthook
#         sys.excepthook = my_exception_hook()


# # ui 파일을 불러온 후 그림을 넣는 방법
# #ui 파일을 불러오는 코드
# # 위에 점을 없애는 방법
# import sys
# from PyQt5 import uic
# from PyQt5.QtWidgets import QWidget
# #-----------------------------------
# from PyQt5.QtChart import QLineSeries, QChart       #series 글려질 데이터(선) chart 도화지(공간)
# #-----------------------------------------
# from PyQt5.QtGui import QPainter
# #-----------------------------------------
#
# class ChartWidget(QWidget):
#     def __init__(self, parent=None, ticker="BTC"):
#         super().__init__(parent)
#         uic.loadUi("C:/Users/zzune/PycharmProjects/pythonProject/chart.ui", self)
#         self.ticker = ticker
#         #----------------------------------
#         self.viewLimit = 128
#
#         self.priceDate = QLineSeries()  #선을 그리겠다고 선언
#         self.priceDate.append(0,10)
#         self.priceDate.append(1,20)
#         self.priceDate.append(2,10)
#
#         self.priceChart = QChart()
#         self.priceChart.addSeries(self.priceDate)   #데이터를 차트 객체로 전달해서 시각화
#
#         self.priceView.setChart(self.priceChart)    #차트를 ui로 전송
#
#         self.priceChart.legend().hide()
#         self.priceView.setRenderHints(QPainter.Antialiasing)
#
#
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)        #프로그램 실행
#     cw = ChartWidget()      #class 실행
#     cw.show()               # cw 동작
#     exit(app.exec_())


# # ui 파일을 불러온 후 그림을 넣는 방법
# #ui 파일을 불러오는 코드
# import sys
# from PyQt5 import uic
# from PyQt5.QtWidgets import QWidget
# #-----------------------------------
# from PyQt5.QtChart import QLineSeries, QChart       #series 글려질 데이터(선) chart 도화지(공간)
# #-----------------------------------------
#
# class ChartWidget(QWidget):
#     def __init__(self, parent=None, ticker="BTC"):
#         super().__init__(parent)
#         uic.loadUi("C:/Users/zzune/PycharmProjects/pythonProject/chart.ui", self)
#         self.ticker = ticker
#         #----------------------------------
#         self.viewLimit = 128
#
#         self.priceDate = QLineSeries()  #선을 그리겠다고 선언
#         self.priceDate.append(0,10)
#         self.priceDate.append(1,20)
#         self.priceDate.append(2,10)
#
#         self.priceChart = QChart()
#         self.priceChart.addSeries(self.priceDate)   #데이터를 차트 객체로 전달해서 시각화
#
#         self.priceView.setChart(self.priceChart)    #차트를 ui로 전송
#
#
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)        #프로그램 실행
#     cw = ChartWidget()      #class 실행
#     cw.show()               # cw 동작
#     exit(app.exec_())


# #ui 파일을 불러오는 코드
# import sys
# from PyQt5 import uic
# from PyQt5.QtWidgets import QWidget
#
# class ChartWidget(QWidget):
#     def __init__(self, parent=None, ticker="BTC"):
#         super().__init__(parent)
#         uic.loadUi("C:/Users/zzune/PycharmProjects/pythonProject/chart.ui", self)
#         self.ticker = ticker
#
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)        #프로그램 실행
#     cw = ChartWidget()      #class 실행
#     cw.show()               # cw 동작
#     exit(app.exec_())


# # 예약 매수 취소
# import pyupbit
#
# access_key = "1gy5EpKHaCt0vyhyVzxC6K0EIuN4nVxv46LAAx37"
# secret_key = "8lfVspOwK0HryXANUBdMeXpHfgFe9K2PcaWkpus4"
#
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.cancel_order('be0c4343-bd9d-4aef-b5fb-cf62f4ea5178')
# print(ret)


# # 매수
# import pyupbit
#
# access_key = "1gy5EpKHaCt0vyhyVzxC6K0EIuN4nVxv46LAAx37"
# secret_key = "8lfVspOwK0HryXANUBdMeXpHfgFe9K2PcaWkpus4"
#
# upbit = pyupbit.Upbit(access_key,secret_key)
# ret = upbit.buy_limit_order("KRW-XRP", 10, 1000)   #코인이름, 가격, 갯수
# print(ret)

# # 잔고조회
# import pyupbit
#
# access_key = "1gy5EpKHaCt0vyhyVzxC6K0EIuN4nVxv46LAAx37"
# secret_key = "8lfVspOwK0HryXANUBdMeXpHfgFe9K2PcaWkpus4"
#
# upbit = pyupbit.Upbit(access_key,secret_key)
# print(upbit.get_balances())


# import pyupbit
#
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute", count=5)  #interval을 하지 않는 경우 일봉을 기준으로 출력을 해준다. count 는 최근 일수 기간동안만 출력을 해준다.
# print(df)


# # 업비트 가겨조회하기
# import pyupbit
# price = pyupbit.get_current_price(["KRW-XRP","KRW-BTC"])
# print(price)


# #
# import sys
# from PyQt5.QtWidgets import *   #QApplicaiton이 value로 포함되어있다.
# from PyQt5 import uic       #uic 눈에보이는 프로그램
# from PyQt5.QtCore import *  # 스레드
# import pybithumb
# import time                #타이머
#
# tickers = ["BTC", "ETH", "BCH", "ETC"]
# form_class = uic.loadUiType("bull.ui")[0]
#
# class Worker(QThread):
#     finished = pyqtSignal(dict)         #변경 이게뭘까?,,, 무조건 해줘야하는 건데 일단 표를 추가하고 표에 값을 넣으니 필요
#
#     def run(self):
#         while True:
#             data = {}
#
#             for ticker in tickers:
#                 data[ticker] = self.get_market_infos(ticker)
#
#             self.finished.emit(data)    #변경
#             time.sleep(2)               #변경
#
#
#     def get_market_infos(self, ticker):
#         try:
#             df = pybithumb.get_ohlcv(ticker)
#             ma5 = df['close'].rolling(window=5).mean()
#             last_ma5 = ma5[-2]
#             price = pybithumb.get_current_price(ticker)
#
#             state = None
#             if price > last_ma5:
#                 state = "상승장"
#             else:
#                 state = "하락장"
#
#             return price, last_ma5, state
#
#         except:
#             return None,None,None
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         self.worker = Worker()
#         self.worker.finished.connect(self.update_table_widget)      #변경
#         self.worker.start()
#
#     @pyqtSlot(dict)
#     def update_table_widget(self, data):
#         try:
#             for ticker, infos in data.items():
#                 index = tickers.index(ticker)
#
#                 self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))   #변경
#                 self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))   #변경
#                 self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))   #변경
#                 self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))   #변경
#         except:
#             pass
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


# # 스레드를 적용한 상승장, 하락장 구분 코딩
# import sys
# from PyQt5.QtWidgets import *   #QApplicaiton이 value로 포함되어있다.
# from PyQt5 import uic       #uic 눈에보이는 프로그램
# from PyQt5.QtCore import *  # 스레드
# import pybithumb
# import time                #타이머
#
# tickers = ["BTC", "ETH", "BCH", "ETC"]
# form_class = uic.loadUiType("bull.ui")[0]
#
# class Worker(QThread):
#     def run(self):
#         while True:
#             data = {}
#
#             for ticker in tickers:
#                 data[ticker] = self.get_market_infos(ticker)
#
#             print(data)
#             time.sleep(5)
#
#     def get_market_infos(self, ticker):
#         try:
#             df = pybithumb.get_ohlcv(ticker)
#             ma5 = df['close'].rolling(window=5).mean()
#             last_ma5 = ma5[-2]
#             price = pybithumb.get_current_price(ticker)
#
#             state = None
#             if price > last_ma5:
#                 state = "상승장"
#             else:
#                 state = "하락장"
#
#             return price, last_ma5, state
#
#         except:
#             return None,None,None
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         self.worker = Worker()
#         self.worker.start()
#
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


# # 상승장 알리미(스레드 버전)
# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
#
# class Worker(QThread):
#     def run(self):
#         while True:
#             print("안녕하세요")
#             self.sleep(1)
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.worker = Worker()
#         self.worker.start()
#
# app = QApplication(sys.argv)
# mywindow = MyWindow()
# mywindow.show()
# app.exec_()


# # 가상화페 이름 출력하기 p235
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# from PyQt5.QtCore import *
#
# tickers = ["BTC", "ETH","BCH", "ETC"]
# form_class = uic.loadUiType("bull.ui")[0]
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         timer = QTimer(self)
#         timer.start(5000)
#         timer.timeout.connect(self.timeout)
#
#     def timeout(self):
#             for i, ticker in enumerate(tickers):
#                 item = QTableWidgetItem(ticker)
#                 self.tableWidget.setItem(i,0,item)
#
#
# app = QApplication(sys.argv)
# win = MyWindow()
# win.show()
# app.exec_()


# # 5초마다 값을 불러오는 타이머 만들기
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# from PyQt5.QtCore import *
#
# form_class = uic.loadUiType("bull.ui")[0]
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         timer = QTimer(self)
#         timer.start(5000)
#         timer.timeout.connect(self.timeout)
#
#     def timeout(self):
#         print("5초에요!!")
#
# app = QApplication(sys.argv)
# win = MyWindow()
# win.show()
# app.exec_()


# # 상승장 알리미 화면
# import sys
#
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
#
# from_class = uic.loadUiType("bull.ui")[0]
#
# class MyWindow(QMainWindow, from_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
# app = QApplication(sys.argv)
# win = MyWindow()
# win.show()
# app.exec_()


# # p227 이평선에 따른 상승장 구별
# import pybithumb
#
# df = pybithumb.get_ohlcv("BTC")
# ma5 = df['close'].rolling(window=5).mean()
# last_ma5 = ma5[-2]
#
# price = pybithumb.get_current_price("BTC")
#
# if price > last_ma5:
#     print("상승장")
# else:
#     print("하락장")


# # 이평선계산
# import pybithumb
#
# btc = pybithumb.get_ohlcv("BTC")
# print(btc)
# close = btc['close']
#
# window = close.rolling(5)
# ma5 = window.mean() #평균 value
# print(ma5)


# 오류 발생 방지
# import pybithumb
# import time
#
# while True:
#     price = pybithumb.get_current_price("BTC")
#     if price is not None:
#         prinet =(price/10)
#     time.sleep(0.2)


# # 여러 가상화폐에 대한 정보 얻기
# import pybithumb
#
# all = pybithumb.get_current_price("ALL")
# for k, v in all.items():
#     print(k,v)


# import pybithumb
# import time
#
# orderbook = pybithumb.get_orderbook("BTC")
# asks = orderbook['asks']
#
# for ask in asks:
#     print(ask)
#     print('-------------')
#     time.sleep(0.1)


# # 매도/ 매수 잔량
# import pybithumb
#
# orderbook = pybithumb.get_orderbook("BTC")
# print(orderbook)
#
# print(orderbook['payment_currency'])
# print("------------------------------------")
#
# for k in orderbook:
#     print(k)

# # 시가/고가/저가/종가/거래량을 알려주는 코딩
# import pybithumb
#
# detail = pybithumb.get_market_detail("BTC")
# print(detail)


# 빗썸의 모든 코인들을 1초 간격으로 가격을 불러오기
# import pybithumb
# import time
#
# tickers = pybithumb.get_tickers()
# for ticker in tickers:
#     price = pybithumb.get_current_price(ticker)
#     print(ticker,price)
#     time.sleep(1)


# 빗썸에서 가격불러오기
# import pybithumb
#
# price = pybithumb.get_current_price("BTC")
# print(price)


# from pandas import Series
#
# s = Series([100, 200, 300])
# s2 = s.shift(1)
# print(s)
# print(s2)


# 행 열 추가 DataFrame
# from pandas import DataFrame, Series
#
# data = {'open': [100,200], "high": [110,120]}
# df1 = DataFrame(data)
# s = Series([777, 333])
# df1["Plus"] = s
#
# print(df1)


# #DataFrame 인덱싱 슬라이스
# p202
# from pandas import DataFrame
#
# data = {'open': [100,200], "high": [110,120]}
# df = DataFrame(data)
# print(df)
# print("----------------")
# print(df.loc[0])
# print(df["open"])


# data = {"open": [1,2], "height":[3,5]}
# df = DataFrame(data, index=["2018-01-01", "2018-01-02"])
# print(df["open"])


# 인터넷 테이블로 부터 자료를 가져오는 것인데 이것에 대한 문제가 설명되어 있다.
# 참고 주소 : https://www.inflearn.com/questions/152894
# # p200
# import pandas as pd
# url='https://finance.naver.com/sise/sise_quant.naver'
# df = pd.read_html(url,encoding='euc-kr')
# df1=df[1].dropna()
# print(df1)


# #p177
# import requests
# from bs4 import BeautifulSoup
#
# url = "https://finance.naver.com/item/main.nhn?code=000660"
# html = requests.get(url).text
#
# soup = BeautifulSoup(html,"html5lib")
# tags = soup.select("#_per")
# tag = tags[0]
# print(tag.text)


# p155
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
# class MySignal(QObject):
#     signal1 = pyqtSignal()
#     signal2 = pyqtSignal(int, int)
#
#     def run(self):
#         self.signal1.emit()
#         self.signal2.emit(1, 2)
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         mysignal = MySignal()
#         mysignal.signal1.connect(self.signal1_emitted)
#         mysignal.signal2.connect(self.signal2_emitted)
#         mysignal.run()
#
#     @pyqtSlot()
#     def signal1_emitted(self):
#         print("signal1 emitted")
#
#     @pyqtSlot(int, int)
#     def signal2_emitted(self, arg1, arg2):
#         print("signal2 emitted",arg1, arg2)
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


#  #p152 시간설정
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.timer = QTimer(self)
#         self.timer.start(1000)
#         self.timer.timeout.connect(self.timeout)
#
#     def timeout(self):
#         cur_time = QTime.currentTime()
#         str_time = cur_time.toString("hh:mm:ss")
#         self.statusBar().showMessage(str_time)
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


# 가격출력 p149
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# import pykorbit
#
# form_class = uic.loadUiType("window.ui")[0]
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.pushButton.clicked.connect(self.inquiry)
#
#     def inquiry(self):
#         price = pykorbit.get_current_price("BTC")
#         self.lineEdit.setText(str(price))
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


# p146
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
#
# form_class = uic.loadUiType("mywindow.ui")[0]
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.pushButton.clicked.connect(self.btn_clicked)
#
#     def btn_clicked(self):
#         print("버튼클릭")
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


# import sys                      #sys를 사용한다.
# from PyQt5.QtWidgets import *   # PyQt5를 사용한다.
# from PyQt5.QtGui import *       # png 그림 사용
#
# class MyWindow(QMainWindow):    # class 사용, MyWindow 임의 이름, 불러온 Qtwidgets 사용
#     def __init__(self):         # init사용
#         super().__init__()
#         self.setGeometry(100,200,300,400)   #크기는 가로 다음 세로, 공백 다음 프로그램 크기
#         self.setWindowTitle("PyQt")
#
#         btn = QPushButton("버튼1", self)
#         btn.move(10, 10)
#         btn.clicked.connect(self.btn_clicked)
#
#     def btn_clicked(self):
#         print("버튼 클릭")
#
#         btn2 = QPushButton("버튼2", self)
#         btn2.move(10,40)
#
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()                     # 프로그램이 닫기 전까지 계속 실행된다.
