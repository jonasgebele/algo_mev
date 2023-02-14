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

def get_swap_funding_transaction(transactions, application_id):
    def humbleswap_funding_transaction(transactions):
        for transaction in transactions:
            if "tx-type" in transaction:
                if transaction["tx-type"] == "pay":
                    return transaction
        return None
    def tinyman_funding_transaction(transactions):
        for transaction in transactions:
            if "tx-type" in transaction:
                if transaction["tx-type"] == "axfer":
                    return transaction
        return None
    def pact_funding_transaction(transactions):
        for transaction in transactions:
            if "tx-type" in transaction:
                if transaction["tx-type"] == "pay":
                    return transaction
        return None

    funding_transaction = None
    if application_id in [777628254, 778663643]:
        funding_transaction = humbleswap_funding_transaction(transactions)
    elif application_id in [620995314, 667170441]:
        funding_transaction = pact_funding_transaction(transactions)
    elif application_id == 552635992:
        funding_transaction = tinyman_funding_transaction(transactions)
    else:
        print("Exception")
    return funding_transaction

def get_swap_receiving_transaction(transactions, application_id, application_call_transaction):
    def humbleswap_receiving_transaction(application_call_transaction):
        return application_call_transaction["inner-txns"][0]
    def tinyman_receiving_transaction(transactions):
        for transaction in transactions:
            if "tx-type" in transaction:
                if transaction["tx-type"] == "pay":
                    if "payment-transaction" in transaction:
                        payment_transaction = transaction["payment-transaction"]
                        if "amount" in payment_transaction:
                            amount = payment_transaction["amount"]
                            if amount > 2000:
                                return transaction
        return None
    def pact_receiving_transaction(application_call_transaction):
        return application_call_transaction["inner-txns"][0]

    receiving_transaction = None
    if application_id in [777628254, 778663643]:
        receiving_transaction = humbleswap_receiving_transaction(application_call_transaction)
    elif application_id in [620995314, 667170441]:
        receiving_transaction = pact_receiving_transaction(application_call_transaction)
    elif application_id == 552635992:
        receiving_transaction = tinyman_receiving_transaction(transactions)
    else:
        print("Exception")
    return receiving_transaction

def get_send_asset_info(funding_transaction, application_id):
    pass

def get_received_asset_info(receiving_transaction, application_i):
    pass

def swap_summary(transactions):
    application_call_transaction = get_application_call_transaction(transactions)
    application_call = application_call_transaction["application-transaction"]
    
    # Application ID
    application_id = application_call["application-id"]

    funding_transaction = get_swap_funding_transaction(transactions, application_id)
    receiving_transaction = get_swap_receiving_transaction(transactions, application_id, application_call_transaction)

    # Group ID
    group_id = application_call_transaction["group"]
    # Sender
    sender = application_call_transaction["sender"]
    # Receiver
    receiver = receiving_transaction["sender"]

    # Send-Amount, Send-Asset
    #amount_send, asset_id_send = get_send_asset_info(funding_transaction, application_id)
    # Received-Amount, Received-Asset
    #amount_received, asset_id_received = get_received_asset_info(receiving_transaction, application_id)

    return group_id, ", Sender:", sender, ", Receiver: ", receiver

    #amount_send = int(payment_tx_info["amount"] / 1000000)
    # asset_id_send

    # amount_received
    # amount_received = int(application_inner_transactions["asset-transfer-transaction"]["amount"] / 1000000)
    # asset_id_received

    # return "Tx-Group:" + group_id + " - Sender:" + sender + " " + "ApplicationID:" + str(application_id) + "(" + receiver + ") \n " + str(amount_send) + "(AssetID:" + str(asset_id_send) + ") " + str(amount_received) + "(AssetID:" + str(asset_id_received) + ")"
