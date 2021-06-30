import json
import discord
import web3
from uniswap import Uniswap
from token_address import address
from dotenv import dotenv_values
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testnet', action='store_true')
cmd_args = parser.parse_args()
print(f'using testnet: {cmd_args.testnet}')
config = dotenv_values('production.env')

TESTNET = False
VERSION = config['UNISWAP_VERSION']
WALLET_ADDRESS = config['WALLET_ADDRESS']
WALLET_PRIVATE_KEY = config['WALLET_SECRET']

if cmd_args.testnet:
    PROVIDER = f"https://rinkeby.infura.io/v3/{config['INFURA_ID']}"
else:
    PROVIDER = f"https://mainnet.infura.io/v3/{config['INFURA_ID']}"

MY_TOKEN = config['TOKEN']

uniswap = Uniswap(WALLET_ADDRESS, WALLET_PRIVATE_KEY, version=int(VERSION), provider=PROVIDER)
client = discord.Client()

@client.event
async def on_ready():
    print(f'we have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        message_content = message.content[1:]
        message_content = message_content.split(' ')
        if message_content[0] == 'price':
            symbol = message_content[1]

            await message.channel.send(f'Getting price for {symbol}...')
            price = uniswap.get_price_input(address['eth'], address['dai'], 1*10**18)/(10**18)
            await message.channel.send(f'{price}')


if __name__ == '__main__':
    client.run(MY_TOKEN)