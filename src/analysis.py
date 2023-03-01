import block_parser

def estimate_dex_arbitrage_lower_bound():
    # loop through blocks

    # if price deviation on AMM is more than specified limit
    #       Check if swap occured on AMM while deviation is more than specified limit
    #               Check if Swap occured in favourable direction
    #                       Calculate the extractable value
    #                       Sum values up
    pass

def main():
    block_number = 27174856
    groups = block_parser.get_swap_interactions(block_number)
    for group in groups:
        transactions_of_group = groups[group]
        group_summary = block_parser.extract_swap_information(transactions_of_group)
        print(group_summary)

if __name__ == "__main__":
    main() # python analyze_mev.py 26814040
