

print("naver", "kakao", "samsung", sep=";")
#띄어쓰기를 하지않고 사이에 말을 넣는 방법

print("first", end=""); print("second")
#연속된 프린트를 붙여서 쓰는법

num_str = "720"
num_int = int(num_str)
print(num_int+1, type(num_int))
#문자열 정수 변환

lang = 'python'
print(lang[0], lang[2])
#문자에서 몇 번째 문자 뽑아오는 방법

license_plate = "24가 2210"
print(license_plate[-4:])
#문자열에서 특정 문자만 뽑기

string = "홀짝홀짝홀짝"
print(string[::1])
print(string[::2])
print(string[::3])
print(string[::-1])
print(string[::-2])
#string(시작:끝:오프셋) 으로 사이사이 문자만 뽑는법

phone_number = "010-1111-2222"
phone_number1 = phone_number.replace("-", " ")
print(phone_number1)
#일부문자열 제거 or 변경

url = "http://sharebook.kr"
a = url.split('.')
# 특정 문자를 기준으로 []를 만든다.

name1 = "김민수"
age1 = 10
name2 = "이철희"
age2 = 13

print("이름: %s 나이: %d" % (name1, age1))
print("이름: %s 나이: %d" % (name2, age2))

print("이름: {} 나이: {}".format(name1, age1))
print("이름: {} 나이: {}".format(name2, age2))

print(f"이름: {name1} 나이: {age1}")
print(f"이름: {name2} 나이: {age2}")        #문자열에 상관없이 출력을 해준다. - 아마 제일 유용할듯하다
# %foramtting을 이용한 출력

분기 = "2020/03(E) (IFRS연결)"
print(분기[:7])
#이거는 잘 모르겠다.

data = "   삼성전자    "
data1 = data.strip()
print(data1)
#공백제거


ticker = "btc_krw"
ticker1 = ticker.upper()
print(ticker1)
#대문자

a = "hello"
a = a.capitalize()
print(a)
#첫 문자만 대문자로 변경

file_name = "보고서.xlsx"
print(file_name.endswith("xlsx"))

file_name = "2020_보고서.xlsx"
file_name.startswith("2020")
#시작과 끝의 문자가 맞는지 확인하는 코드

date = "2020-05-01"
print(date.split("-"))

movie_rank = ['닥터 스트레인지', '슈퍼맨', '스플릿', '럭키', '배트맨']
del movie_rank[3]
print(movie_rank)
#리스트 삭제

nums = [1, 2, 3, 4, 5, 6, 7]
print("max: ", max(nums))
print("min: ", min(nums))
#리스트 가장 큰 값 출력

#리스트 출력 번호
price = ['20180728', 100, 130, 140, 150, 160, 170]
print(price[1:])

#리스트 홀수 번만 출력
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(nums[::2])

interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print(" ".join(interest))
#함수 출력 사이에 무엇을 넣을건지 변수 지정

string = "삼성전자/LG전자/Naver"
interest = string.split("/")
print(interest)
#split을 통하여 리스트로 분리 ""큰따옴표를 사용해야한다.

data = [2, 4, 3, 1, 5, 10, 9]
data.sort()
print(data)
#오름차순

#내림차순
print(data[::-1])

my_variable = ()
print(type(my_variable))
#튜플을 만드는 방법 - 수정이 불가능하다.





#06. 딕셔너리
temp = {}
#비어있는 딕셔너리
#파이썬 딕셔너리는 순서는 없지만 key와 value 형태로 데이터를 저장합니다. 특히 key는 데이터의 레이블(label)을 지정하는 용도로 자주 사용됩니다.
scores = [8.8, 8.9, 8.7, 9.2, 9.3, 9.7, 9.9, 9.5, 7.8, 9.4]
*valid_score, _, _, _= scores
print(valid_score)

scores = [8.8, 8.9, 8.7, 9.2, 9.3, 9.7, 9.9, 9.5, 7.8, 9.4]
a, b, *valid_score = scores
print(valid_score)

ice = {"메로나": 1000, "폴라포": 1200, "빵빠레": 1800}
print(ice)

#딕셔너리 수정할때는 []를 사용해야한다.


inventory = {"메로나": [300, 20],
              "비비빅": [400, 3],
              "죠스바": [250, 100]}
print(inventory["메로나"][0], "원")
print(inventory["메로나"][1], "원")
inventory["월드콘"] = [500, 7] #추가

icecream = {'탱크보이': 1200, '폴라포': 1200, '빵빠레': 1800, '월드콘': 1500, '메로나': 1000}
print(sum(icecream.values()))
new_product = {'팥빙수':2700, '아맛나':1000}  #새로운 딕셔너리 추가
icecream.update(new_product)


#딕셔너리 만드는 법
keys = ("apple", "pear", "peach")
vals = (300, 250, 400)
result = dict(zip(keys, vals))











#07. 파이썬 분기문

#값을 받으면 str값이므로 int로 변환을 해주어야한다.

변수 = "A"
b = 변수.lower()
print("변환:", b)
변수 = "B"
b = 변수.lower()
print("변환:", b)
변수 = "C"
b = 변수.lower()
print("변환:", b)





#8. 파이썬 반복문
리스트 = ["가", "나", "다", "라"]
for 변수 in 리스트[: :2]:
  print(변수)

리스트 = [3, 100, 23, 44]
for 변수 in 리스트:
    if 변수%3 == 0:
        print(변수)


리스트 = ["I", "study", "python", "language", "!"]
for 변수 in 리스트[1:4]:
    print(변수)


리스트 = ['hello.py', 'ex01.py', 'intro.hwp']
for 변수 in 리스트:
  split = 변수.split(".")
  print(split[0])

for i in range(100):
    print(i)

price_list = [32100, 32150, 32000, 32500]
for i, data in enumerate(price_list):
    print(i, data)
#배열 번호와 데이터 모두 출력


리스트 = ["dog", "cat", "parrot"]
for 이름 in 리스트:
  print(이름[0])


my_list = ["가", "나", "다", "라", "마"]
print(len(my_list))




# 10. 파이썬 모듈
import datetime
now = datetime.datetime.now()
print(now,type(now))

for day in range(5, 0, -1):
    delta = datetime.timedelta(days=day)
    date = now - delta
    print(date)
    # range를 이요해서 하루전씩 마이너쓰를 통해서 수를 출력할 수 있다.


now = datetime.datetime.now()
print(now.strftime("%H:%M:%S"))
# 시간을 출력하는 방법

day = "2020-05-04"
ret = datetime.datetime.strptime(day, "%Y-%m-%d")
print(ret, type(ret))

import os
ret = os.getcwd()
print(ret, type(ret))

#11. 파이썬 클래스
class Human:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

areum = Human("아름", 25, "여자")
print(areum.name)

class Stock:
    def __init__(self, name, code, per, pbr, dividend):
        self.name = name
        self.code = code
        self.per = per
        self.pbr = pbr
        self.dividend = dividend

    def set_name(self, name):
        self.name = name

    def set_code(self, code):
        self.code = code

    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

    def set_per(self, per):
        self.per = per

    def set_pbr(self, pbr):
        self.pbr = pbr

    def set_dividend(self, dividend):
        self.dividend = dividend

종목 = []

삼성 = Stock("삼성전자", "005930", 15.79, 1.33, 2.83)
현대차 = Stock("현대차", "005380", 8.70, 0.35, 4.27)
LG전자 = Stock("LG전자", "066570", 317.34, 0.69, 1.37)

종목.append(삼성)
종목.append(현대차)
종목.append(LG전자)

for i in 종목:
    print(i.code, i.per)        # i-> Stock 클래스의 객체를 바인딩하기 때문

import random


class Account:
    # class variable
    account_count = 0

    def __init__(self, name, balance):
        self.deposit_count = 0
        self.deposit_log = []
        self.withdraw_log = []

        self.name = name
        self.balance = balance
        self.bank = "SC은행"

        # 3-2-6
        num1 = random.randint(0, 999)
        num2 = random.randint(0, 99)
        num3 = random.randint(0, 999999)

        num1 = str(num1).zfill(3)  # 1 -> '1' -> '001'
        num2 = str(num2).zfill(2)  # 1 -> '1' -> '01'
        num3 = str(num3).zfill(6)  # 1 -> '1' -> '0000001'
        self.account_number = num1 + '-' + num2 + '-' + num3  # 001-01-000001
        Account.account_count += 1

    @classmethod
    def get_account_num(cls):
        print(cls.account_count)  # Account.account_count

    def deposit(self, amount):
        if amount >= 1:
            self.deposit_log.append(amount)
            self.balance += amount

            self.deposit_count += 1
            if self.deposit_count % 5 == 0:         # 5, 10, 15
                # 이자 지금
                self.balance = (self.balance * 1.01)


    def withdraw(self, amount):
        if self.balance > amount:
            self.withdraw_log.append(amount)
            self.balance -= amount

    def display_info(self):
        print("은행이름: ", self.bank)
        print("예금주: ", self.name)
        print("계좌번호: ", self.account_number)
        print("잔고: ", self.balance)

    def withdraw_history(self):
        for amount in self.withdraw_log:
            print(amount)

    def deposit_history(self):
        for amount in self.deposit_log:
            print(amount)


k = Account("Kim", 1000)
k.deposit(100)
k.deposit(200)
k.deposit(300)
k.deposit_history()

k.withdraw(100)
k.withdraw(200)
k.withdraw_history()

class 차:
    def __init__(self, 바퀴, 가격):
        self.바퀴 = 바퀴
        self.가격 = 가격

    def 정보(self):
        print("바퀴수 ", self.바퀴)
        print("가격 ", self.가격)

    def 확인(self):
        print("모두 가능하다")

class 자동차(차):
    def __init__(self, 바퀴, 가격):
        super().__init__(바퀴, 가격)

class 자전차(차):
    def __init__(self, 바퀴, 가격, 구동계):
        super().__init__(바퀴, 가격)
        self.구동계 = 구동계

    def 정보(self):
        super().정보()
        print("구동계 ", self.구동계)

    def 확인(self):
        super().확인()
        print("구동계 ", self.구동계)

bicycle = 자전차(2, 100, "시마노")
bicycle.정보()
bicycle.확인()

class 부모:
    def 호출(self):
        print("부모호출")

class 자식(부모):
    def 호출(self):
        print("자식호출")


나 = 자식()
나.호출()

class 부모:
    def __init__(self):
        print("부모생성")

class 자식(부모):
    a = 0
    def __init__(self):
        print("자식생성")
        super().__init__()
        print(a)

나 = 자식()

king = ['가', '나', '다']
for i in range(len(king)):
    print(i)