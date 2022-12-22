# Analysing MEV on Algorand

## DEX Price Scraper
### Real-Time DEX Price Scraper
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
