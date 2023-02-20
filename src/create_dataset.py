import os
import csv
import argparse

def parse_source_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, help='Filepath for the source file.')
    args = parser.parse_args()
    return args.source_file

def destination_filename(source_file):
    filepath = os.path.dirname(source_file)
    responses_basename = os.path.basename(source_file)
    dest_filename = filepath + "/prices_" + responses_basename
    return dest_filename

def write_csv_header(filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        header = [
            "block-height",
            "timestamp",
            "binance_algousdt",
            "humbleswap_algousdc",
            "humbleswap_algogousd",
            "pact_algousdc",
            "pact_algousdt",
            "tinyman_algousdc",
            "tinyman_algousdt"
        ]
        writer.writerow(header)

def write_csv_rows(filename, source_reader):
    with open(filename, "a", newline="") as output_file:
        writer = csv.writer(output_file)
        for row in source_reader:
            info = []
            info.append(row[2]) # block-height (range)
            info.append(row[1]) # timestamp
            info.append(row[0]) # binance_algousdt
            info.append(row[3]) # humbleswap_algousdc
            info.append(row[7]) # humbleswap_algogousd
            info.append(row[11]) # pact_algousdc
            info.append(row[15]) # pact_algousdt
            info.append(row[19]) # tinyman_algousdc
            info.append(row[23]) # tinyman_algousdt
            writer.writerow(info)

def main():
    responses_file = parse_source_parameter()
    try:
        with open(responses_file, "r") as input_file:
            source_reader = csv.reader(input_file)
            next(source_reader) # Skip the header row

            dest_filename = destination_filename(responses_file)
            write_csv_header(dest_filename)
            write_csv_rows(dest_filename, source_reader)
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the file: {e}")

if __name__ == "__main__":
    # RUN WITH:    python create_price_data_of_responses.py "../data/responses.csv"
    main()
