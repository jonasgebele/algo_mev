import json
import requests
import argparse

from collections import defaultdict

BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/blocks/"

def add_payment_transaction_to_groups(transactions, application_tx_group):
    for transaction in transactions:
        if "group" in transaction:
            group_id = transaction["group"]
            if not (transaction in application_tx_group[group_id]):
                application_tx_group[group_id].append(transaction)
    return application_tx_group

def extract_application_call_groups(transactions: dict) -> dict:
    transaction_groups = defaultdict(list)
    for transaction in transactions:
        if "group" in transaction:
            group_id = transaction["group"]
            transaction_groups[group_id].append(transaction)
    return transaction_groups

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
        print(f"An request error occurred: {e}")
    except KeyError as e:
        print(f"An key error occurred: {e}")
    except AssertionError as e:
        print(f"An assertion error occurred: {e}")
    finally:
        return hash, timestamp, transactions

def main(start, end):
    for i in range(start, end):
        hash, timestamp, transactions = get_block_data(i)
        application_tx_groups = extract_application_call_groups(transactions)
        transaction_groups = add_payment_transaction_to_groups(transactions, application_tx_groups)
        
        for group_id in transaction_groups:
            print(transaction_groups[group_id])
            print(" ")
        

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Add two integer arguments with a restricted range of blocks to query
    parser.add_argument("start", type=int, help="first block we want to query (included)")
    parser.add_argument("end", type=int, help="last block we want to query (excluded)")

    # Parse the command-line arguments
    args = parser.parse_args()
    main(args.start, args.end)
