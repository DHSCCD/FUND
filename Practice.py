import ccxt

with open("C:/Users/zzune/PycharmProjects/FUND/api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})




coin = binance.fetch_ticker("ETH/USDT")
balance = binance.fetch_balance()
print(coin)
print(balance`)