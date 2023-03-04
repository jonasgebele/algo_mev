import os
import csv
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import markets

def setup_logging(path):
    logging.basicConfig(
        filename=path,
        level=logging.DEBUG,
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

def get_unix_timestamp():
    return int(time.time())

def get_avg_spot_price_from_binance(markets, key):
    timestamp = "{:.2f}".format(time.time())
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={markets[key]}").json()
        bid_price = response['bidPrice']
        ask_price = response['askPrice']
        # Calculate the average of the two prices to get a fair representation of the exchange price
        avg_price = (float(bid_price) + float(ask_price)) / 2
        spot_price = round(avg_price, 17)
    except Exception as e:
        spot_price = -1
        logging.error(f"An exception doing the Binance API-call occured at timestamp {timestamp}: {e}")
    finally:
        return spot_price, timestamp

def get_avg_spot_price_from_coincap():
    try:
        response = requests.get(f"https://api.coincap.io/v2/assets/algorand").json()
        timestamp = response["timestamp"]
        data = response["data"]
        spot_price = data["priceUsd"]
    except ValueError as e:
        timestamp = "{:.2f}".format(time.time())
        logging.error(f"An Value exception occurred while parsing the JSON response from the CoinCap API-call at timestamp {timestamp}: {e}")
        spot_price = 0
    except Exception as e:
        timestamp = "{:.2f}".format(time.time())
        spot_price = -1
        logging.error(f"An exception doing the CoinCap ALGO/USD API-call occured at timestamp {timestamp}: {e}")
    finally:
        return spot_price, timestamp

coincap_lock = False
binance_lock = False

def get_exchange_price_from_market(markets, key, parsing_starting_timestamp):
    time_to_switch_endpoints_in_seconds = 3600 # 3600 => switch after 1h
    
    current_timestamp = get_unix_timestamp()
    time_diff = current_timestamp - parsing_starting_timestamp

    global coincap_lock
    global binance_lock

    if  (not coincap_lock) and (time_diff // time_to_switch_endpoints_in_seconds) % 2 == 0:
        print("CoinCap")
        spot_price, timestamp = get_avg_spot_price_from_coincap()
        if spot_price == -1:
            coincap_lock = True
            binance_lock = False
    elif (not binance_lock):
        print("Binance")
        spot_price, timestamp = get_avg_spot_price_from_binance(markets, key)
        if spot_price == -1:
            binance_lock = True
            coincap_lock = False
    else:
        spot_price, timestamp = get_avg_spot_price_from_coincap()

    if spot_price == -1:
        pass

    return [timestamp, key, spot_price]

def get_stablecoin_amount(assets):
    stablecoin_asset_ids = [312769, 31566704, 672913181] # USDT, USDC, goUSD
    for asset in assets:
        if asset['asset-id'] in stablecoin_asset_ids:
            return asset['amount']
    return 0.0000

def get_swap_price_from_address(markets, key):
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
    parsing_starting_timestamp = get_unix_timestamp()
    last_dex_responses = None
    while True:
        scraped_dex_responses, rounds_of_responses, scraped_cex_responses = parse_market_endpoints(dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys, parsing_starting_timestamp)
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

def parse_market_endpoints(dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys, parsing_starting_timestamp):
    scraped_dex_responses, scraped_cex_responses = {}, {}
    rounds_of_responses = set()
    
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(get_swap_price_from_address, dex_markets, key) for key in ordered_dex_keys]
        results.extend([executor.submit(get_exchange_price_from_market, cex_markets, key, parsing_starting_timestamp) for key in ordered_cex_keys])
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

def get_current_block_height():
    url = "https://node.algoexplorerapi.io/v2/status"
    response = requests.get(url)
    data = response.json()
    last_round = int(data["last-round"])
    return last_round

def main():
    try:
        timestamp = get_unix_timestamp()
        setup_logging(f'../logs/responses_{timestamp}.log')

        starting_block = get_current_block_height()
        source_filepath = f"../data/responses_{starting_block}.csv"

        dex_markets, cex_markets = get_dex_markets(), get_cex_markets()
        ordered_dex_keys, ordered_cex_keys = get_sorted_keys(dex_markets), get_sorted_keys(cex_markets)
        write_csv_header(source_filepath, ordered_dex_keys, ordered_cex_keys)
        write_csv_rows(source_filepath, dex_markets, cex_markets, ordered_dex_keys, ordered_cex_keys)
    except KeyboardInterrupt:
        ending_block = get_current_block_height()
        new_source_filepath = f"../data/responses_{starting_block}_{ending_block}.csv"
        os.rename(source_filepath, new_source_filepath)
        print(f"Interrupted by user, exiting. Stored the price data from block {starting_block} till block {ending_block} in the following file: {new_source_filepath}")

if __name__ == "__main__":
    main()