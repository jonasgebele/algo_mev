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
            application_call = transaction["application-transaction"]
            if "application-id" in application_call:
                application_id = application_call["application-id"]
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
        if "transactions" in response:
            transactions = response["transactions"]
    except requests.exceptions.RequestException as e:
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
                if "sender" in transaction:
                    if transaction["sender"] == sender:
                        if "payment-transaction" in transaction:
                            payment_info = transaction["payment-transaction"]
                            # Check for Tinyman protocol fee transaction
                            if "amount" in payment_info:
                                if payment_info["amount"] == 2000:
                                    continue
                                else:
                                    return transaction
                        else:
                            return transaction
    return None

def get_receiving_transaction(transactions, application_call, application_id, receiver):
    def default_receiving_transaction(application_call):
        if "inner-txns" in application_call:
            inner_txs = application_call["inner-txns"]
            return inner_txs[0]
        return None
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

def get_fields_from_transaction(transaction, fields: list):
    values = dict()
    if "tx-type" in transaction:
        tx_type = transaction["tx-type"]
        if tx_type == "pay":
            if "payment-transaction" in transaction:
                payment_info = transaction["payment-transaction"]
                for field in fields:
                    # if is payment-transaction, the asset-id of ALGO of 0 is implicitly given
                    if field == "asset-id":
                        values["asset-id"] = 0
                    else:
                        values[field] = payment_info[field]
        elif tx_type == "axfer":
            if "asset-transfer-transaction" in transaction:
                transfer_info = transaction["asset-transfer-transaction"]
                for field in fields:
                    values[field] = transfer_info[field]
        elif tx_type == "appl":
            if "application-transaction" in transaction:
                app_call_info = transaction["application-transaction"]
                for field in fields:
                    values[field] = app_call_info[field]
    return values

def extract_swap_information(transactions):
    # 1. Get the unique application call of the group
    application_call = get_application_call_transaction(transactions)
    group_id = application_call["group"]

    # 2. Extract the unique sender out of the application call
    sender = application_call["sender"]
    # 3. Find with the sender-address the funding-transaction from all transactions
    funding_transaction = get_funding_transaction(transactions, sender)
    
    # 4. Extract receiver from the funding-transaction
    receiver_transaction_field = get_fields_from_transaction(funding_transaction, ["receiver"])
    receiver = receiver_transaction_field["receiver"]

    # 5. Extract the application-id to differentiate between different tx's strcutures of protocols
    application_id_transaction_field = get_fields_from_transaction(application_call, ["application-id"])
    application_id = application_id_transaction_field["application-id"]
    # 6. Find the receiving transaction either in application-call-transaction (Tinyman) or with application-id from all transactions
    receiving_transaction = get_receiving_transaction(transactions, application_call, application_id, receiver)

    if (not funding_transaction) or (not receiving_transaction):
        return {} # TODO: Check for Tinyman -> Check if Assets are USDC, goUSD or USDT - all assets go over same address

    # 7. Parse funding-transaction and receiving-transaction for amount and asset-ids
    send_transaction_field = get_fields_from_transaction(funding_transaction, ["asset-id", "amount"])
    amount_send, asset_id_send = send_transaction_field["amount"], send_transaction_field["asset-id"]
    received_transaction_field = get_fields_from_transaction(receiving_transaction, ["asset-id", "amount"])
    amount_received, asset_id_received = received_transaction_field["amount"], received_transaction_field["asset-id"]

    # 8. Extract the round for data-analysis purposes
    round = application_call["confirmed-round"]

    return {
        "round": round,
        "group_id": group_id,
        "sender": sender,
        "receiver": receiver,
        "application-id": application_id,
        "amount_send": amount_send,
        "asset_id_send": asset_id_send,
        "amount_received": amount_received,
        "asset_id_received": asset_id_received
    }
