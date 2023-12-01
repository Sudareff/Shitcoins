from buying import *
from helpers import *
from collections import deque
from datetime import datetime, timedelta

def get_check_sum(address):
    web3 = Web3(Web3.HTTPProvider(dictChainToRpc["Ethereum"]))
    check_sum = ""
    try:
        check_sum = web3.to_checksum_address(address)
    except:
        pass
    return check_sum

address_queue = deque()
black = set()
class Strategy:
    def __init__(self, threshhold):
        self.threshhold = threshhold
        self.current_positions = {}
        self.net = 'Ethereum'
        self.web3 = Web3(Web3.HTTPProvider(dictChainToRpc[self.net]))
        self.address_queue = deque()
        self.profit = 0


    async def monitor_price(self):
        while True:
            for token_address in list(self.current_positions.keys()):
                pool_address = get_pool(self.net, self.web3, token_address)
                decimal = get_decimal(self.net, self.web3, token_address)
                symbol = get_symbol(self.net, self.web3, token_address)
                token_balance = int(self.current_positions[token_address])
                min_amt = get_min_amt(self.net, self.web3, pool_address, token_address, decimal, token_balance, False) * 10**-18
                if min_amt > self.threshhold * dictChainToAmt[self.net]:
                    log(f'READY TO SELL {symbol}, SWAPPING {token_balance} {symbol} FOR MIN {min_amt} ETH at Strategy {self.threshhold}')
                    self.profit += min_amt
                    del self.current_positions[token_address]
                    log(f'CURRENT PROFIT = {self.profit} for Strategy {self.threshhold}')
            await asyncio.sleep(10)

strategies = [Strategy(1), Strategy(1.3), Strategy(1.6), Strategy(1.9), Strategy(2.2)]

async def download_data():
    global address_queue
    while True:
        if datetime.now().second % 5 == 2:
            try:
                with open('data.json', 'r') as f:
                    for x in  json.load(f):
                        if not x[0] in black:
                            address_queue.append((x[0], datetime.fromtimestamp(x[1])))
                            black.add(x[0])

                log(f'Loaded data {address_queue}')
                await asyncio.sleep(60)
            except:
                pass

async def process_queue():
    global address_queue
    while True:
        if address_queue:
            address, time_added = address_queue[0]
            current_time = datetime.now()
            if current_time >= time_added + timedelta(seconds=120):
                address, time_added = address_queue.popleft()
                log(f'Processing address: {address} at {current_time}, added time = {time_added}')
                time_added = time_added.timestamp()
                await process_address(address, int(time_added * 1000))
        await asyncio.sleep(60)

async def process_address(address, start_time):
    if get_symbol(net, web3, address) == "UNI-V2":
        pool_address = address
        token_address = get_token(net, web3, pool_address)
    elif get_symbol(net, web3, get_pool(net, web3, address)) == "UNI-V2":
        pool_address = get_pool(net, web3, address)
        token_address = address

    if not scam_check(token_address, str(start_time), 5):
        log("SCAM")
        return
    
    decimal = get_decimal(net, web3, token_address)
    symbol = get_symbol(net, web3, token_address)
    min_amt = get_min_amt(net, web3, pool_address, token_address, decimal, dictChainToAmt[net], True) * 10**-decimal
    log(f'READY TO BUY " {symbol}, SWAPPING {dictChainToAmt[net]} ETH FOR MIN {min_amt} {symbol} for all Strategies')

    for st in strategies:
        st.profit -= dictChainToAmt[net]
        st.current_positions[token_address] = min_amt
        log(f'CURRENT PROFIT = {st.profit} for Strategy {st.threshhold}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(download_data())
    loop.create_task(process_queue())
    for strategy in strategies:
        loop.create_task(strategy.monitor_price())
    loop.run_forever()
