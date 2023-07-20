import time
from datetime import datetime

from binance import Client

from config import api_secret, api_key, request_interval_seconds, changes_interval_minutes
from dependency_calculate import calculate_futures_price_dependency
from utils import get_actual_pair, has_changes_for_hour, get_futures_change


def mainloop(client: Client, insignificant_difference: float) -> None:
    """
    mainloop that catch self changes of ETHUSDT and alert if it is more than 1% during past hour
    :param client:
    :param insignificant_difference:
    """
    # initialize history log for past hour for each future
    eth_story = [0] * changes_interval_minutes
    btc_story = [0] * changes_interval_minutes
    eth_prev = float(get_actual_pair(client, "ETHUSDT")["price"])
    btc_prev = float(get_actual_pair(client, "BTCUSDT")["price"])
    while True:
        # write in history log difference between current and previous futures price in current minute
        minute = datetime.now().minute
        eth_story[minute] = get_futures_change(float(get_actual_pair(client, "ETHUSDT")["price"]), eth_prev)
        btc_story[minute] = get_futures_change(float(get_actual_pair(client, "BTCUSDT")["price"]), btc_prev)
        eth_prev = float(get_actual_pair(client, "ETHUSDT")["price"])
        btc_prev = float(get_actual_pair(client, "BTCUSDT")["price"])
        # check if ETHUSDT changes are self changes or it is impact of BTCUSDT
        if abs(eth_story[minute] - btc_story[minute]) > insignificant_difference:
            # in case that it is self change of ETHUSDT check
            # if its change is more than 1% during past hour
            # and creating alert in case it is
            has_changes = has_changes_for_hour(eth_story)
            if has_changes["status"]:
                print(f"Futures changed for {has_changes['change']}%")
        else:
            # in case that it is impact of BTCUSDT write 0 in history
            eth_story[minute] = 0
            btc_story[minute] = 0
        time.sleep(request_interval_seconds)


def main():
    client = Client(api_key, api_secret, testnet=True)
    insignificant_difference = calculate_futures_price_dependency(client)
    mainloop(client, insignificant_difference)


if __name__ == '__main__':
    main()
