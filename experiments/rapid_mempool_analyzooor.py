import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_algo_usd_dex_addresses():
    addresses = set()
    addresses.add("SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34")
    addresses.add("LMU5MRQWB3DDSM7J3YY32OBURDL3FHEHQW7J6USTIR5J3HSCNSCDTGDTCU")
    addresses.add("L747MOJV43QCLY4HSWVPL2A5SW62IBLA5XPTI5R4HO32WVAWOO5OBCEP3A")
    addresses.add("KIQDDU4KRXFMUBMLQ75VN5R6RVQHNGHCEX43VSPYHGHBNW27AFNGEZ7EY4")
    addresses.add("FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA")
    addresses.add("54UTVEAHWMBYB4L4BNLAEJFWBUTLLERTULROEEP7774OK6FUTX4U5NX6RM")
    return addresses

def fetch_mempool_data():
    response = requests.get("https://node.algoexplorerapi.io/v2/transactions/pending").json()
    transactions = response["top-transactions"]
    count = response["total-transactions"]
    return count

# if same transaction count -> same mempool
# if increasing -> new transactions
# if decreasing -> maybe new transactions


def main():
    addresses = get_algo_usd_dex_addresses()

    mempool_size = list()
    for i in range(50):
        mempool_size.append(fetch_mempool_data())
    print(mempool_size)

if __name__ == "__main__":
    main()
