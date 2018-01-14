import json
import yaml
import unittest

from ctapi import CTAPI

try:
    open("secrets.yml").close()
    IS_CI_ENV = False
except Exception:
    IS_CI_ENV = True

def test_basic_response(unit_test, result, method_name):
    unit_test.assertTrue(result['success'], "%s failed" % method_name)
    unit_test.assertTrue(result['result'] is not None, "result not present in response")
    unit_test.assertTrue(isinstance(result['result'], dict), "result is not a dict")
    # unit_test.assertTrue(result['result']['method'] is method_name, "result method is wrong")

@unittest.skipIf(IS_CI_ENV, 'no account secrets uploaded in CI envieonment, TODO')
class TestCTAPIBasicTests(unittest.TestCase):
    """
    Integration tests for the CoinTracking API

      * These will fail in the absence of an internet connection or if CoinTracking API goes down
      * They require a valid API key and secret issued by CoinTracking
      * They also require the presence of a JSON file called secrets.yml

    It is structured as such:
    ---
    key: '123'
    secret: '456'
    """

    def setUp(self):
        with open("secrets.yml") as f:
            self.secrets = yaml.load(f)
            f.close()

        # self.api = CTAPI(secrets['key'], secrets['secret'], debug=True)
        self.api = CTAPI(self.secrets['key'], self.secrets['secret'])

    def test_handles_invalid_key_or_secret(self):
        self.api = CTAPI('invalidkey', self.secrets['secret'])
        actual = self.api.getBalance()
        self.assertFalse(actual['success'], 'Invalid key, valid secret')

        self.api = CTAPI(None, self.secrets['secret'])
        actual = self.api.getBalance()
        self.assertFalse(actual['success'], 'None key, valid secret')

        self.api = CTAPI(self.secrets['key'], 'invalidsecret')
        actual = self.api.getBalance()
        self.assertFalse(actual['success'], 'valid key, invalid secret')

        self.api = CTAPI(self.secrets['key'], None)
        actual = self.api.getBalance()
        self.assertFalse(actual['success'], 'valid key, None secret')

        self.api = CTAPI('invalidkey', 'invalidsecret')
        actual = self.api.getBalance()
        self.assertFalse(actual['success'], 'invalid key, invalid secret')

    def test_getTrades(self):
        actual = self.api.getTrades()
        test_basic_response(self, actual, "getTrades")

    def test_getBalance(self):
        actual = self.api.getBalance()
        test_basic_response(self, actual, "getBalance")

    def test_getHistoricalSummary(self):
        actual = self.api.getHistoricalSummary()
        test_basic_response(self, actual, "getHistoricalSummary")

    def test_getHistoricalCurrency(self):
        actual = self.api.getHistoricalCurrency()
        test_basic_response(self, actual, "getHistoricalCurrency")

    def test_getGroupedBalance(self):
        actual = self.api.getGroupedBalance()
        test_basic_response(self, actual, "getGroupedBalance")

    def test_getGains(self):
        actual = self.api.getGains()
        test_basic_response(self, actual, "getGains")

if __name__ == '__main__':
    unittest.main()
