import requests
from collections import defaultdict

# import classes.application_call as ApplicationCall
# import classes.payment as Payment

BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/blocks/"

def add_transaction_data(transactions, group_collection):
    for transaction in transactions:
        if "group" in transaction:
            transaction_group = transaction["group"]
            if transaction_group in group_collection:
                group_collection[transaction_group].append(transaction)
    return group_collection

def get_swap_application_group_collection(transactions: dict) -> dict:
    group_collection = defaultdict(list)
    for transaction in transactions:
        if "application-transaction" in transaction:
            application_txs = transaction["application-transaction"]
            if is_monitored_application(application_txs["application-id"]):
                group_collection[transaction["group"]]
    return group_collection

def parse_block_data(round: int):
    hash, timestamp, transactions = "", 0, {}
    try:
        response = requests.get(BASE_URL + str(round)).json()
        hash = response["genesis-hash"]
        transactions = response["transactions"]
        timestamp = response["timestamp"]
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"An request error occurred: {e}")
    finally:
        return hash, timestamp, transactions

def get_swap_interactions(block_number):
    hash, timestamp, transactions = parse_block_data(block_number)
    group_collection = get_swap_application_group_collection(transactions)
    group_collection = add_transaction_data(transactions, group_collection)
    return hash, timestamp, group_collection

def is_monitored_application(application_id):
    # "HUMBLESWAP_ALGOUSDC" = "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34" = 777628254
    # "HUMBLESWAP_ALGOgoUSD" = "LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU" = 778663643
    # "PACT_ALGOUSDC" = "L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A" = 620995314
    # "PACT_ALGOUSDT" = "KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4" = 667170441
    # "TINYMAN_ALGOUSDC" = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA" = 552635992 # (4 txs) Here also a fee goes to Tinyman
    # "TINYMAN_ALGOUSDT" = "54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM" = 552635992 # (4 txs) Here also a fee goes to Tinyman
    monitored_dex_list = [777628254, 778663643, 620995314, 667170441, 552635992]
    return True if application_id in monitored_dex_list else False

def get_application_call(transaction_list):
    for transaction in transaction_list:
        if "tx-type" in transaction:
            if transaction["tx-type"] == "appl":
                return transaction
    return None

def get_payment(transaction_list):
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

def get_swap_summary(transactions):
    # TODO: Parse txs from AlgoFi

    application_call = get_application_call(transactions)
    payment = get_payment(transactions)

    group_id = application_call["group"]
    originator = application_call["sender"]
    # address of AMM
    dex_address = payment["sender"]
    # application_id
    application_specs = application_call["application-transaction"]
    application_id = application_specs["application-id"]

    internal_txns = application_call["inner-txns"]
    # amount_send

    # asset_id_send
    #asset_id = internal_txns["asset-id"]

    # amount_received
    # asset_id_received

    # market impact on price
    # price before swap
    # price after swap

    return "[" + group_id + "] - " + originator + "->" + "Application:" + str(application_id) + " (" + dex_address + ") "
