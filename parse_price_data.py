import csv

def market_fees():
    market_fees = {}
    market_fees["HUMBLESWAP"] = 0.3
    market_fees["PACT"] = 0.3
    market_fees["TINYMAN"] = 0.3
    return market_fees

def spot_market_deviation(spot: float, dex_prices: list):
    deviations = []
    for dex_price in dex_prices:
        deviation = (dex_price - spot) / spot * 100
        deviations.append(deviation)
    return deviations

def parse_prices(source_filename, target_filename):
    with open(source_filename, "r") as input_file:
        reader = csv.reader(input_file)
        
        with open(target_filename, "w", newline="") as output_file:
            writer = csv.writer(output_file)

            for row in reader:
                prices = list(row[0]) # binance_algousdt
                prices.append(row[2]) # humbleswap_algousdc
                prices.append(row[6]) # humbleswap_algogousd
                prices.append(row[10]) # pact_algousdc
                prices.append(row[14]) # pact_algousdt
                prices.append(row[18]) # tinyman_algousdc
                prices.append(row[22]) # tinyman_algousdt

                writer.writerow(prices)

def mev_analysis(fees, filename):
    with open('path/to/file.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header-row
        for row in reader:
            spot_price, dex_prices = row[0], row[1:]
            spot_market_deviation()

def main():
    source_filename = "data/responses.csv"
    target_filename = "data/prices.csv"

    parse_prices(source_filename, target_filename)

    fees = market_fees()
    mev_analysis(fees, target_filename)
    
if __name__ == "__main__":
    main()
