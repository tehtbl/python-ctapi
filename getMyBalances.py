import os

from ctapi import CTAPI

if __name__ == "__main__":

    secrets = {"key": os.environ["key"], "secret": os.environ["secret"]}

    # api = CTAPI(secrets['key'], secrets['secret'], debug=True)
    api = CTAPI(secrets['key'], secrets['secret'])
    balances = api.getBalance()

    if balances['result']['success']:
        sum = 0
        print("+-------+------------+------------+------------+")
        print("|  SYM  |   amount   | price_fiat | value_fiat |")
        print("+-------+------------+------------+------------+")
        for b in balances['result']['details']:
            details = balances['result']['details'][b]
            if float(details['value_fiat']) > 0.01:
                sum = sum + float(details['value_fiat'])
                print("| %5s | %10.2f | %10.2f | %10.2f |" % (b, float(details['amount']),
                    float(details['price_fiat']), float(details['value_fiat']) ))

        print("+-------+------------+------------+------------+")
        print("")
        print("Sum: %15.2f EUR" % (sum))
        print("=" * 24)
    else:
        print("got no balances")
