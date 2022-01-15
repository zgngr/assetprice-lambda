# assetprice-lambda

Install dependencies
```
pip3 install -r requirements.txt
```

Local testing
```
chalice local
```

**Crypto price request response**
  ```
  curl 'localhost:8000/crypto?symbols=ETH,BTC'
  ```
 
 `{"ETH_USD":3345.45,"BTC_USD":43407.56}`

**Stock price request response**
  ```
  curl 'localhost:8000/stock?symbols=AAPL,MSFT
  ```
  
 `{"AAPL":173.07000732421875,"MSFT":310.20001220703125}`


Deploy to AWS
```
chalice deploy
```
