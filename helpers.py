import json
from telethon import TelegramClient, events
from web3 import Web3
import time
import requests
import asyncio
import signal
import sys
from datetime import datetime
import websockets
import json
import ssl


def read_json(path):
    with open('/Users/ivansudarev/PycharmProjects/MyShitBot/abis/' + path, 'r') as f:
        return json.load(f)

# UNISWAP ABIS


uniswap_universal_router_abi = read_json('uniswap_universal_router_abi.json')
# /Users/ivansudarev/PycharmProjects/MyShitBot/abis/uniswap_universal_router_abi.json
#
# check if pool
black_list = set()
with open('/Users/ivansudarev/PycharmProjects/MyShitBot/abis/black.txt', 'r') as fp:
    for x in fp.read().split("\n"):
        black_list.add(x)
black_list.clear()


def append_to_black(addr):
    addr = addr.lower()
    print(f'Appending addr {addr} to black_list')
    if addr not in black_list:
        black_list.add(addr)
        with open('/Users/ivansudarev/PycharmProjects/MyShitBot/abis/black.txt', 'a') as f:
            f.write(addr.lower() + '\n')
    black_list.clear()
    return


TEST = True
publicKey = ''
privateKey = ''
slippage = 0.90
gasMultiplier = 1
maxGas = 50

# factoryContractAddr = "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f";
# # factoryContract = new ethers.Contract(factoryContractAddr, factoryABI, eth);
# uniswapV2RouterAddr = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D";
# uniswapV2RouterABI =
# # uniswapV2Contract = new ethers.Contract(uniswapV2RouterAddr, uniswapV2RouterABI, eth);
# pairAbi =
# uniswapAbi =

dictChainToAmt = {'Ethereum': 0.001, 'BNB Smart Chain (BEP20)': 0.00000001}

dictChainToRpc = {"Ethereum": "https://spring-wiser-general.discover.quiknode.pro/75b26e0702193303abbef416fdf4a13bd533f2ca/",
                  'BNB Smart Chain (BEP20)': "https://bsc.meowrpc.com",
                  'Arbitrum': ""}
dictChainToFactory = {'Ethereum': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
                      'BNB Smart Chain (BEP20)': '0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865'}
dictChainToWeth = {'Ethereum': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                   'BNB Smart Chain (BEP20)': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'}
dictChainToUSDT = {'Ethereum': '0xdAC17F958D2ee523a2206206994597C13D831ec7'}
dictChainToSwap = {'Ethereum': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
                   'BNB Smart Chain (BEP20)': '0x13f4EA83D0bd40E75C8222255bc855a974568Dd4'}
dictChainToFactoryV2 = {
    'Ethereum': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'}
dictChainToSwapV2 = {'Ethereum': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'}

factoryAbi = read_json('factoryAbi.json')
factoryAbiV2 = read_json('factoryAbiV2.json')
swapAbiETH = read_json('swapAbiETH.json')
swapAbiBSC = read_json('swapAbiBSC.json')
erc20Abi = read_json('erc20Abi.json')
poolAbiV2 = read_json('poolAbiV2.json')
poolAbiBSC = read_json('poolAbiBSC.json')
poolAbiETH = read_json('poolAbiEth.json')
swapAbiV2 = read_json('swapAbiV2.json')

dictChainToSwapAbi = {'Ethereum': swapAbiETH,
                      'BNB Smart Chain (BEP20)': swapAbiBSC}
fees = [300, 50, 1000]
api_id = 28781919
api_hash = ''
bot_token = ''
bot_chatID = ''


def log(bot_message):
    bot_message = str(bot_message)
    try:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
                    bot_chatID + '&parse_mode=HTML&text=' + bot_message
        response = requests.post(send_text)
    except Exception as e:
        print(f'Error while sending text {bot_message}, error: {e}')


def format_text(additional_text, flash_addr, net, decimal, channel_name):
    text = additional_text
    text += f'\nToken = {flash_addr}\nChain = {net}\nDecimals = {decimal}\nFrom channel = {channel_name}'
    text += f'\n\nDexscreener: https://dexscreener.com/ethereum/{flash_addr}'
    log(text)


print('helpers loaded')
