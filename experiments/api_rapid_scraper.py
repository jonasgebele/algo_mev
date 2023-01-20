import asyncio
import time
import requests

async def getDateTimeFromAPIWithDelay(url):
    while True:
        start = time.perf_counter()        
        response = requests.get(url).json()
        time_in_seconds =  response["dateTime"].split(":")[-1]
        print(time_in_seconds)
        end = time.perf_counter()
        diff = end - start
        await asyncio.sleep(1-(diff+0.005))

async def sendAsyncAtRatePerSecond(url, units):
    startup_interval_delays = [round(unit * (1/units), 4) for unit in range(units)]
    for i in startup_interval_delays:
        time.sleep(i)
        _ = asyncio.Task(getDateTimeFromAPIWithDelay(url))
    await asyncio.sleep(9999999999999)

def main():
    url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Berlin"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendAsyncAtRatePerSecond(url, 10))

if __name__ == "__main__":
    main()
