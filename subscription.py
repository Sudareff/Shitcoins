import web3.eth

from helpers import *

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
nullAddress = "0x0000000000000000000000000000000000000000"

multiCallRouter1 = "0xac9650d8"
multiCallRouter2 = "0x5ae401dc"

addLiquidityStable = "0xe8e33700"
openTrading = "0xc9567bf9"

lockTokens = "0x7d533c1e"

addLiquidity = ""
addLiquidityETH = "0xf305d719"
removeLiquidity = ""
removeLiquidityETH = ""
removeLiquidityETHSupportingFeeOnTransferTokens = ""
removeLiquidityETHWithPermit = ""
removeLiquidityETHWithPermitSupportingFeeOnTransferTokens = ""
removeLiquidityWithPermit = "0x2195995c"

swapExactTokensForETHSupportingFeeOnTransferTokens = "0x791ac947"
swapExactTokensForTokensSupportingFeeOnTransferTokens = "0x5c11d795"
swapExactETHForTokensSupportingFeeOnTransferTokens = "0xb6f9de95"
swapExactETHForTokens = "0x7ff36ab5"
swapExactTokensForETH = "0x18cbafe5"
swapExactTokensForTokens = "0x38ed1739"
swapETHForExactTokens = "0xfb3bdb41"
swapTokensForExactETH = "0x4a25d94a"
swapTokensForExactTokens = "0x8803dbee"
uniswap_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

# def decode_command(code):
#     dict_code_to_name = {'0x80': 'FLAG_ALLOW_REVERT', '0x3f': 'COMMAND_TYPE_MASK', '0x00': 'V3_SWAP_EXACT_IN', '0x01': 'V3_SWAP_EXACT_OUT', '0x02': 'PERMIT2_TRANSFER_FROM', '0x03': 'PERMIT2_PERMIT_BATCH', '0x04': 'SWEEP', '0x05': 'TRANSFER', '0x06': 'PAY_PORTION', '0x08': 'V2_SWAP_EXACT_IN', '0x09': 'V2_SWAP_EXACT_OUT', '0x0a': 'PERMIT2_PERMIT', '0x0b': 'WRAP_ETH', '0x0c': 'UNWRAP_WETH', '0x0d': 'PERMIT2_TRANSFER_FROM_BATCH',
#                          '0x0e': 'BALANCE_CHECK_ERC20', '0x10': 'SEAPORT_V1_5', '0x11': 'LOOKS_RARE_V2', '0x12': 'NFTX', '0x13': 'CRYPTOPUNKS', '0x15': 'OWNER_CHECK_721', '0x16': 'OWNER_CHECK_1155', '0x17': 'SWEEP_ERC721', '0x18': 'X2Y2_721', '0x19': 'SUDOSWAP', '0x1a': 'NFT20', '0x1b': 'X2Y2_1155', '0x1c': 'FOUNDATION', '0x1d': 'SWEEP_ERC1155', '0x1e': 'ELEMENT_MARKET', '0x20': 'SEAPORT_V1_4', '0x21': 'EXECUTE_SUB_PLAN', '0x22': 'APPROVE_ERC20'}
#     return dict_code_to_name[code]


# def decode_inputs(code):
# pass


def get_method_name(method_id):
    match method_id:
        case "0xf305d719":
            method_name = "addLiquidityETH"
        case "0x791ac947":
            method_name = "swapExactTokensForETHSupportingFeeOnTransferTokens"
        case "0x5c11d795":
            method_name = "swapExactTokensForTokensSupportingFeeOnTransferTokens"
        case "0xb6f9de95":
            method_name = "swapExactETHForTokensSupportingFeeOnTransferTokens"
        case "0x7ff36ab5":
            method_name = "swapExactETHForTokens"
        case "0x18cbafe5":
            method_name = "swapExactTokensForETH"
        case "0x38ed1739":
            method_name = "swapExactTokensForTokens"
        case "0xfb3bdb41":
            method_name = "swapETHForExactTokens"
        case "0x4a25d94a":
            method_name = "swapTokensForExactETH"
        case "0x8803dbee":
            method_name = "swapTokensForExactTokens"
        case "0xac9650d8":
            method_name = "Multicall"
        case "0x5ae401dc":
            method_name = "Multicall"
        case "0xe8e33700":
            method_name = "addLiquidityStable"
        case _:
            method_name = "broken"

    return method_name


async def get_transaction_by_hash(tx_hash):
    w3 = Web3(Web3.HTTPProvider(dictChainToRpc["Ethereum"]))
    transaction = w3.eth.get_transaction(tx_hash)
    print(tx_hash)
    # input_data = (transaction.input)[2:].hex()
    # print(f'input_data: {input_data}')
    # pool_abi = ''

    # if tx['from'] == uniswap_address or tx['to'] == uniswap_address:
    #     print(tx_hash)

    # contract = w3.eth.contract(address=uniswap_address, abi=uniswap_abi)
    # decoded_input = contract.decode_function_input(transaction.input.hex())

    # # if data[:10] == '0xac9650d8' or data[:10] == '0x5ae401dc':
    # #     print("Multicall: ", tx_hash)

    # d = {}

    # if params != 0:
    #     print(params)


# function decodeInputMulticall(data) {
#     let resArray = [], funcArray = [];

#     data = data.slice(10 + 64, data.length);

#     let pointer = parseInt(data.slice(0 ,64), 16) * 2;
#     let arrayLen = parseInt(data.slice(64, 128), 16);
#     let offsetPtr, sz;
#     for (let i = 0; i < arrayLen; i++) {
#         offsetPtr = parseInt(data.slice(pointer + i * 64, pointer + (i+1) * 64), 16) * 2;
#         sz = parseInt(data.slice(pointer + offsetPtr, pointer + offsetPtr + 64), 16) * 2;
#         funcArray.push(data.slice(pointer + offsetPtr + 64, pointer + offsetPtr + 64 + sz));
#     }

#     for (let elem of funcArray) {
#         resArray.push(decodeInput(elem));
#     }

#     return resArray;
# }


def main():
    try:
        API_KEY = "4b7ab4b6302d49759b0cc19a546c4455"
        uri = "https://spring-wiser-general.discover.quiknode.pro/75b26e0702193303abbef416fdf4a13bd533f2ca/"
        ssl_context = ssl._create_unverified_context()

        async def subscribe(uri):
            subscribe_message = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "eth_subscribe",
                    "params": ["newPendingTransactions"],
                }
            )

            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                await websocket.send(subscribe_message)
                async for message in websocket:
                    try:
                        tx_hash = json.loads(message)["params"]["result"]
                        await get_transaction_by_hash(tx_hash)
                    except:
                        pass

        asyncio.get_event_loop().run_until_complete(
            subscribe(f"wss://mainnet.infura.io/ws/v3/{API_KEY}")
        )
    except Exception as e:
        pass


if __name__ == "__main__":
    while True:
        main()


# (Uniswap: Universal Router)
# Uniswap V2: Router 2
# Mev bot
# Unibot: Router
# 1inch v5: Aggregation Router
