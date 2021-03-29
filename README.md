# etrade-sdk
Python SDK for Etrade REST API 
This SDK implements all REST API calls for the Etrade API listed here: https://apisb.etrade.com/docs/api/account/api-account-v1.html
This class has been tested and is in use in my own personal python trading scripts.

# Authentication Requirements
In order to leverage this (and the REST API) you must have an API enabled Etrade account with both a 'consumer key' and a 'consumer secret'. When authenticating, the OAuth modules will attempt to authenticate and open a web browser window which you must follow to login. The SDK will then ask for a verification token. Simply paste this value back into the script to complete the interactive authentication.

# Usage Examples

## How to authenticate interactively and get a listing of accounts
```
import etrade
sdk = etrade.API()
sdk.authenticate()

### Consumer Key not set. Please enter the consumer key: abcd... [input redacted]
### Consumer Secret not set. Please enter the consumer key: fedcba... [input redacted]
### Please input the verifier: 1234... [input redacted]

accounts_list = sdk.accounts.list_accounts()
# JSON Dump output of the accounts list
sdk.jd(accounts_list)
```

## How to preset the consumer keys/secrets and get a stock quote for google
```
import etrade
sdk = etrade.API()
sdk.attributes['consumer_key'] = '....aaabbbccc.....'
sdk.attributes['consumer_secret'] =  '....fffeeeddd.....'
sdk.authenticate()
# Please input the verifier: 5432... [input redacted]

stock_label = "goog"
stock_quote = sdk.markets.get_quotes(stock_label)
try:
  last_trade_price = stock_quote['QuoteResponse']['QuoteData']['All']['lastTrade']
  print("Last Trade Price for",stock_label,"is",last_trade_price)
except:
  print("Error getting last trade price. RAW DATA:")
  sdk.jd(stock_quote) ## JSON Dump output of response
```
  
## How to iterate through all ALERTS on your account and print the ID and Detail
```
import etrade
sdk = etrade.API()
sdk.attributes['consumer_key'] = '....aaabbbccc.....'
sdk.attributes['consumer_secret'] =  '....fffeeeddd.....'
sdk.authenticate()
# Please input the verifier: 5432... [input redacted]

result = sdk.alerts.list_alerts()
try:
  alerts_list = result.get("AlertsResponse",{}).get("Alert",[])
  for alert in alerts_list:
    print(alert['id'],":", alert['subject'],"-",alert['status'])
except:
  print("Error retrieving alerts")
```

# Other system dependencies
This SDK makes heavy use of the following libraries:
- xmltodict
- rauth
- webbrowser (for interactive authentication)
- json

