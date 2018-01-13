import json
import yaml
import unittest

from ctapi import CTAPI

try:
    open("secrets.yml").close()
    IS_CI_ENV = False
except Exception:
    IS_CI_ENV = True

# def test_basic_response(unit_test, result, method_name):
#     unit_test.assertTrue(result['success'], "{0:s} failed".format(method_name))
#     unit_test.assertTrue(result['message'] is not None, "message not present in response")
#     unit_test.assertTrue(result['result'] is not None, "result not present in response")


# {'result': {u'error_msg': u'ERROR: Sign is not correct', u'method': u'getBalance', u'success': 0, u'error': u'SIGN_INCORRECT'}, 'success': True}
# {'result': {u'error_msg': u'ERROR: API Key not set', u'method': u'getBalance', u'success': 0, u'error': u'KEY_MISSING'}, 'success': True}
# {'result': {u'error_msg': u'ERROR: Sign is not correct', u'method': u'getBalance', u'success': 0, u'error': u'SIGN_INCORRECT'}, 'success': True}

def test_auth_basic_failures(unit_test, result, test_type):
    pass

    # unit_test.assertFalse(result['success'], "{0:s} failed".format(test_type))
    # unit_test.assertTrue('invalid' in str(result['message']).lower(), "{0:s} failed response message".format(test_type))
    # unit_test.assertIsNone(result['result'], "{0:s} failed response result not None".format(test_type))


@unittest.skipIf(IS_CI_ENV, 'no account secrets uploaded in CI envieonment, TODO')
class TestCoinTrackingAPIBasicTests(unittest.TestCase):
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

    # def test_get_balances(self):
    #     actual = self.bittrex.get_balances()
    #     test_basic_response(self, actual, "get_balances")
    #     self.assertTrue(isinstance(actual['result'], list), "result is not a list")


if __name__ == '__main__':
    unittest.main()
