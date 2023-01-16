import csv
import time
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def set_up_markets_dict () -> dict:
    markets = {}
    # adding addresses of DEX'es to the dictionary
    markets["HUMBLESWAP_ALGOUSDC"] = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
    # markets["Binance_ALGOUSDT"] = "ALGOUSDT"
    markets["HUMBLESWAP_ALGOgoUSD"] = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU"
    markets["PACT_ALGOUSDC"] = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A"
    markets["PACT_ALGOUSDT"] = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4"
    markets["TINYMAN_ALGOUSDC"] = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
    markets["TINYMAN_ALGOUSDT"] = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM"
    # returning the markets-dictionary
    return markets

def get_sorted_list_of_keys(markets):
    # creating a list of keys for markets-dictionary
    keys = list(markets.keys())
    # sorting the list of keys alphabetically
    keys.sort()
    # returning the sorted list of keys
    return keys

def get_avg_spot_price_from_binance_spot(pair):
    # Default value for price to return in case of a exception
    spot_price = 0.000000
    try:
        # Make a GET request to the Binance API to the given pair
        response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={pair}")
        # Get the current date and time
        now = datetime.now()
        # Get the timestamp
        timestamp = int(now.timestamp())
        # Extract the bidPrice and askPrice values from the API response to calculate the average orderbook price
        bid_price = response.json()['bidPrice']
        ask_price = response.json()['askPrice']
        # Calculate the average of the two prices
        avg_price = (float(bid_price) + float(ask_price)) / 2
        spot_price = round(avg_price, 6)

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred while making the API call
        print(f"An error occurred: {e}")
    except ValueError as e:
        # Handle any value errors that occurred while processing the response
        print(f"An error occurred: {e}")
    finally:
        return "Binance_ALGOUSDT", timestamp, spot_price, 0, 0

def get_swap_price_from_address_at_range(markets, key):
    try:
        # Make a GET request to the Address of Pool Account we want to monitor

        # ------------------------------------------------------------------------------------------#
        # ALGOEXPLORER INDEXER
        #response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{markets[key]}").json()

        # TUM INDEXER
        response = requests.get(f"http://131.159.14.109:8981/v2/accounts/{markets[key]}").json()
        response = response["account"]
        #-------------------------------------------------------------------------------------------#

        # Extract the pool-sizes and asset values from the API response
        assets = response['assets']
        X = response['amount']
        Y = assets[0]["amount"]
        round = response['round']
        
        # Calculate the swap price as the Y divided by X
        swap_price = Y / X
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred while making the API call
        print(f"An error occurred: {e}")
    except ValueError as e:
        # Handle any value errors that occurred while processing the response
        print(f"An error occurred: {e}")
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    finally:
        return key, round, swap_price, X, Y

def main():
    # create dict with market-descriptors as keys and addresses of asset-pools as values
    markets = set_up_markets_dict()
    # get consistent order of market-keys from the markets-dict
    ordered_list_of_market_keys = get_sorted_list_of_keys(markets)
    
    # Open the CSV file for writing
    with open("prices2.csv", "w", newline="") as f:
        # Create a CSV writer
        writer = csv.writer(f)
        # Write the header row with market-keys in consistent order
        writer.writerow([x for market_key in ordered_list_of_market_keys for x in ("range", market_key, "pool_size_X", "pool_size_Y")])
    
    # Store track of API response information from the latest call
    latest_scraped_info = None
    while True:
        # Dictionary for API response information for the current call
        scraped_info = {}
        # Keep track of rounds for each DEX info scraped
        rounds = set()

        # Making API calls parallized instead of sequentially in order to reduce I/O waiting time
        with ThreadPoolExecutor() as executor:
            results = [executor.submit(get_swap_price_from_address_at_range, markets, market_key) for market_key in ordered_list_of_market_keys]
            # results.append(executor.submit(get_avg_spot_price_from_binance_spot, "ALGOUSDT"))
            for f in as_completed(results):
                key, round, swap_price, X, Y = f.result()
                scraped_info[key] = (round, swap_price, X, Y)
                rounds.add(round)

        # Check if API response information has not changed
        if scraped_info == latest_scraped_info:
            # Restarting the loop, doing the next API calls
            continue
        # Keep track of the most recent API response information for future calls 
        latest_scraped_info = scraped_info.copy()

        # Check if API response information is consistent among block-rounds
        if len(rounds) != 1:
            # Do new API response calls right away
            continue
        
        # Open the CSV file for writing
        with open("prices2.csv", "a", newline="") as f:
            # Create a CSV writer
            writer = csv.writer(f)
            # Get response information in uniform order
            price_info_tuples = [scraped_info[market_key] for market_key in ordered_list_of_market_keys]
            # Write dereferenced tuples in CSV file
            writer.writerow([x for tuple in price_info_tuples for x in tuple])

if __name__ == "__main__":
    try:
        print("Starting to scrape the Algorand universe.")
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
