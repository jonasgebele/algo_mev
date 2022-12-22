import json
import requests
import argparse

from collections import defaultdict

BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/blocks/"

def extract_groups_with_application_calls(transactions: dict) -> dict:
    transactions_by_groupID = defaultdict(list)
    for tx in transactions:
        if "group" in tx:
            transactions_by_groupID[tx["group"]] = tx
    return transactions_by_groupID

def get_block_data(round: int):
    hash, transactions, timestamp = "ERROR", {}, 0
    try:
        response = requests.get(BASE_URL + str(round)).json()
        assert round == response["round"]
        assert response["genesis-id"] == "mainnet-v1.0"
        hash = response["genesis-hash"]
        transactions = response["transactions"]
        timestamp = response["timestamp"]
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred while making the API call
        print(f"An error occurred: {e}")
    except KeyError as e:
        # Handle any key errors that occurred while processing the response
        print(f"An error occurred: {e}")
    except AssertionError as e:
        # If the response doesn't align with the specified parameter
        print(f"An error occurred: {e}")
    finally:
        return hash, transactions, timestamp

def main(round_start, round_stop):
    hash, transactions, timestamp = get_block_data(25729521)
    relevant_transactions = extract_groups_with_application_calls(transactions)
    print(relevant_transactions)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()
    
    #start 0 - max = current block height -1
    # min = max, current block height

    # Add two integer arguments with a restricted range
    parser.add_argument("round_start", type=int, min=0, max=10)
    parser.add_argument("round_stop", type=int, min=1, max=10)


    # Parse the arguments from the command line
    args = parser.parse_args()

    main(args.round_start, args.round_stop)
