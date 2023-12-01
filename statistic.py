from uniswap_universal_router_decoder import RouterCodec
from web3 import Web3, HTTPProvider
from time import sleep
from web3 import Web3
from helpers import *
from datetime import datetime
import pytz
import random
import threading

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


def process_transaction(tx):
    try:
        if tx.to == UNISWAP_UNIVERSAL_ROUTER_ADDRESS:
            decoded_tx_input = codec.decode.function_input(tx.input)
            for elem in decoded_tx_input[1]["inputs"]:
                for elen in elem:
                    try:
                        if "path" in elen:
                            path = elen["path"]
                            if type(path) == list:
                                for address in path:
                                    print(
                                        "Found address: ",
                                        address,
                                        " in tx: ",
                                        tx.hash.hex(),
                                    )
                    except TypeError as e:
                        pass
                    except Exception as e:
                        print(e)

        elif tx.to == UNISWAP_ROUTER02_ADDRESS:
            decoded_tx_input = UNISWAP_ROUTER02_CONTRACT.decode_function_input(tx.input)
            if "path" in decoded_tx_input[1]:
                for address in decoded_tx_input[1]["path"]:
                    print("Found address:", address, "in tx:", tx.hash.hex())
    except Exception as e:
        print("Exception: ", e)


token = w3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")


def find_token_in_data(token, input):
    start_index = input.find("path")
    if start_index == -1:
        return -1
    lenght = input[start_index:].find("]")
    if lenght == -1:
        return -1
    array = input[start_index + 8 : start_index + lenght]
    if array[0] == '"':
        return -1
    array = array.replace("'", "")
    array = array.split(", ")
    if token in array:
        return 1


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
                    res = find_token_in_data(
                        token, str(codec.decode.function_input(tx.input))
                    )
                    if res == 1 and tx.hash not in black:
                        print(tx.gasPrice * 1e-9, tx.hash.hex())
                        black.add(tx.hash)
                except Exception as e:
                    res = find_token_in_data(
                        token,
                        str(UNISWAP_ROUTER02_CONTRACT.decode_function_input(tx.input)),
                    )
                    if res == 1 and tx.hash not in black:
                        print(tx.gasPrice * 1e-9, tx.hash.hex())
                        black.add(tx.hash)
        sleep(0.02)


# Create a thread to run fetch_tx_pool function in the background
tx_thread = threading.Thread(target=fetch_tx_pool)

# Start the thread
tx_thread.start()

for i in range(100):
    print("Main thread is running")
    sleep(1)
