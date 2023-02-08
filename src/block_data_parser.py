import time
import requests
from collections import defaultdict

# import classes.application_call as ApplicationCall
# import classes.payment as Payment

BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/blocks/"

    # "HUMBLESWAP_ALGOUSDC" = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34" = 777628254
    # "HUMBLESWAP_ALGOgoUSD" = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU" = 778663643
    # "PACT_ALGOUSDC" = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A" = 620995314
    # "PACT_ALGOUSDT" = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4" = 667170441
    # "TINYMAN_ALGOUSDC" = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA" = 552635992 # (4 txs) Here also a fee goes to Tinyman
    # "TINYMAN_ALGOUSDT" = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM" = 552635992 # (4 txs) Here also a fee goes to Tinyman

def add_transactions_to_groups(transactions, group_collection):
    for transaction in transactions:
        if "group" in transaction:
            transaction_group = transaction["group"]
            if transaction_group in group_collection:
                group_collection[transaction_group].append(transaction)
    return group_collection

def get_swap_transaction_groups(transactions: dict) -> dict:
    group_collection = defaultdict(list)
    transactions_within_groups = list(transactions)
    for transaction in transactions:
        if not ("group" in transaction):
            transactions_within_groups.remove(transaction)
            continue
        if "application-transaction" in transaction:
            application_txs = transaction["application-transaction"]
            if is_monitored_application(application_txs["application-id"]):
                group_collection[transaction["group"]]
    return group_collection, transactions_within_groups

def is_monitored_application(application_id):
    monitored_dex_list = [777628254, 778663643, 620995314, 667170441, 552635992]
    return True if application_id in monitored_dex_list else False

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

def get_payment_transaction(transaction_list):
    for transaction in transaction_list:
        if "tx-type" in transaction:
            if transaction["tx-type"] == "pay":
                if "payment-transaction" in transaction:
                    payment_transaction = transaction["payment-transaction"]
                    if "amount" in payment_transaction:
                        amount = payment_transaction["amount"]
                        if amount > 2000: # Protocol-Fee for Tinyman-AMM
                            return transaction
    return None

def ticket_of_assetID():
    stablecoin_asset_ids = [312769, 31566704, 672913181] # USDT, USDC, goUSD


def swap_summary(transactions):
    # TODO: Parse txs from AlgoFi
    application_call_transaction = get_application_call_transaction(transactions)
    application_inner_transactions = application_call_transaction["inner-txns"][0]
    application = application_call_transaction["application-transaction"]

    payment_transaction = get_payment_transaction(transactions)
    payment_tx_info = payment_transaction["payment-transaction"]

    group_id = payment_transaction["group"]
    originator = application_inner_transactions["sender"]
    amm_address = payment_transaction["sender"]
    
    application_id = application["application-id"]

    # amount_send
    amount_send = int(payment_tx_info["amount"] / 1000000)
    # asset_id_send
    asset_ids = application["foreign-assets"]
    
    asset_id_send = asset_ids[0] if asset_ids[0] > 0 else asset_ids[1]

    # amount_received
    amount_received = int(application_inner_transactions["asset-transfer-transaction"]["amount"] / 1000000)
    # asset_id_received
    asset_id_received = application_inner_transactions["asset-transfer-transaction"]["asset-id"]

    # market impact on price
    # price before swap
    # price after swap

    return "Tx-Group:" + group_id + " - Sender:" + originator + " " + "ApplicationID:" + str(application_id) + "(" + amm_address + ") \n " + str(amount_send) + "(AssetID:" + str(asset_id_send) + ") " + str(amount_received) + "(AssetID:" + str(asset_id_received) + ")"
