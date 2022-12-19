import csv
import time
import requests

def get_avg_spot_price_from_binance_api():
    # Define Pair ALGO/USDT
    pair = "ALGOUSDT"
    
    # Make a GET request to the Binance API
    response = requests.get(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={pair}")

    # Extract the bidPrice and askPrice values from the API response to calculate the average orderbook price
    bid_price = response.json()['bidPrice']
    ask_price = response.json()['askPrice']

    # Calculate the average of the two prices
    avg_price = (float(bid_price) + float(ask_price)) / 2
    spot_price = round(avg_price, 6)
    return spot_price

def get_swap_price_from_humbleswap_usdc():
    # Address of Pool Account of ALGO USDT HumbleSwap 
    address = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[0]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def get_swap_price_from_humbleswap_gousd():
    # Address of Pool Account of ALGO goUSD HumbleSwap 
    address = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[0]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def get_swap_price_from_pact_usdc():
    # Address of Pool Account of ALGO USDC Pact DEX
    address = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[1]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def get_swap_price_from_pact_usdt():
    # Address of Pool Account of ALGO USDT Pact DEX
    address = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[1]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def get_swap_price_from_tinyman_usdc():
    # Address of Pool Account of ALGO USDC Tinyman
    address = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[1]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def get_swap_price_from_tinyman_usdt():
    # Address of Pool Account of ALGO USDT Tinyman
    address = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM"
    
    # Make a GET request to the HumbleSwap API
    response = requests.get(f"https://node.algoexplorerapi.io/v2/accounts/{address}")

    # Extract the amount and assets values from the API response
    amount = response.json()['amount']
    assets = response.json()['assets']

    # Calculate the swap price as the assets[1]["amount"] divided by amount
    swap_price = round(assets[0]["amount"] / amount, 6)
    return swap_price

def main():
    # Open the CSV file for writing
    with open("prices2.csv", "w", newline="") as f:
        # Create a CSV writer
        writer = csv.writer(f)

        # Write the header row
        writer.writerow([
            "timestamp", "priceBinanceSpot[ALGOUSDT]",
            "priceHumbeSwap[ALGOUSDC]",
            "priceHumbeSwap[ALGOgoUSD]",
            "pricePact[ALGOUSDC]",
            "pricePact[ALGOUSDT]",
            "priceTinyman[ALGOUSDC]",
            "priceTinyman[ALGOUSDT]"
        ])

    while True:
        # Get the current timestamp
        timestamp = round(time.time(), 2)

        # Get the average price from the API
        binance_usdt = get_avg_spot_price_from_binance_api()
        humbleswap_usdc = get_swap_price_from_humbleswap_usdc()
        humbleswap_gousd = get_swap_price_from_humbleswap_gousd()
        pact_usdc = get_swap_price_from_pact_usdc()
        pact_usdt = get_swap_price_from_pact_usdt()
        tinyman_usdc = get_swap_price_from_tinyman_usdc()
        tinyman_usdt = get_swap_price_from_tinyman_usdt()

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
