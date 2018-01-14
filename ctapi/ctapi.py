"""
    See https://cointracking.info/api/api.php
"""

try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urljoin

import time
import hmac
import logging
import hashlib

import requests

__author__ = "tbl42"
__copyright__ = "(C) 2018 https://github.com/tbl42/"
__version__ = '0.3.0'

# set logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests.packages.urllib3').setLevel(logging.INFO)
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# disable unsecure SSL warning
requests.packages.urllib3.disable_warnings()

URI_API = 'https://cointracking.info/api/v1/'

#
# API object
#
class CTAPI(object):
    """
    requesting CoinTracking API with API key and API secret

    Documentation: https://cointracking.info/api/api.php
    """

    #
    # init
    #
    def __init__(self, api_key=None, api_secret=None, debug=False):
        # if not self.api_key or not self.api_secret:


        self.api_key = api_key
        self.api_secret = api_secret
        self.debug = debug

        if self.debug:
            import http.client
            http.client.HTTPConnection.debuglevel = 1
            logging.getLogger('requests.packages.urllib3').setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("creating instance of CoinTracking API with api_key %s" % self.api_key)

    #
    # encode parameters for url
    #
    def _encode_params_url(self, params):
        """
        encoding URL parameters

        :params: Request parameters to be encoded
        """

        encoded_string = ''

        if params:
            # for key, value in sorted(params.items()):
            for key, value in params.items():
                encoded_string += str(key) + '=' + str(value) + '&'
            encoded_string = encoded_string[:-1]

        return encoded_string

    #
    # make query to API
    #
    def _api_query(self, method, params={}):
        """
        Queries CoinTracking.info

        :method: Request method
        :params: Request parameters
        :return: JSON response from Bittrex
        """

        global URI_API

        params.update({
            'method': method,
            'nonce': '%d' % int(time.time() * 10),
        })

        if not self.api_secret:
            return {
                'success': False,
                'message': 'no valid secret key',
            }

        params_string = self._encode_params_url(params)
        params_signed = hmac.new(self.api_secret.encode(), msg=params_string.encode(), digestmod=hashlib.sha512).hexdigest()

        hdrs = {
            'Key': self.api_key,
            'Sign': params_signed,
            'Connection': 'close',
            'User-Agent': 'python-ctapi/%s (https://github.com/tbl42/python-ctapi)' % (__version__),
        }

        logger.debug("="*30)
        logger.debug(params)
        logger.debug(params_string)
        logger.debug(params_signed)
        logger.debug(hdrs)
        logger.debug("="*30)

        try:
            new_params = {}
            for k in params.keys():
                new_params[k] = (None, str(params[k]))

            r = requests.post(URI_API, headers=hdrs, files=new_params, verify=False)
            ret_json = r.json()

            return {
                'success': ret_json['success'],
                'result': ret_json
            }
        except:
            return {
                'success': False,
                'message': "error connecting to API"
            }

    ###########################################################################
    # API methods
    ###########################################################################

    #
    # getTrades
    #
    def getTrades(self, **args):
        """
        Used to get all your CoinTracking trades and transactions.
        Similar to the Trade List at https://cointracking.info/trades_full.php
        """

        params = {
            'limit': 5,
            'order': 'DESC',
        }
        params.update(args)

        return self._api_query('getTrades', params)

    #
    # getBalance
    #
    def getBalance(self):
        """
        Used to get your current CoinTracking account and coin balance.
        Similar to the Current Balance at https://cointracking.info/current_balance.php
        """

        return self._api_query('getBalance')

    #
    # getHistoricalSummary
    #
    def getHistoricalSummary(self, **args):
        """
        Used to get all historical values for all your coins, currencies, commodities, and the total account value.
        Similar to the Daily Balance at https://cointracking.info/overview.php or the Trade Statistics at https://cointracking.info/stats.php
        """

        params = {
            'btc': 0,
        }
        params.update(args)

        return self._api_query('getHistoricalSummary', params)

    #
    # getHistoricalCurrency
    #
    def getHistoricalCurrency(self, **args):
        """
        Used to get all historical amounts and values for a specific currency/coin or for all currencies/coins.
        Similar to the Daily Balance at https://cointracking.info/overview.php or the Trade Statistics at https://cointracking.info/stats.php
        """

        params = {
            'currency': 'ETH',
        }
        params.update(args)

        return self._api_query('getHistoricalCurrency', params)

    #
    # getGroupedBalance
    #
    def getGroupedBalance(self, **args):
        """
        Used to get the current balance grouped by exchange, trade-group or transaction type.
        Similar to the Balance by Exchange at https://cointracking.info/balance_by_exchange.php
        """

        params = {
            'group': 'exchange',
        }
        params.update(args)

        return self._api_query('getGroupedBalance', params)

    #
    # getGains
    #
    def getGains(self, **args):
        """
        Used to get Returns your current realized and unrealized gains data.
        Similar to the Realized and Unrealized Gains at https://cointracking.info/gains.php
        """

        params = {
            'method': 'FIFO',
        }
        params.update(args)

        return self._api_query('getGains', params)
