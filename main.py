import time

from binance import Client
import pandas as pd

from config import api_secret, api_key


def get_actual_pair(client: Client, symbol: str):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return ticker


def get_futures_change(f_prev: float, f_current: float):
    return round(abs(f_prev-f_current)/f_prev*100, 4)


def check_difference(futures_1: float, futures_2: float):
    difference = abs(futures_2 - futures_1)
    return "Незначительная разница" if difference < 0.1 else f"разница на {difference}"


def check_if_difference_is_significant(client: Client):
    eth_story = []
    btc_story = []
    i = 0
    while True:
        eth_story.append(float(get_actual_pair(client, "ETHUSDT")["price"]))
        btc_story.append(float(get_actual_pair(client, "BTCUSDT")["price"]))
        if i:
            eth_change = get_futures_change(eth_story[-2], eth_story[-1])
            btc_change = get_futures_change(btc_story[-2], btc_story[-1])
            print(check_difference(eth_change, btc_change))
        i += 1
        time.sleep(30)


def main():
    client = Client(api_key, api_secret, testnet=True)
    #check_if_difference_is_significant(client)
    df = pd.DataFrame(client.futures_historical_klines(
        symbol='BTCUSDT',
        interval='1h',
        start_str='2023-06-20',
        end_str='2023-06-30'
    ), columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    print(df[['Open', 'High', 'Low', 'Close']])


if __name__ == '__main__':
    main()
