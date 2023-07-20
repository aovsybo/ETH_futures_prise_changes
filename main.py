import time
from datetime import datetime

from binance import Client

from config import api_secret, api_key, request_interval_seconds, changes_interval_minutes
from dependency_calculate import calculate_futures_price_dependency
from utils import get_actual_pair, is_difference_significant, has_changes_for_hour


def mainloop(client: Client, insignificant_difference: float):
    # Init
    eth_story = [float(get_actual_pair(client, "ETHUSDT")["price"]) for i in range(changes_interval_minutes)]
    btc_story = [float(get_actual_pair(client, "BTCUSDT")["price"]) for i in range(changes_interval_minutes)]

    while True:
        minute = datetime.now().minute
        eth_story[minute] = float(get_actual_pair(client, "ETHUSDT")["price"])
        btc_story[minute] = float(get_actual_pair(client, "BTCUSDT")["price"])
        #TODO Проверить зависимость от битка

        # print(is_difference_significant(eth_change, btc_change, insignificant_difference))

        has_changes = has_changes_for_hour(eth_story)
        if has_changes["status"]:
            print(f"Futures changed for {has_changes['change']}%")
        time.sleep(request_interval_seconds)

# TODO: Тесты
def main():
    client = Client(api_key, api_secret, testnet=True)
    insignificant_difference = calculate_futures_price_dependency(client)
    mainloop(client, insignificant_difference)


if __name__ == '__main__':
    main()
