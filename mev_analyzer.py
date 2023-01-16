import csv

def read_csv(file_path):
    data = []
    # Open the CSV file
    with open(file_path, newline='') as csvfile:
        # Create a CSV reader
        reader = csv.reader(csvfile)
        # Iterate over the rows in the CSV file
        for row in reader:
            data.append(row)
    return data

def process_data(data):
    try:
        for row in data:
            # Extract the data from the row
            range = row[0]
            market_key = row[1]
            pool_size_X = row[2]
            pool_size_Y = row[3]
            # Perform any calculations or processing on the data
            swap_price = float(pool_size_Y) / float(pool_size_X)
            print(f"Range: {range}, Market: {market_key}, Swap Price: {swap_price}")
    except ZeroDivisionError:
        print("Division by zero error")

def main():
    # Replace file_path with the path to your CSV file
    file_path = "./prices2.csv"
    data = read_csv(file_path)
    process_data(data)

if __name__ == "__main__":
    main()   
