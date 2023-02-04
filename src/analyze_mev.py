import block_data_parser

def main():
    block_number = 25729521
    hash, timestamp, transaction_groups = block_data_parser.get_swap_interactions(block_number)
    for group in transaction_groups:
        print(transaction_groups[group])

if __name__ == "__main__":
    main()
