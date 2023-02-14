import csv

CSV_FILE_PATH = "./markets.csv"

def read_csv_column(column) -> set:
    set_ = set()
    with open(CSV_FILE_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            set_.add(row[column])
    return set_

def get_market_names() -> set:
    market_names = read_csv_column('market_name')
    return market_names

def get_pimary_assets() -> set:
    prim_assets = read_csv_column('asset_0')
    return prim_assets

def get_secondary_assets() -> set:
    sec_assets = read_csv_column('asset_1')
    return sec_assets

def get_addresses() -> set:
    sec_assets = read_csv_column('address')
    return sec_assets

def get_application_ids() -> set:
    sec_assets = read_csv_column('application_id')
    return sec_assets

def get_markets() -> dict:
    markets = dict()
    with open(CSV_FILE_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            key = row['market_name'] + '_' + row['asset_0'] + row['asset_1']
            markets[key] = row['address'], int(row['application_id'])
    return markets
