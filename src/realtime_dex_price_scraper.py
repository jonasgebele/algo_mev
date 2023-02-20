import sys
import csv
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import markets

def setup_logging(path):
    logging.basicConfig(
        filename=path,
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

def get_dex_markets():
    dex_markets = markets.get_markets_addresses()
    return dex_markets

def get_cex_markets():
    cex_markets = {}
    cex_markets["Binance_ALGOUSDT"] = "ALGOUSDT"
    return cex_markets

def get_sorted_keys(markets):
    keys = list(markets.keys())
    keys.sort()
    return keys

def get_avg_spot_price_from_binance_spot(markets, key):
    try:
        timestamp = "{:.2f}".format(time.time())
        # print(timestamp)
        response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={markets[key]}").json()
        bid_price = response['bidPrice']
        ask_price = response['askPrice']
        # Calculate the average of the two prices to get a fair representation of the exchange price
        avg_price = (float(bid_price) + float(ask_price)) / 2
        spot_price = round(avg_price, 17)
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error(f"An exception doing the {key} API-call occured at timestamp {timestamp}: {e}")
    finally:
        return [timestamp, key, spot_price]

def get_stablecoin_amount(assets):
    stablecoin_asset_ids = [312769, 31566704, 672913181] # USDT, USDC, goUSD
    for asset in assets:
        if asset['asset-id'] in stablecoin_asset_ids:
            return asset['amount']
    return 0.0000

def get_swap_price_from_address_at_range(markets, key):
    try:
        # ALGOEXPLORER NODE
        '''
        response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{markets[key]}").json()
        '''
        # TUM INDEXER
        response = requests.get(f"http://131.159.14.109:8981/v2/accounts/{markets[key]}").json()
        response = response["account"]
   

        round = response['round']
        X = response['amount']
        Y = get_stablecoin_amount(response['assets'])
        swap_price = Y / X
    except (requests.exceptions.RequestException, ValueError, ZeroDivisionError) as e:
        logging.error(f"An exception doing the Indexer API-call occured at round {round}: {e}")
    finally:
        return [key, round, swap_price, X, Y]

def write_csv_header(filename, ordered_dex_keys, ordered_cex_keys):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        dex_row = [x for market_key in ordered_dex_keys for x in ("round:", market_key, "pool_size_X", "pool_size_Y")]
        header = list(ordered_cex_keys)
        header.append("timestamp")
        header.extend(dex_row)
        writer.writerow(header)

def write_csv_rows(filename, dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys):
    last_dex_responses = None
    while True:
        scraped_dex_responses, rounds_of_responses, scraped_cex_responses = parse_market_endpoints(dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys)
        # print("Response changed: ", response_changed(scraped_dex_responses, last_dex_responses))
        if not response_changed(scraped_dex_responses, last_dex_responses):
            continue
        last_dex_responses = scraped_dex_responses.copy()
        # print("Consistent round: ", consistent_rounds(rounds_of_responses))
        if not consistent_rounds(rounds_of_responses):
            continue
        write_response_row(filename, ordered_dex_keys,  ordered_cex_keys, scraped_dex_responses, scraped_cex_responses)

def write_response_row(filename, ordered_dex_keys, ordered_cex_keys, scraped_dex_responses, scraped_cex_responses):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        dex_info_tuples = [scraped_dex_responses[key] for key in ordered_dex_keys]
        dex_row = [x for tuple in dex_info_tuples for x in tuple]
        time = [scraped_cex_responses[key][1] for key in ordered_cex_keys][0]
        cex_row = [scraped_cex_responses[key][0] for key in ordered_cex_keys]
        response = list(cex_row)
        response.append(time)
        response.extend(dex_row)
        writer.writerow(response)

def response_changed(scraped_dex_info, latest_scraped_dex_info):
    return False if scraped_dex_info == latest_scraped_dex_info else True

def consistent_rounds(rounds):
    return False if len(rounds) != 1 else True

def parse_market_endpoints(dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys):
    scraped_dex_responses, scraped_cex_responses = {}, {}
    rounds_of_responses = set()
    
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(get_swap_price_from_address_at_range, dex_markets, key) for key in ordered_dex_keys]
        results.extend([executor.submit(get_avg_spot_price_from_binance_spot, cex_markets, key) for key in ordered_cex_keys])
        for f in as_completed(results):
            result = f.result()
            is_dex_result = True if len(result) == 5 else False
            if is_dex_result:
                key, round, swap_price, X, Y = result[0], result[1], result[2], result[3], result[4]
                scraped_dex_responses[key] = round, swap_price, X, Y
                rounds_of_responses.add(round)
            else:
                time, key, spot_price= result[0], result[1], result[2]
                scraped_cex_responses[key] = (spot_price, time)

        return scraped_dex_responses, rounds_of_responses, scraped_cex_responses

def main():
    timestamp = int(time.time())

    setup_logging(f'../logs/responses_{timestamp}.log')
    source_filepath = f"../data/responses_{timestamp}.csv"

    dex_markets, cex_markets = get_dex_markets(), get_cex_markets()
    ordered_dex_keys, ordered_cex_keys = get_sorted_keys(dex_markets), get_sorted_keys(cex_markets)
    write_csv_header(source_filepath, ordered_dex_keys, ordered_cex_keys)
    write_csv_rows(source_filepath, dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
