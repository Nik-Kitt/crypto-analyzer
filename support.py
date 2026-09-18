import requests
import time

from rich.table import Table
from functools import wraps

url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1'


def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except requests.exceptions.RequestException:
                    if i == max_attempts - 1:
                        raise RuntimeError('Ошибка подключения к API')
                    time.sleep(delay)
                

        return wrapper
    return decorator


@retry(max_attempts=3, delay=2)
def load_crypto_data():
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def get_top_coins(some_data, field_name, top_n, reverse=False):
    filtered_data = []

    for coin in some_data:
        if coin[field_name] is None:
            continue
        filtered_data.append(coin)
        
    sorted_data = sorted(
        filtered_data,
        key=lambda coin: coin[field_name],
        reverse=reverse
    )

    return sorted_data[:top_n]


def sum_market_cap(data):
    result = 0

    for i in range(len(data)):
        result += data[i]['market_cap']

    return result


def create_crypto_table(coins, title, color):
    table = Table(title=title)

    table.add_column('Монета')
    table.add_column('Символ')
    table.add_column('Изменение за 24ч')

    for coin in coins:
        table.add_row(
            f'[{color}]{coin["name"]}[/{color}]',
            f'[{color}]{coin["symbol"]}[/{color}]',
            f'[{color}]{coin["price_change_percentage_24h"]}[/{color}]'
        )

    return table