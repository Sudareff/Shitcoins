from buying import *
from helpers import *
from collections import deque
from datetime import datetime, timedelta


client = TelegramClient("abob", api_id, api_hash)
client.start()

@client.on(events.NewMessage("@DEXTNewPairsBot"))
@client.on(events.NewMessage('@mockchmock'))
async def event_handler(event):
    print('New message received')
    await handle_event(event)

class Strategy:
    def __init__(self, threshhold):
        self.threshhold = threshhold
        self.current_positions = {}
        self.net = 'Ethereum'
        self.web3 = Web3(Web3.HTTPProvider(dictChainToRpc[self.net]))
        self.address_queue = deque()
        self.profit = 0

    async def handle_event(self, event):
        try:
            channel_instance = await event.get_chat()
            channel = channel_instance.username
            if not channel:
                channel = channel_instance.title
            else:
                channel = "@" + channel

            message = event.message.message
            index = message.find("0x")

            if index != -1:
                address = message[index : index + 42]
                address = get_check_sum(address)
                if address != "":
                    print(f'Queueing address: {address} from channel: {channel} at Strategy {self.threshhold}')
                    
                    current_time = datetime.now()
                    self.address_queue.append((address, current_time))
        except:
            pass

    async def process_queue(self):
        while True:
            await reconnect()
            if self.address_queue:
                address, time_added = self.address_queue[0]
                current_time = datetime.now()

                if current_time >= time_added + timedelta(seconds=120):
                    address, time_added = self.address_queue.popleft()
                    print(f'Processing address: {address} at {current_time}, added time = {time_added} at Strategy {self.threshhold}')
                    time_added = time_added.timestamp()
                    await self.process_address(address, int(time_added * 1000))


    async def process_address(self, address, start_time):
        await reconnect()
        if get_symbol(self.net, self.web3, address) == "UNI-V2":
            pool_address = address
            token_address = get_token(self.net, self.web3, pool_address)
        elif get_symbol(self.net, self.web3, get_pool(self.net, self.web3, address)) == "UNI-V2":
            pool_address = get_pool(self.net, self.web3, address)
            token_address = address
        else:
            print("NO")
            return
        
        if not scam_check(token_address, str(start_time), 5):
            print("SCAM")
            return
        decimal = get_decimal(self.net, self.web3, token_address)
        symbol = get_symbol(self.net, self.web3, token_address)
        min_amt = get_min_amt(self.net, self.web3, pool_address, token_address, decimal, dictChainToAmt[self.net], True) * 10**-decimal
        print(f'READY TO BUY " {symbol}, SWAPPING {dictChainToAmt[net]} ETH FOR MIN {min_amt} {symbol} at Strategy {self.threshhold}')
        self.profit -= dictChainToAmt[self.net]
        self.current_positions[token_address] = min_amt
        print(f'Strategy {self.threshhold}: CURRENT PROFIT = {self.profit}')


    async def monitor_price(self):
        while True:
            await reconnect()
            for token_address in self.current_positions.keys():
                pool_address = get_pool(self.net, self.web3, token_address)
                decimal = get_decimal(self.net, self.web3, token_address)
                symbol = get_symbol(self.net, self.web3, token_address)
                token_balance = int(self.current_positions[token_address])
                min_amt = get_min_amt(self.net, self.web3, pool_address, token_address, decimal, token_balance, False) * 10**-18
                if min_amt > self.threshhold * dictChainToAmt[self.net]:
                    print(f'READY TO SELL {symbol}, SWAPPING {token_balance} {symbol} FOR MIN {min_amt} ETH at Strategy {self.threshhold}')
                    self.profit += min_amt
                    self.current_positions[token_address] = 0
                    print(f'Strategy {self.threshhold}: CURRENT PROFIT = {self.profit}')
            await asyncio.sleep(30)

strategies = [Strategy(1), Strategy(2), Strategy(3), Strategy(4), Strategy(5)]



last_reconnect = datetime.fromtimestamp(0)

async def reconnect():
    global last_reconnect
    global client
    if client.is_connected() and datetime.now() >= last_reconnect + timedelta(seconds=60):
        client.disconnect()
        client.run_until_disconnected()
        last_reconnect = datetime.now()
        print('Client reconnected')

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    tasks = []   


    tasks.append(loop.create_task(reconnect()))

    for strategy in strategies:
        tasks.append(loop.create_task(strategy.process_queue()))
        tasks.append(loop.create_task(strategy.monitor_price()))

    loop.run_until_complete(asyncio.gather(*tasks))

# @client.on(events.NewMessage(channel_tester))
# @client.on(events.NewMessage(-1001650345849)) # eye cross chain
# @client.on(events.NewMessage(-1001515849943))  # chats='@lowtaxethx'
# @client.on(events.NewMessage(-1001557733373))  # chats='@GoldWhiteList')
# @client.on(events.NewMessage(-1001614158986))  # chats='@NyanCatGamble')
# @client.on(events.NewMessage(-1001631609672))  # chats='@lowtaxwolfy')
# @client.on(events.NewMessage(-1001117184677))  # chats='@Kingdom_X100_CALLS'
# # @client.on(events.NewMessage('@DEXTNewPairsBot'))
# @client.on(events.NewMessage('@mad_apes_gambles'))
# # @client.on(events.NewMessage('@jvfoknewrvknero'))
# @client.on(events.NewMessage(-1001515849943))  # chats='@lowtaxethx'
# @client.on(events.NewMessage(-1001557733373))  # chats='@GoldWhiteList')
# @client.on(events.NewMessage(-1001614158986))  # chats='@NyanCatGamble')
# @client.on(events.NewMessage(-1001631609672))  # chats='@lowtaxwolfy')
# @client.on(events.NewMessage(-1001117184677))  # chats='@Kingdom_X100_CALLS'
# @client.on(events.NewMessage('@mad_apes_gambles'))
