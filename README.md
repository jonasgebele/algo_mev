# Analysing MEV on Algorand

## DEX Price Scraper
```
python price_scraper.py
```
Output
```
timestamp,priceBinanceSpot[ALGOUSDT],priceHumbeSwap[ALGOUSDC],priceHumbeSwap[ALGOgoUSD],pricePact[ALGOUSDC],pricePact[ALGOUSDT],priceTinyman[ALGOUSDC],priceTinyman[ALGOUSDT]
1671452629.22,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452633.58,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452637.64,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452641.9,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452646.53,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452651.07,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
1671452654.96,0.18465,0.185404,0.194214,0.184586,0.182313,0.184843,0.187997
```

## DeFi-Tx Extractor from Block-Data
To parse block number 25729521.
```
python block_tx_scraper.py 25729521 25729522
```
Output:
```
{
  "application-transaction": {
    "accounts": [],
    "application-args": ["c2Vm", "AAAAAAOhVDE="],
    "application-id": 906655543,
    "foreign-apps": [605753404],
    "foreign-assets": [],
    "global-state-schema": { "num-byte-slice": 0, "num-uint": 0 },
    "local-state-schema": { "num-byte-slice": 0, "num-uint": 0 },
    "on-completion": "noop"
  },
  "close-rewards": 0,
  "closing-amount": 0,
  "confirmed-round": 25729521,
  "fee": 2000,
  "first-valid": 25729519,
  "genesis-hash": "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=",
  "genesis-id": "mainnet-v1.0",
  "global-state-delta": [
    { "key": "YjE=", "value": { "action": 2, "uint": 22034199484 } },
    { "key": "YjI=", "value": { "action": 2, "uint": 1012002638086 } },
    { "key": "Y2Yy", "value": { "action": 2, "uint": 112901558396 } },
    { "key": "Y3QxMg==", "value": { "action": 2, "uint": 190581425106354838 } },
    { "key": "Y3QyMQ==", "value": { "action": 2, "uint": 188644187568773 } },
    { "key": "Y3Yx", "value": { "action": 2, "uint": 3309131195611 } },
    { "key": "Y3Yy", "value": { "action": 2, "uint": 89535139914772 } },
    {
      "key": "Y3YyMQ==",
      "value": { "action": 2, "uint": 7755260410652402800 }
    },
    { "key": "bHQ=", "value": { "action": 2, "uint": 1671725524 } }
  ],
  "group": "HBmRZZYHBy3F6zc62GHn/5l3RWpI4WwvW6YpXsYJ3Yk=",
  "id": "LKELNLN6KFQOXPXNRBAS6HT7L6XLY2SIGSIADI3CF56WQM3VES7Q",
  "inner-txns": [
    {
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 25729521,
      "fee": 0,
      "first-valid": 25729519,
      "intra-round-offset": 53,
      "last-valid": 25730519,
      "payment-transaction": {
        "amount": 60904497,
        "close-amount": 0,
        "receiver": "ODKHWTGQUBJ2I62QBLBL3BZP5YUSPJ5OVL7JHUKCJOE3T4YET6RXVT65QY"
      },
      "receiver-rewards": 0,
      "round-time": 1671725527,
      "sender": "UO47CTCILYLSKVMDCBGDVV75V74QQQ45YDSGAHEOOBS4NQ7JTZIHMWZYWQ",
      "sender-rewards": 0,
      "tx-type": "pay"
    }
  ],
  "intra-round-offset": 53,
  "last-valid": 25730519,
  "receiver-rewards": 0,
  "round-time": 1671725527,
  "sender": "ODKHWTGQUBJ2I62QBLBL3BZP5YUSPJ5OVL7JHUKCJOE3T4YET6RXVT65QY",
  "sender-rewards": 0,
  "signature": {
    "sig": "kE1OvD93uGtmCglypdFZ/4Jy9MQgM57qgCTKHZfoe87EMoAfa4Laz1ANx2vA1h34voZesr1/o87DOEd5oEYpBw=="
  },
  "tx-type": "appl"
}

```
