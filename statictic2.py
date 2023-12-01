from uniswap_universal_router_decoder import RouterCodec
from time import sleep
from web3 import Web3
from helpers import *
from web3 import Web3, HTTPProvider, AsyncWeb3, AsyncHTTPProvider

url = "https://mainnet.infura.io/v3/32f8a92827ff4a66be3d3b89c7034d46"
w3 = Web3(Web3.HTTPProvider(url))
token = w3.to_checksum_address("0xbc184ceb725d2c36e2f28ff11e23fa6cbd037bfe")

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


def get_block_by_number(block_number):
    return w3.eth.get_block(block_number)


addresses = []

dict_cnt = {}
dict_sum = {}


async def process_block(block_number):
    global w3
    global cur_sum
    global cnt
    w3 = AsyncWeb3(AsyncHTTPProvider(url))
    block = await get_block_by_number(block_number)
    for tx in block.transactions:
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
                                        if address in addresses:
                                            cur_sum += tx.gasPrice
                                            cnt += 1
                                            dict_cnt[address] += 1
                                            dict_sum[address] += tx.gasPrice
                                            if dict_cnt[address] == 10:
                                                print(
                                                    f"Average for {address} {dict_sum[address] / 10}"
                                                )
                                                with open(
                                                    "/Users/ivansudarev/PycharmProjects/MyShitBot/gas_logs_new.txt",
                                                    "a",
                                                ) as f:
                                                    f.write(
                                                        f"Average for {address} {dict_sum[address] / 10}\n"
                                                    )
                                            print(
                                                f"1: Current average: {cur_sum / cnt}"
                                            )

                        except TypeError as e:
                            pass
                        except Exception as e:
                            print(e)
            elif tx.to == UNISWAP_ROUTER02_ADDRESS:
                decoded_tx_input = UNISWAP_ROUTER02_CONTRACT.decode_function_input(
                    tx.input
                )
                if "path" in decoded_tx_input[1]:
                    for address in decoded_tx_input[1]["path"]:
                        if address in addresses:
                            cur_sum += tx.gasPrice
                            cnt += 1
                            dict_cnt[address] += 1
                            dict_sum[address] += tx.gasPrice
                            if dict_cnt[address] == 10:
                                print(f"Average for {address} {dict_sum[address] / 10}")
                                with open(
                                    "/Users/ivansudarev/PycharmProjects/MyShitBot/gas_logs_new.txt",
                                    "a",
                                ) as f:
                                    f.write(
                                        f"Average for {address} {dict_sum[address] / 10}\n"
                                    )
                            print(f"2: Current average: {cur_sum / cnt}")
        except Exception as e:
            print("Exception: ", e)
