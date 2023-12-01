import requests
import time
from datetime import datetime, timedelta

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


def get_pair(token):
    pass


def get_initial_volume(pair, start, minutes = 5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    base = "https://io.dexscreener.com/dex/chart/amm/uniswap/bars/ethereum/"
    end = str(min(60000 * minutes + int(start), int(time.time()) * 1000))
    url = base + pair + "?from=" + start + "&to=" + end + "&res=1&cb=6" + "&q=" + WETH
    r = requests.get(url, headers=headers).json()

    volume = 0

    for i in r["bars"]:
        volume += float(i["volumeUsd"])

    print(volume)
    print(f'time: {datetime.fromtimestamp(int(r["bars"][0]["timestamp"]) / 1000)} {datetime.fromtimestamp(int(r["bars"][-1]["timestamp"]) / 1000)}')

    return volume


def scam_check(token, start="0", minutes=5):
    try: 
        url = "https://api.honeypot.is/v2/IsHoneypot"
        params = {"address": token}
        headers = {"X-API-KEY": ""}

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            pair = json_data["pairAddress"]
            is_honeypot = json_data["honeypotResult"]["isHoneypot"]

            buy_tax = json_data['simulationResult']['buyTax']
            sell_tax = json_data['simulationResult']['sellTax']
            transfer_tax = json_data['simulationResult']['transferTax']
            

        initial_volume = get_initial_volume(pair, start, minutes)  
        return (
            not is_honeypot
            and buy_tax <= 10
            and sell_tax <= 10
            and transfer_tax <= 10
            and initial_volume > 100
        )
    except Exception as e:
        print(e)
        return False
