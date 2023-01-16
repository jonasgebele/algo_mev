# Analysing MEV on Algorand

## DEX Price Scraper
### Real-Time DEX Price Scraper
```
python realtime_dex_price_scraper.py
```
Output
```
range,HUMBLESWAP_ALGOUSDC,pool_size_X,pool_size_Y,range,HUMBLESWAP_ALGOgoUSD,pool_size_X,pool_size_Y,range,PACT_ALGOUSDC,pool_size_X,pool_size_Y,range,PACT_ALGOUSDT,pool_size_X,pool_size_Y,range,TINYMAN_ALGOUSDC,pool_size_X,pool_size_Y,range,TINYMAN_ALGOUSDT,pool_size_X,pool_size_Y
26291478,0.23952301679350121,3134827659061,750863378026,26291478,0.23818106460034974,223518662377,53237912963,26291478,0.2389845014987845,1771086203325,423262153413,26291478,0.22993773977877519,19252903,4426969,26291478,0.23923943603919579,1520796365656,363834464850,26291478,0.24392474444960519,44028286799,10739588606
26291479,0.23952301679350121,3134827659061,750863378026,26291479,0.23818106460034974,223518662377,53237912963,26291479,0.2389845014987845,1771086203325,423262153413,26291479,0.22993773977877519,19252903,4426969,26291479,0.23923943603919579,1520796365656,363834464850,26291479,0.24392474444960519,44028286799,10739588606
26291480,0.23952301679350121,3134827659061,750863378026,26291480,0.23818106460034974,223518662377,53237912963,26291480,0.2389845014987845,1771086203325,423262153413,26291480,0.22993773977877519,19252903,4426969,26291480,0.23923943603919579,1520796365656,363834464850,26291480,0.24392474444960519,44028286799,10739588606

```
### Historic DEX Price Scraper
Coming Soon.

## Parse Historic Smart Contract Interactions
E.g. parse block number 25729521.
```
python block_tx_scraper.py 25729521 25729522
```
Output ([Swap on DEX](https://algoexplorer.io/tx/group/xOfl513cvxwdHkdTEHhqB%2BmuQ8Z%2F4pLcC9iXCGImw4A%3D)):
```
[
  {
    "payment-transaction": {
      "amount": 300000,
      "close-amount": 0,
      "receiver": "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
    },
    ...
    "sender": "NNEJ6IOFB2D7EUA2VHTFVAUNLY2XZGBMXG5WUW2XJ3IBAJPUW4PNTZ7KIA",
    ...
    "tx-type": "pay"
  },
  {
    "application-transaction": {
      ...
      "application-id": 777628254,
      "foreign-assets": [31566704],
      ...
    },
    ...
    "group": "xOfl513cvxwdHkdTEHhqB+muQ8Z/4pLcC9iXCGImw4A=",
    "id": "2LOER3TT4FUJM6FHQZPME6OX56ZMFP2CTGB3RK5HOX44T7PPHGIA",
    "inner-txns": [
      {
        "asset-transfer-transaction": {
          "amount": 71751,
          "asset-id": 31566704,
          "close-amount": 0,
          "receiver": "NNEJ6IOFB2D7EUA2VHTFVAUNLY2XZGBMXG5WUW2XJ3IBAJPUW4PNTZ7KIA"
        },
        ...
        "sender": "SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34"
      }
    ],
    ...
    "sender": "NNEJ6IOFB2D7EUA2VHTFVAUNLY2XZGBMXG5WUW2XJ3IBAJPUW4PNTZ7KIA"
  }
]
```
