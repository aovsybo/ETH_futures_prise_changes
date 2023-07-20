from binance import Client

from config import percent_change


def get_futures_change(f_prev: float, f_current: float):
    return round(abs(f_prev-f_current)/f_prev*100, 1)


def get_actual_pair(client: Client, symbol: str):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return ticker


def is_difference_significant(futures_1: float, futures_2: float, insignificant_difference: float):
    difference = abs(futures_2 - futures_1)
    return "Незначительная разница" if difference < insignificant_difference else f"разница на {difference}"


def has_changes_for_hour(futures_history: list[float]) -> dict:
    low = min(futures_history)
    high = max(futures_history)
    change = get_futures_change(low, high)
    result = {
        "status": change >= percent_change,
        "change": change
    }
    return result
