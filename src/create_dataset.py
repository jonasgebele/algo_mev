import os
import csv
import argparse
import block_parser

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description="Create a dataset based on the specified command")
    subparsers = parser.add_subparsers(dest="command")

    prices_parser = subparsers.add_parser("prices", help="Create a prices dataset")
    prices_parser.add_argument("filepath", help="Path to the source file containing prices data")
    
    transactions_parser = subparsers.add_parser("transactions", help="Create a transactions dataset")
    transactions_parser.add_argument("start_round", type=int, help="Round start for transactions data")
    transactions_parser.add_argument("end_round", type=int, help="Round end for transactions data")
    
    args = parser.parse_args()
    params = dict()
    if args.command == "prices":
        params["filepath"] = args.filepath
    elif args.command == "transactions":
        if args.start_round >= args.end_round:
            raise ValueError("Start round must be less than end round")
        params["start_round"] = args.start_round
        params["end_round"] = args.end_round
    else:
        raise ValueError("Invalid command specified")
    return args.command, params

def create_swap_transaction_dataset(start_round, end_round, output_filepath):
    with open(output_filepath, 'w', newline='') as csvfile:
        fieldnames = ["round", "group_id", "sender", "receiver", "application-id", "amount_send", "asset_id_send", "amount_received", "asset_id_received"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for round in range(start_round, end_round+1):
            print(f"Working on round {round}")
            groups = block_parser.get_swap_interactions(round)
            for group in groups:
                transactions_of_group = groups[group]
                group_summary = block_parser.extract_swap_information(transactions_of_group)
                print(group_summary)
                writer.writerow(group_summary)

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

def create_price_dataset(responses_file):
    try:
        with open(responses_file, "r") as input_file:
            source_reader = csv.reader(input_file)
            next(source_reader) # Skip the header row
            dest_filename = destination_filename(responses_file)
            write_csv_header(dest_filename)
            write_csv_rows(dest_filename, source_reader)
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the file: {e}")

def main():
    command, params = parse_command_line_arguments()
    output_filepath = "../data/swap_transactions.csv"
    if command == "transactions":
        create_swap_transaction_dataset(params["start_round"], params["end_round"], output_filepath)
    elif command == "prices":
        create_price_dataset(params["filepath"])

if __name__ == "__main__":
    main()
    # python create_dataset.py prices "../data/responses_XXXXXXXXXX.csv"
    # python create_dataset.py transactions 26814040 26814140
