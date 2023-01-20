import time
import requests
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor, as_completed

def requestAsJSON(url):
    return requests.get(url).json()

def requestTime(url):
    start = time.perf_counter()
    _ = requestAsJSON(url)
    end = time.perf_counter()
    return end - start

def requestWithDelay(url, delay):
    time.sleep(delay)
    return requestAsJSON(url)

def sendRequestsAtRatePerSecond(ratePerSecond, url):
    sleep_interval = 1 / ratePerSecond
    times = [round(x*0.01, 2) for x in range(0, ratePerSecond)]

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(getDateTime, i) for i in range(times)]
        results = []
        for future in as_completed(futures):
            results.append(future.result())

    return results

def getDateTime(url):
    response = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Berlin").json()
    return response["dateTime"].split(":")[-1]

if __name__ == "__main__":
    url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Berlin"

    request_time = requestTime(url)
    print("Time taken for one request: ", request_time)
    #-----------------------------------------------------------------------------------------------#
    print([round(x*0.01, 2) for x in range(0, 100)])
