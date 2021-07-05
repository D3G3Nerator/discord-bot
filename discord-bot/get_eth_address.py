# Install coingecko api:
# pip install pycoingecko

import json
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# To add coins manually:
# erc20_addresses['tether'] = cg.get_coin_by_id(id='tether')['platforms']['ethereum']

# Coingecko has a rate limit of 50 request per min
# so max per_page is 50
# change page number to get the next 50 coins
listOfCoins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page='50', page='1')

erc20_addresses_dict = {}

for i in listOfCoins:
    coin = cg.get_coin_by_id(id=i['id'], localization='false', tickers='false', market_data='false', community_data='false', developer_data='false', sparkline='false')
    print(i)
    if coin['asset_platform_id'] == 'ethereum':
        erc20_addresses_dict[i['symbol']] = coin['platforms']['ethereum']

# print(erc20_addresses)

# json object
json_obj = json.dumps(erc20_addresses_dict)

# Outputs a .txt file
with open('erc20_address.json', 'w') as json_file:
  json.dump(erc20_addresses_dict, json_file)