# python-cointracking-api

Python Interface for [CoinTracking.info API](https://cointracking.info/api/api.php)

# Requirements:

* requests
* futures

# Install
```
python setup.py install
```

# How to Use

This is an example how you can use the library:
```
#!/usr/bin/env python2

from ctapi.ctapi import CTAPI

api_key = <YourAPIKey>
api_secret = <YourAPISecret>

# api = CTAPI(api_key, api_secret, debug=True)
api = CTAPI(api_key, api_secret)
trades = api.getTrades()

if trades['success']:
    for t in trades['result']:
        print trades['result'][t]

else:
    print "got no orders"
    
print api.getBalance()
print api.getHistoricalSummary()
print api.getHistoricalCurrency()
print api.getGroupedBalance()
print api.getGains()

```
