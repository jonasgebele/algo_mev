import csv

def main():
    with open("../data/responses.csv", "r") as input_file:
        reader = csv.reader(input_file)
        
        # Skip the header row
        next(reader)

        with open("../data/prices.csv", "w", newline="") as output_file:
            writer = csv.writer(output_file)

            for row in reader:
                prices = []
                prices.append(row[0]) # binance_algousdt
                prices.append(row[2]) # humbleswap_algousdc
                prices.append(row[6]) # humbleswap_algogousd
                prices.append(row[10]) # pact_algousdc
                prices.append(row[14]) # pact_algousdt
                prices.append(row[18]) # tinyman_algousdc
                prices.append(row[22]) # tinyman_algousdt
                writer.writerow(prices)

if __name__ == "__main__":
    main()
