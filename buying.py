from helpers import *
from scam_cheker import *

def get_symbol(net, web3, address):
    contract = web3.eth.contract(address, abi=erc20Abi, decode_tuples=True)
    symbol = contract.functions.symbol().call()
    return symbol


def get_decimal(net, web3, address):
    contract = web3.eth.contract(address, abi=erc20Abi, decode_tuples=True)
    decimal = contract.functions.decimals().call()
    return decimal


def get_balance(net, web3, token_address):
    token_contract = web3.eth.contract(token_address, abi=erc20Abi, decode_tuples=True)
    balance = token_contract.functions.balanceOf(publicKey).call()
    return balance


def get_pool(net, web3, token_address):
    quote_address = dictChainToWeth[net]
    pair_address = (
        web3.eth.contract(address=dictChainToFactoryV2[net], abi=factoryAbiV2)
        .functions.getPair(quote_address, token_address)
        .call()
    )
    if pair_address != "0x0000000000000000000000000000000000000000":
        return pair_address
    return -1


def get_token(net, web3, pool_address):
    try:
        contract = web3.eth.contract(address=pool_address, abi=poolAbiV2)
        token = contract.functions.token0().call()

        if token == dictChainToWeth[net]:
            token = contract.functions.token1().call()

        return token
    except:
        return -1


def get_min_amt(net, web3, pool_address, token_adress, decimal, amount, is_buy):
    pool_contract = web3.eth.contract(address=pool_address, abi=poolAbiV2)
    reserves = pool_contract.functions.getReserves().call()
    token0 = pool_contract.functions.token0().call()

    if token_adress != token0:
        x = reserves[0] * 10**-18
        y = reserves[1] * 10**-decimal
    else:
        x = reserves[1] * 10**-18
        y = reserves[0] * 10**-decimal
    if not is_buy:
        x, y = y, x
        decimal = 18

    dx = amount
    price = y * 0.997 * dx / (x + 0.997 * dx)
    return int(price * slippage * 10**decimal)


def buy(net, web3, pool_address, token_address):
        decimal = get_decimal(net, web3, token_address)
        min_amt = get_min_amt(
            net, web3, pool_address, token_address, decimal, dictChainToAmt[net], True
        )
        swap_contract = web3.eth.contract(
            dictChainToSwapV2[net], abi=swapAbiV2, decode_tuples=True
        )
        deadline = int(time.time()) + 300
        gas_price_now = int(web3.eth.gas_price * gasMultiplier)
        gas_price_max = web3.to_wei(maxGas, "gwei")

        if gas_price_now > gas_price_max:
            print("GAS PRICE TOO HIGH")
            return

        tx_to_swap = swap_contract.functions.swapExactETHForTokens(
            min_amt, (dictChainToWeth[net], token_address), publicKey, deadline
        ).build_transaction(
            {
                "nonce": web3.eth.get_transaction_count(publicKey),
                "gas": 300000,
                "gasPrice": gas_price_now,
                "value": web3.to_wei(dictChainToAmt[net], "ether"),
            }
        )

        # signed_tx = web3.eth.account.sign_transaction(tx_to_swap, privateKey)
        # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # web3.eth.wait_for_transaction_receipt(tx_hash)

        # text_bought = ""
        # text_bought += f"Bought {symbol}\n"
        # text_bought += f'Status = {web3.eth.get_transaction_receipt(tx_hash)["status"]}, hash = {tx_hash.hex()}'
        # log(text_bought)


def sell(net, web3, token_address, token_balance):
    pool_address = get_pool(net, web3, token_address)

    if pool_address != -1:
        decimal = get_decimal(net, web3, token_address)
        # token_balance = get_balance(net, web3, token_address)
        swap_contract = web3.eth.contract(
            dictChainToSwapV2[net], abi=swapAbiV2, decode_tuples=True
        )
        deadline = int(time.time()) + 300
        gas_price_now = int(web3.eth.gas_price * gasMultiplier)
        min_amt = get_min_amt(
            net, web3, pool_address, token_address, decimal, token_balance, False
        )
        tx_to_swap = swap_contract.functions.swapExactTokensForETH(
            token_balance * 10**decimal,
            min_amt,
            (token_address, dictChainToWeth[net]),
            publicKey,
            deadline,
        ).build_transaction(
            {
                "nonce": web3.eth.get_transaction_count(publicKey),
                "gas": 300000,
                "gasPrice": gas_price_now,
            }
        )

        # signed_tx = web3.eth.account.sign_transaction(tx_to_swap, privateKey)
        # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # web3.eth.wait_for_transaction_receipt(tx_hash)

        # text_sold = ''
        # text_sold += f'Sold {symbol}\n'
        # text_sold += f'Status = {web3.eth.get_transaction_receipt(tx_hash)["status"]}, hash = {tx_hash.hex()}'
        # log(text_sold)


print("buying loaded")

net = "Ethereum"
web3 = Web3(Web3.HTTPProvider(dictChainToRpc[net]))
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
token_address = USDC

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

# buy(net, web3, get_pool(net, web3, token_address), token_address)

# sell(net, web3, token_address)
