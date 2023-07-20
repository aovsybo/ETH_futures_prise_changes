from binance import Client
import pandas as pd

from utils import get_futures_change


def get_change_percentage(client: Client, symbol: str) -> list[float]:
    """
    requests futures changes during past 2 months,
    calculates difference between two neighbour hours and writes it into list

    :param client: param for making requests to binance
    :param symbol: name of futures
    :return: list of percents of price changes every hour from past 2 months
    """

    df = pd.DataFrame(client.futures_historical_klines(
        symbol=symbol,
        interval='1h',
        start_str='2023-05-20',
        end_str='2023-07-20'
    ), columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    percentage = [
        get_futures_change(float(open_price), float(close_price))
        for open_price, close_price
        in zip(df["Open"], df["Close"])
    ]
    return percentage


def get_frequency_of_percents(percentage_differences: list) -> float:
    """
    creates dict, where key - percent, value - amount on list.
    then filter five most frequent - in these cases BTC impacts to ETH changes.
    then select max of this list and returns
    :param percentage_differences: list of percents of futures price changing  during past 2 months
    :return: max of five most frequent percents
    """
    frequency_of_percents = dict()
    for percent in percentage_differences:
        percent = str(percent)
        if percent in frequency_of_percents:
            frequency_of_percents[percent] += 1
        else:
            frequency_of_percents[percent] = 1
    most_frequent_percent = float(max(sorted([k for k, v in frequency_of_percents.items()])[:5]))
    return most_frequent_percent


def calculate_futures_price_dependency(client: Client) -> float:
    """
    calculate percents of changes of futures BTCUSDT and ETHUSDT
    and select most frequent of it
    :param client: param for making requests to binance
    :return: number that means that difference between percents is significant
    """
    eth_percentages = get_change_percentage(client, "ETHUSDT")
    btc_percentages = get_change_percentage(client, "BTCUSDT")
    percentage_differences = [
        round(abs(eth_percentage - btc_percentage), 1)
        for eth_percentage, btc_percentage
        in zip(eth_percentages, btc_percentages)
    ]
    most_frequent_percent = get_frequency_of_percents(percentage_differences)
    return most_frequent_percent
