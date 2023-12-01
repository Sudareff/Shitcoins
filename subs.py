from web3.exceptions import TransactionNotFound
from web3 import AsyncWeb3, AsyncHTTPProvider
import ssl
from web3 import Web3, WebsocketProvider, HTTPProvider, AsyncWeb3, AsyncHTTPProvider
import json
import requests
import aiohttp
import time
import asyncio
import web3
import concurrent.futures
from web3 import Web3
from helpers import *
from time import sleep

url = "https://spring-wiser-general.discover.quiknode.pro/75b26e0702193303abbef416fdf4a13bd533f2ca/"


UNISWAP_ROUTER02_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
UNISWAP_UNIVERSAL_ROUTER_ADDRESS = "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"

UNI_SWAPROUTER02_ABI = read_json("uniswap_router_abi.json")


ssl_context = ssl._create_unverified_context()

w3 = AsyncWeb3(
    AsyncHTTPProvider(
        "https://spring-wiser-general.discover.quiknode.pro/75b26e0702193303abbef416fdf4a13bd533f2ca/",
        {"ssl": ssl_context},
    )
)

uniswap_router02_contract = w3.eth.contract(
    address=UNISWAP_ROUTER02_ADDRESS, abi=UNI_SWAPROUTER02_ABI
)


async def handle_event(event):
    tx_hash = event.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        print(tx.to)
    except TransactionNotFound:
        print("Transaction not found")


async def log_loop(event_filter, poll_interval):
    while True:
        for event in await event_filter.get_new_entries():
            await handle_event(event)
        await asyncio.sleep(poll_interval)


async def main():
    tx_filter = await w3.eth.filter("pending")
    await log_loop(tx_filter, 1)


if __name__ == "__main__":
    asyncio.run(main())
