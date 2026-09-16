import json
import sys


from rich.console import Console
from rich.table import Table
from datetime import datetime

from support import load_crypto_data, get_top_coins, sum_market_cap


console = Console()

try:
    with console.status('Загружаю данные...'):
        data = load_crypto_data()
except RuntimeError:
    console.print('Ошибка подключения/получения данных от API')
    sys.exit()


Top_3_max = get_top_coins(data, 'price_change_percentage_24h', 3, True)
Top_3_min = get_top_coins(data, 'price_change_percentage_24h', 3)
max_total_volume = get_top_coins(data, 'total_volume', 1, True)
result_summ = sum_market_cap(data)
    
table_height = Table(title='Топ-3 роста')
table_height.add_column('Монета')
table_height.add_column('Символ')
table_height.add_column('Изменение за 24ч')

for coin in Top_3_max:
    table_height.add_row(
        f"[green]{coin['name']}[/green]",
        f"[green]{coin['symbol']}[/green]",
        f"[green]{coin['price_change_percentage_24h']}[/green]"
        )

table_fall = Table(title='Топ-3 падения')
table_fall.add_column('Монета')
table_fall.add_column('Символ')
table_fall.add_column('Изменение за 24ч')

for coin in Top_3_min:
    table_fall.add_row(
        f"[red]{coin['name']}[/red]",
        f"[red]{coin['symbol']}[/red]",
        f"[red]{coin['price_change_percentage_24h']}[/red]"
        )

console.print(table_height)
console.print(table_fall)

generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

top_gainers = []
for coin in Top_3_max:
    new_dict = {}
    new_dict['name'] = coin['name']
    new_dict['symbol'] = coin['symbol']
    new_dict['change_24h'] = coin['price_change_percentage_24h']
    top_gainers.append(new_dict)

top_losers = []
for coin in Top_3_min:
    new_dict = {}
    new_dict['name'] = coin['name']
    new_dict['symbol'] = coin['symbol']
    new_dict['change_24h'] = coin['price_change_percentage_24h']
    top_losers.append(new_dict)

highest_volume_coin = max_total_volume[0]
highest_volume = {
    'name': highest_volume_coin['name'],
    'symbol': highest_volume_coin['symbol'],
    'volume_usd': highest_volume_coin['total_volume']
}

report = {
    'generated_at': generated_at,
    'total_coins_analyzed': len(data),
    'total_market_cap_usd': result_summ,
    'top_gainers': top_gainers,
    'top_losers': top_losers,
    'highest_volume': highest_volume
  }

with open('crypto_report.json', 'w') as file:
    json.dump(report, file, indent=4, ensure_ascii=False)
