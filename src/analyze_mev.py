import argparse
import block_data_parser

def parse_block_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument('block_number', type=int, help='Block we want to analyze for swaps.')
    args = parser.parse_args()
    return args.block_number

def main():
    block_number = parse_block_parameter()

    hash, timestamp, group_collection = block_data_parser.get_swap_interactions(block_number)
    for group in group_collection:
        summary = block_data_parser.get_swap_summary(group_collection[group])
        print(summary)

if __name__ == "__main__":
    main() # Run with: python analyze_mev.py 26814040
