import argparse
import block_parser

def parse_block_parameter():
    parser = argparse.ArgumentParser()
    parser.add_argument('block_number', type=int, help='Block we want to analyze for swaps.')
    args = parser.parse_args()
    return args.block_number

def main():
    block_number = parse_block_parameter()
    groups = block_parser.get_swap_interactions(block_number)

    for group in groups:
        transactions_of_group = groups[group]
        group_summary = block_parser.swap_summary(transactions_of_group)
        print(group_summary)

if __name__ == "__main__":
    main()
    # Run with: python analyze_mev.py 26814040
