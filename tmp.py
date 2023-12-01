from uniswap_universal_router_decoder import RouterCodec
from web3 import Web3, HTTPProvider
from time import sleep
from web3 import Web3
from helpers import *
import threading
from collections import deque

url = "https://mainnet.infura.io/v3/32f8a92827ff4a66be3d3b89c7034d46"
w3 = Web3(Web3.HTTPProvider(url))

codec = RouterCodec()

w3 = Web3(HTTPProvider(dictChainToRpc["Ethereum"]))
UNISWAP_ROUTER02_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
UNISWAP_ROUTER02_ABI = read_json("uniswap_router_abi.json")
UNISWAP_ROUTER02_CONTRACT = w3.eth.contract(
    address=UNISWAP_ROUTER02_ADDRESS, abi=UNISWAP_ROUTER02_ABI
)

UNISWAP_UNIVERSAL_ROUTER_ADDRESS = "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"
UNISWAP_UNIVERSAL_ROUTER_ABI = read_json("uniswap_universal_router_abi.json")
UNISWAP_UNIVERSAL_ROUTER_CONTRACT = w3.eth.contract(
    address=UNISWAP_UNIVERSAL_ROUTER_ADDRESS, abi=UNISWAP_UNIVERSAL_ROUTER_ABI
)


# средняя скользащая цена газа за последние k транзакций
# словарь для нее token -> цена газа
# honeypot check
# backtest
#

tokens = [w3.to_checksum_address("0x43D7E65B8fF49698D9550a7F315c87E67344FB59")]
WETH = w3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")

last_transactions_fee_buy = {token: deque(maxlen=10) for token in tokens}
last_transactions_fee_sell = {token: deque(maxlen=10) for token in tokens}


def get_transaction_type(path):
    if len(path) == 2:
        if path[0] == WETH:
            return "buy"
        elif path[1] == WETH:
            return "sell"


def get_mean_gas_price(token, type):
    if type == "buy":
        return sum(last_transactions_fee_buy[token]) / len(
            last_transactions_fee_buy[token]
        )
    elif type == "sell":
        return sum(last_transactions_fee_sell[token]) / len(
            last_transactions_fee_sell[token]
        )


def find_tokens_in_data(input):
    start_index = input.find("path")
    if start_index == -1:
        return []
    lenght = input[start_index:].find("]")
    if lenght == -1:
        return []
    array = input[start_index + 8 : start_index + lenght]
    if array[0] == '"':
        return []
    array = array.replace("'", "")
    array = array.split(", ")
    return array


def fetch_tx_pool():
    black = set()
    while True:
        tx_pool = w3.eth.get_block("pending", full_transactions=True)
        for tx in tx_pool.transactions:
            if (
                tx.to == UNISWAP_ROUTER02_ADDRESS
                or tx.to == UNISWAP_UNIVERSAL_ROUTER_ADDRESS
            ):
                try:
                    res = find_tokens_in_data(
                        str(codec.decode.function_input(tx.input))
                    )
                    for token in res:
                        if tx.hash not in black and get_transaction_type(res) == "buy":
                            gas_price = tx.gasPrice * 1e-9
                            last_transactions_fee_buy[token].append(gas_price)
                            print(last_transactions_fee_buy)
                            black.add(tx.hash)
                        if tx.hash not in black and get_transaction_type(res) == "sell":
                            gas_price = tx.gasPrice * 1e-9
                            last_transactions_fee_sell[token].append(gas_price)
                            print(last_transactions_fee_sell)
                            black.add(tx.hash)
                except Exception as e:
                    res = find_tokens_in_data(
                        str(UNISWAP_ROUTER02_CONTRACT.decode_function_input(tx.input))
                    )
                    for token in res:
                        if tx.hash not in black and get_transaction_type(res) == "buy":
                            gas_price = tx.gasPrice * 1e-9
                            last_transactions_fee_buy[token].append(gas_price)
                            print(last_transactions_fee_buy)
                            black.add(tx.hash)
                        if tx.hash not in black and get_transaction_type(res) == "sell":
                            gas_price = tx.gasPrice * 1e-9
                            last_transactions_fee_sell[token].append(gas_price)
                            print(last_transactions_fee_sell)
                            black.add(tx.hash)
        sleep(0.02)


# # Create a thread to run fetch_tx_pool function in the background
# tx_thread = threading.Thread(target=fetch_tx_pool)
# # Start the thread
# tx_thread.start()


input = '0x7ff36ab500000000000000000000000000000000000000000000000000000000000245240000000000000000000000000000000000000000000000000000000000000080000000000000000000000000962558e166e1aa38a67ea9c0b2eeee172d69d3b90000000000000000000000000000000000000000000000000000000064e8b28c0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

print(str(UNISWAP_ROUTER02_CONTRACT.decode_function_input(input)))