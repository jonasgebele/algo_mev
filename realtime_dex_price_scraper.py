import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_dex_markets():
    dex_markets = {}
    dex_markets["HUMBLESWAP_ALGOUSDC"] = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
    dex_markets["HUMBLESWAP_ALGOgoUSD"] = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU"
    dex_markets["PACT_ALGOUSDC"] = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A"
    dex_markets["PACT_ALGOUSDT"] = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4"
    dex_markets["TINYMAN_ALGOUSDC"] = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
    dex_markets["TINYMAN_ALGOUSDT"] = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM"
    return dex_markets

def get_cex_markets():
    cex_markets = {}
    cex_markets["Binance_ALGOUSDT"] = "ALGOUSDT"
    return cex_markets

def get_sorted_list_of_keys(markets):
    keys = list(markets.keys())
    keys.sort()
    return keys

def get_avg_spot_price_from_binance_spot(markets, key):
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={markets[key]}")
        # Extract the bidPrice and askPrice values from the orderbook
        bid_price = response.json()['bidPrice']
        ask_price = response.json()['askPrice']
        # Calculate the average of the two prices to get a fair representation of the exchange price
        avg_price = (float(bid_price) + float(ask_price)) / 2
        spot_price = round(avg_price, 17)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"An error occurred: {e}")
    finally:
        return key, spot_price

def get_swap_price_from_address_at_range(markets, key):
    try:
# ------------------------------------------------------------------------------------------#
        # ALGOEXPLORER INDEXER
        #response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{markets[key]}").json()

        # TUM INDEXER
        response = requests.get(f"http://131.159.14.109:8981/v2/accounts/{markets[key]}").json()
        response = response["account"]
#-------------------------------------------------------------------------------------------#
        round = response['round']
        X = response['amount']
        assets = response['assets']
        Y = assets[0]["amount"]
        # Calculate the swap price as the Y divided by X
        swap_price = Y / X
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"An error occurred: {e}")
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    finally:
        return key, round, swap_price, X, Y

def write_csv_header(filename, ordered_dex_keys, ordered_cex_keys):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        dex_row = [x for market_key in ordered_dex_keys for x in ("range", market_key, "pool_size_X", "pool_size_Y")]
        header_row = []
        header_row.extend(ordered_cex_keys)
        header_row.extend(dex_row)
        writer.writerow(header_row)

def write_response_row(filename, ordered_dex_keys, scraped_dex_info):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        # Get response information in uniform order
        price_info_tuples = [scraped_dex_info[key] for key in ordered_dex_keys]
        # Write dereferenced tuples in CSV file
        writer.writerow([x for tuple in price_info_tuples for x in tuple])

def response_changed(scraped_dex_info, latest_scraped_dex_info):
        if scraped_dex_info == latest_scraped_dex_info:
            return False
        return True

def consistent_rounds(rounds):
    if len(rounds) != 1:
        return False
    return True

def main():
    # dex and cex markets-dict with descriptors as keys and addresses/pair-names as values
    dex_markets, cex_markets = get_dex_markets(), get_cex_markets()
    # get uniform-order (alphabetically) of keys from the markets-dict
    ordered_dex_keys, ordered_cex_keys = get_sorted_list_of_keys(dex_markets), get_sorted_list_of_keys(cex_markets)
    
    write_csv_header("prices.csv", ordered_dex_keys, ordered_cex_keys)
    
    # Store track of API response information from the latest call
    last_dex_responses = None
    while True:
        scraped_dex_responses = {}
        # Keep track of rounds for each DEX-info scraped
        rounds_of_responses = set()

        # Making API calls parallized instead of sequentially to reduce I/O delay
        with ThreadPoolExecutor() as executor:
            results = [executor.submit(get_swap_price_from_address_at_range, dex_markets, key) for key in ordered_dex_keys]
            # results.extend([executor.submit(get_avg_spot_price_from_binance_spot, cex_markets, key) for key in ordered_cex_keys])
            for f in as_completed(results):
                key, round, swap_price, X, Y = f.result()
                scraped_dex_responses[key] = round, swap_price, X, Y
                rounds_of_responses.add(round)

        if not response_changed(scraped_dex_responses, last_dex_responses):
            continue
        last_dex_responses = scraped_dex_responses.copy()
        
        if not consistent_rounds(rounds_of_responses):
            continue
        
        write_response_row("prices.csv", ordered_dex_keys, scraped_dex_responses)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
