from data_handler import *

address_queue = []

client = TelegramClient("abob", api_id, api_hash)
client.start()

@client.on(events.NewMessage("@DEXTNewPairsBot"))
@client.on(events.NewMessage('@mockchmock'))
async def event_handler(event):
    log('New message received')
    await handle_event(event)

async def handle_event(event):
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
                log(f'Queueing address: {address} from channel: {channel}')
                
                current_time = datetime.now()
                address_queue.append((address, current_time.timestamp()))
    except:
        pass


async def load_data():
    global address_queue
    while True:
        if address_queue and datetime.now().second % 5 == 0:
            with open('data.json', 'w') as f:
                json.dump([x for x in address_queue], f)
            log(f'Saved data {address_queue}') 
            address_queue = deque()
            await asyncio.sleep(60)
        await asyncio.sleep(1)
    

if __name__ == '__main__':
    log('Starting...')
    loop = asyncio.get_event_loop()
    loop.create_task(load_data())
    loop.run_until_complete(client.run_until_disconnected())