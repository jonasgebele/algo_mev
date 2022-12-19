import csv
import time
import requests

HUMBLESWAP_ALGOUSDC = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
HUMBLESWAP_ALGOgoUSD = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU"
PACT_ALGOUSDC = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A"
PACT_ALGOUSDT = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4"
TINYMAN_ALGOUSDC = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
TINYMAN_ALGOUSDT = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM"

def get_avg_spot_price_from_binance_spot(pair: str):
    """
    Get the average spot price from Binance Spot for a given pair.

    Parameters:
    pair (str): The pair for which to get the average spot price.

    Returns:
    float: The average spot price for the given pair.
    """
    # Make a GET request to the Binance API to the given pair
    response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={pair}")

    # Extract the bidPrice and askPrice values from the API response to calculate the average orderbook price
    bid_price = response.json()['bidPrice']
    ask_price = response.json()['askPrice']

    # Calculate the average of the two prices
    avg_price = (float(bid_price) + float(ask_price)) / 2
    spot_price = round(avg_price, 6)
    return spot_price

def get_swap_price_from_address(address: str):
    """
    Get the swap price for a given address.

    Parameters:
    address (str): The address for which to get the swap price.

    Returns:
    float: The swap price for the given address.
    """
    # Make a GET request to the Address of Pool Account we want to monitor
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[0]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def main():
    """
    Get the spot prices from various sources and write them to a CSV file.

    The following prices are obtained and written to the CSV file:
    Binance Spot price for the 'ALGOUSDT' pair
    Humbe Swap price for the 'ALGOUSDC' address
    Humbe Swap price for the 'ALGOgoUSD' address
    Pact price for the 'ALGOUSDC' address
    Pact price for the 'ALGOUSDT' address
    Tinyman price for the 'ALGOUSDC' address
    Tinyman price for the 'ALGOUSDT' address

    The prices are obtained continuously in a loop and written to the CSV file with a timestamp.
    """
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
