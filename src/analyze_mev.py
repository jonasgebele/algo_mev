import csv
import argparse
import block_parser

def parse_block_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument('block_number', type=int, help='Block we want to analyze for swaps.')
    args = parser.parse_args()
    return args.block_number

def estimate_dex_arbitrage_lower_bound():
    # loop through blocks

    # if price deviation on AMM is more than specified limit
    #       Check if swap occured on AMM while deviation is more than specified limit
    #               Check if Swap occured in favourable direction
    #                       Calculate the extractable value
    #                       Sum values up
    pass

def create_swap_transaction_data_per_block(start_round, end_round, output_filepath):
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
                a = {"a": 3}
                writer.writerow(a)

def main():
    '''
    block_number = parse_block_parameter()
    groups = block_parser.get_swap_interactions(block_number)
    for group in groups:
        transactions_of_group = groups[group]
        group_summary = block_parser.extract_swap_information(transactions_of_group)
        print(group_summary)
    '''
    create_swap_transaction_data_per_block(26814040, 26814200, "../data/swap_transactions.csv")


if __name__ == "__main__":
    main() # python analyze_mev.py 26814040
