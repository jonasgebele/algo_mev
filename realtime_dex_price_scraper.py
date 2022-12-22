import csv
import time
import requests
import threading

HUMBLESWAP_ALGOUSDC = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
HUMBLESWAP_ALGOgoUSD = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU"
PACT_ALGOUSDC = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A"
PACT_ALGOUSDT = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4"
TINYMAN_ALGOUSDC = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
TINYMAN_ALGOUSDT = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM"

def get_avg_spot_price_from_binance_spot(pair: str):
    # Default value for price to return in case of a exception
    spot_price = 0.000000

    try:
        # Make a GET request to the Binance API to the given pair
        response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={pair}")

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
        return spot_price

def get_swap_price_from_address(address: str):
    # Default value for price to return in case of a exception
    api_call_data = {
        "swap_price": 0.000000,
        "round": 0,
        "pool_size": 0.000000
    }

    try:
        # Make a GET request to the Address of Pool Account we want to monitor
        response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}").json()

        # Extract the amount and assets values from the API response
        amount = response['amount']
        assets = response['assets']
        round = response['round']

        # Calculate the swap price as the assets[0]["amount"] divided by amount
        swap_price = round(assets[0]["amount"] / amount, 6)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred while making the API call
        print(f"An error occurred: {e}")
    except ValueError as e:
        # Handle any value errors that occurred while processing the response
        print(f"An error occurred: {e}")
    finally:
        return swap_price

def main():
    # Open the CSV file for writing
    with open("prices2.csv", "w", newline="") as f:
        # Create a CSV writer
        writer = csv.writer(f)

        # Write the header row
        writer.writerow([
            "timestamp",
            "priceBinanceSpot[ALGOUSDT]",
            "priceHumbeSwap[ALGOUSDC]",
            "priceHumbeSwap[ALGOgoUSD]",
            "pricePact[ALGOUSDC]",
            "pricePact[ALGOUSDT]",
            "priceTinyman[ALGOUSDC]",
            "priceTinyman[ALGOUSDT]"
        ])

    while True:
        # Get the current timestamp in miliseconds
        timestamp = round(time.time(), 2)
        '''
        # Create a thread for each API call
        api_1_thread = threading.Thread(target=get_avg_spot_price_from_binance_spot, args=("ALGOUSDT",))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(HUMBLESWAP_ALGOUSDC,))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(HUMBLESWAP_ALGOgoUSD,))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(PACT_ALGOUSDC,))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(PACT_ALGOUSDT,))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(TINYMAN_ALGOUSDC,))
        api_2_thread = threading.Thread(target=get_swap_price_from_address, args=(TINYMAN_ALGOUSDT,))

        # Start the threads
        api_1_thread.start()
        api_2_thread.start()

        # Wait for the threads to finish
        api_1_thread.join()
        api_2_thread.join()
        '''

        # Get the average price from the API
        binance_usdt = get_avg_spot_price_from_binance_spot("ALGOUSDT")
        humbleswap_usdc = get_swap_price_from_address(HUMBLESWAP_ALGOUSDC)
        humbleswap_gousd = get_swap_price_from_address(HUMBLESWAP_ALGOgoUSD)
        pact_usdc = get_swap_price_from_address(PACT_ALGOUSDC)
        pact_usdt = get_swap_price_from_address(PACT_ALGOUSDT)
        tinyman_usdc = get_swap_price_from_address(TINYMAN_ALGOUSDC)
        tinyman_usdt = get_swap_price_from_address(TINYMAN_ALGOUSDT)

        # Open the CSV file for writing
        with open("prices2.csv", "a", newline="") as f:
            # Create a CSV writer
            writer = csv.writer(f)

            # Write the avg_price and timestamp to the file as a new row
            writer.writerow([
                timestamp,
                binance_usdt,
                humbleswap_usdc,
                humbleswap_gousd,
                pact_usdc,
                pact_usdt,
                tinyman_usdc,
                tinyman_usdt
            ])

        # Sleep for 2 seconds before making the next API call to get to the 4,5 second block time of Algorand
        time.sleep(2)

if __name__ == "__main__":
    main()
