# python-cointracking-api

Python Interface for [CoinTracking.info API](https://cointracking.info/api/api.php)

# Requirements:

* requests
* futures

# Install
```

```

# How to Use

This is an example how you can use the library in a python script
```
#! /usr/bin/env python

from ctapi import CTAPI

api_key = <YourAPIKey>
api_secret = <YourAPISecret>

api = CTAPI(api_key, api_secret)
trades = api.getTrades()

if trades['success']:
    print 'credits left: {0}'.format(trades['result']['credits'])

    for order in trades['result']['orders']:
        print 'Order ID: {0} >>> Price: {1} EUR'.format(order['order_id'], order['price'])
else:
    print "got no orders"
```


POST /api/v1/getTrades HTTP/1.1
Host: cointracking.info
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Key: 5f3ab6b651b5ae77ca85ea20baa955fc
Sign: 33b3c257ab3dab73e593bf9ba90ee722bf257632dcdcdb26aae6ca1c0fa21c983568da463d06030581b0de596541c344c8ec337370d3eec2889657e9a03af381
Content-Length: 34

method=getTrades&nonce=15153302975