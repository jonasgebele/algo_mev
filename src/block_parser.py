import requests
from collections import defaultdict

import markets

BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/blocks/"

def add_transactions_to_groups(transactions, groups):
    for transaction in transactions:
        if "group" in transaction:
            group = transaction["group"]
            if group in groups:
                groups[group].append(transaction)
    return groups

def get_swap_transaction_groups(transactions: dict) -> dict:
    groups = defaultdict(list)
    transactions_in_groups = list(transactions)
    for transaction in transactions:
        if not ("group" in transaction):
            transactions_in_groups.remove(transaction)
            continue
        if "application-transaction" in transaction:
            application_txs = transaction["application-transaction"]
            application_id = application_txs["application-id"]
            if is_monitored_application(application_id):
                group = transaction["group"]
                groups[group]
    return groups, transactions_in_groups

def is_monitored_application(application_id):
    application_ids = list(map(int, markets.get_application_ids()))
    return True if application_id in application_ids else False

def parse_block_data(round: int):
    transactions = {}
    try:
        response = requests.get(BASE_URL + str(round)).json()
        transactions = response["transactions"]
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"An error occurred: {e}")
    finally:
        return transactions

def get_swap_interactions(block_number):
    transactions = parse_block_data(block_number)
    swap_groups, transactions_within_groups = get_swap_transaction_groups(transactions)
    groups = add_transactions_to_groups(transactions_within_groups, swap_groups)
    return groups

def get_application_call_transaction(transaction_list):
    for transaction in transaction_list:
        if "tx-type" in transaction:
            if transaction["tx-type"] == "appl":
                return transaction
    return None

def get_funding_transaction(transactions, sender):
    for transaction in transactions:
        if "tx-type" in transaction:
            tx_type = transaction["tx-type"]
            if tx_type == "pay" or tx_type == "axfer":
                if transaction["sender"] == sender:
                    # Check for Tinyman Protocol Fee
                    if "payment-transaction" in transaction:
                        if not (transaction["payment-transaction"]["amount"] == 2000):
                            return transaction
                    else:
                        return transaction

def get_receiving_transaction(transactions, application_call, application_id, receiver):
    def default_receiving_transaction(application_call):
        return application_call["inner-txns"][0]
    def tinyman_receiving_transaction(transactions, receiver):
        for transaction in transactions:
            if "tx-type" in transaction:
                if "sender" in transaction:
                    if transaction["sender"] == receiver:
                        return transaction
        return None
    receiving_transaction = None
    if application_id ==  552635992: # Tinyman
        receiving_transaction = tinyman_receiving_transaction(transactions, receiver)
    else:
        receiving_transaction = default_receiving_transaction(application_call)
    return receiving_transaction

def get_send_asset_info(funding_transaction):
    if "tx-type" in funding_transaction:
        if funding_transaction["tx-type"] == "pay":
            if "payment-transaction" in funding_transaction:
                payment_info = funding_transaction["payment-transaction"]
                amount_send, asset_id_send = payment_info["amount"], 0
                return amount_send, asset_id_send
        elif funding_transaction["tx-type"] == "axfer":
            if "asset-transfer-transaction" in funding_transaction:
                transfer_info = funding_transaction["asset-transfer-transaction"]
                amount_send, asset_id_send = transfer_info["amount"], transfer_info["asset-id"]
                return amount_send, asset_id_send
        return None

def get_received_asset_info(receiving_transaction):
    if "tx-type" in receiving_transaction:
        if receiving_transaction["tx-type"] == "pay":
            if "payment-transaction" in receiving_transaction:
                payment_info = receiving_transaction["payment-transaction"]
                amount_send, asset_id_send = payment_info["amount"], 0
                return amount_send, asset_id_send
        elif receiving_transaction["tx-type"] == "axfer":
            if "asset-transfer-transaction" in receiving_transaction:
                transfer_info = receiving_transaction["asset-transfer-transaction"]
                amount_send, asset_id_send = transfer_info["amount"], transfer_info["asset-id"]
                return amount_send, asset_id_send
        else:
            return None, None

def get_receiver_from_funding_transaction(funding_transaction):
    if "asset-transfer-transaction" in funding_transaction:
        return funding_transaction["asset-transfer-transaction"]["receiver"]
    elif "payment-transaction" in funding_transaction:
        return funding_transaction["payment-transaction"]["receiver"]
    return None

def get_application_id_from_application_call(application_call):
    if "asset-transfer-transaction" in application_call:
        return application_call["asset-transfer-transaction"]["application-id"]
    elif "payment-transaction" in application_call:
        return application_call["payment-transaction"]["application-id"]
    return None

def swap_summary(transactions):
    # 1. Get the unique application call of the group
    application_call = get_application_call_transaction(transactions)
    
    # 2. Extract the unique sender out of the application call
    sender = application_call["sender"]
    # 3. Find with the sender-address the funding-transaction from all transactions
    funding_transaction = get_funding_transaction(transactions, sender)
    
    # 4. Extract receiver from the funding-transaction
    receiver = get_receiver_from_funding_transaction(funding_transaction)
    # 5. Extract the application-id to differentiate between different tx's strcutures of protocols
    application_id = get_application_id_from_application_call(application_call)
    # 6. Find the receiving transaction either in application-call-transaction (Tinyman) or with application-id from all transactions
    receiving_transaction = get_receiving_transaction(transactions, application_call, application_id, receiver)

    # TODO: Check for Tinyman -> Check if Assets are USDC, goUSD or USDT - all assets go over same address
    if not funding_transaction:
        return
    if not receiving_transaction:
        return

    group_id = application_call["group"]
    amount_send, asset_id_send = get_send_asset_info(funding_transaction)
    amount_received, asset_id_received = get_received_asset_info(receiving_transaction)

    return {
        "group_id": group_id,
        "sender": sender,
        "receiver": receiver,
        "amount_send": amount_send,
        "asset_id_send": asset_id_send,
        "amount_received": amount_received,
        "asset_id_received": asset_id_received
        }
