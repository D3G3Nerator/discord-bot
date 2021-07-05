import json
import discord
from web3 import Web3
from uniswap import Uniswap
from dotenv import dotenv_values
import argparse
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testnet', action='store_true')
cmd_args = parser.parse_args()
print(f'using testnet: {cmd_args.testnet}')
config = dotenv_values('production.env')

TESTNET = False
VERSION = config['UNISWAP_VERSION']
WALLET_ADDRESS = config['WALLET_ADDRESS']
WALLET_PRIVATE_KEY = config['WALLET_SECRET']
with open('erc20_address.json') as file:
    ERC20_ADDRESSES = json.load(file)

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
        action = message_content[0]
        if action == 'price':
            symbol = message_content[1]

            await message.channel.send(f'Getting price for {symbol}...')
            base_symbol = symbol.split('/')[0]
            quote_symbol = symbol.split('/')[1]
            try:
                base_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[base_symbol.lower()])
                quote_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[quote_symbol.lower()])
                if quote_symbol == 'usdc':
                    input_amount = uniswap.get_price_input(base_symbol_address, quote_symbol_address, 1*10**18)/(10**6)
                else:
                    input_amount = uniswap.get_price_input(base_symbol_address, quote_symbol_address, 1*10**18)/10**18
            except Exception as e:
                print(e.with_traceback())
                await message.channel.send(f'unable to find pair {symbol}')
                return
            await message.channel.send(f'{input_amount}')
            return
            
        elif action == 'buy':
            size = message_content[1]
            symbol = message_content[2]
            try:
                size = float(size)
            except ValueError:
                await message.channel.send(f'unable to parse size {size} into float')
            print(size)
            base_symbol = symbol.split('/')[0]
            quote_symbol = symbol.split('/')[1]
            base_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[base_symbol.lower()])
            quote_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[quote_symbol.lower()])
            try:   
                if quote_symbol == 'usdc':
                    input_amount = size*10**18/uniswap.get_price_output(base_symbol_address, quote_symbol_address, int(size*10**6))
                else:
                    input_amount = size*10**18/uniswap.get_price_output(base_symbol_address, quote_symbol_address, int(size*10**18))
                    
                print(f'need {input_amount} amount of {quote_symbol} in order to buy {size} amount of {base_symbol}')
                trade = uniswap.make_trade_output(base_symbol_address, quote_symbol_address, int(input_amount))
                print(f'trade completed: {trade}')
            except Exception as e:
                traceback.print_exc()
                await message.channel.send(e)
        elif action == 'sell':
            size = message_content[1]
            symbol = message_content[2]
            try:
                size = float(size)
            except ValueError:
                await message.channel.send(f'unable to parse size {size} into float')
            base_symbol = symbol.split('/')[0]
            quote_symbol = symbol.split('/')[1]
            base_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[base_symbol.lower()])
            quote_symbol_address = Web3.toChecksumAddress(ERC20_ADDRESSES[quote_symbol.lower()])
            
            try:   
                if quote_symbol == 'usdc':
                    trade = uniswap.make_trade(base_symbol_address, quote_symbol_address, int(size*10**6))
                    
                else:
                    trade = uniswap.make_trade(base_symbol_address, quote_symbol_address, int(size*10**18))
                    
                print(f'trade completed: {trade}')
                
            except Exception as e:
                traceback.print_exc()
                await message.channel.send(e)
                
            
            pass
        
        if action == 'sell':
            symbol = message_content[1]
            pass


if __name__ == '__main__':
    client.run(MY_TOKEN)