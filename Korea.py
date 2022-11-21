import mojito
import pprint

key = "PSzp4vdwqlZ302SpBNtglLZi1YKsMdEhKH4S"
secret = "SQl/rDoWlst0aRCaDesdtZ2kiQzP154gEfP+lgvQt8g8SelBMi+jNCKk3UlOGobpY1DmfUGVVb48MLaio+gZygPzomqU5nYGTKha+e6LTM0GR4WhOwYItPMYc557PdqvgUAI7OqpGnxPXOMktH755CUdyFz4L42ap3nWCOy2L1PrRAf7mA0="
ACC_NO = "63589255-01"


# broker라는 변수가 KoreaInvestment 클래스의 객체를 바인딩
broker = mojito.KoreaInvestment(
    api_key=key,
    api_secret=secret,
    acc_no=ACC_NO
)

symbols = broker.fetch_symbols()

# #자주 조회하는 종류
# resp = broker.fetch_price("005930")
#
# print("Open:  ", resp['output']['stck_oprc'])   # 시가
# print("High : ", resp['output']['stck_hgpr'])    # 고가
# print("Low  : ", resp['output']['stck_lwpr'])     # 저가
# print("Close: ", resp['output']['stck_prpr'])    # 종가