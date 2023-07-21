from binance import Client

from config import percent_change


def get_futures_change(f_prev: float, f_current: float) -> float:
    """
    :param f_prev: previous futures price
    :param f_current: current futures price
    :return: percent of difference between previous and current futures
    """
    return round((f_prev-f_current)/f_prev*100, 1)


def get_actual_pair(client: Client, symbol: str):
    """
    :param client: param for making requests to binance
    :param symbol: name of futures
    :return: current info about futures
    """
    ticker = client.get_symbol_ticker(symbol=symbol)
    return ticker


def has_changes_for_hour(futures_history: list[float]) -> dict:
    """
    :param futures_history: history of self changes of futures
    :return: changes during past hour
    """
    result = dict()
    result["change"] = round(sum(futures_history), 1)
    result["status"] = result["change"] >= percent_change
    return result
