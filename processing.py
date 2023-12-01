from buying import *


def check_chain(address, net):
    web3 = Web3(Web3.HTTPProvider(dictChainToRpc[net]))
    try:
        token_contract = web3.eth.contract(
            address, abi=erc20Abi, decode_tuples=True)
        symbol = token_contract.functions.symbol().call()
    except Exception as e:
        print(e)
        return False
    return True


def process(address):
    if check_chain(address, 'Ethereum'):
        net = 'Ethereum'
        web3 = Web3(Web3.HTTPProvider(dictChainToRpc[net]))
        buy(net, web3, address)
    # elif check_chain(address, 'BNB Smart Chain (BEP20)'):
    #     net = 'BNB Smart Chain (BEP20)'
    #     web3 = Web3(Web3.HTTPProvider(dictChainToRpc[net]))
    #     buy(net, web3, address, channel)
    else:
        print("NO")


print('processing loaded')
