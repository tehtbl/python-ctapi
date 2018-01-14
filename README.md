# python-ctapi
Python interface for [CoinTracking.info API](https://cointracking.info/api/api.php).

I am not associated to cointracking.info -- use at your own risk!

# Requirements:
* requests

# Install
`python setup.py install`
`pip install python-ctapi`

# How to Use
This is an example about how you can use the library

```
#!/usr/bin/env python2

from ctapi import CTAPI

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

# Running Tests
**be aware of the API requests limit of 20 req/h**
`venv/bin/python -m unittest -v ctapi.test.ctapi_tests`

# Contribute
Do you have an idea or found a bug in python-ctapi? Please file an issue and make a PR! :)

## Support Me
If you like the API and wanna support its developer, use the following referral link when registering at cointracking: https://cointracking.info?ref=T161519
