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
__copyright__ = "tbl42 2017"
__version__ = '0.1.0-dev'

# set logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests.packages.urllib3').setLevel(logging.INFO)
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# disable unsecure SSL warning
requests.packages.urllib3.disable_warnings()

URI_API = 'https://cointracking.info/api/v1/'


class CTAPI(object):
    """ requesting CoinTracking API with API key and API secret """

    #
    # init
    #
    def __init__(self, api_key='', api_secret='', debug=False):
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
        """ TODO """

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
        """ TODO """

        global URI_API

        params.update({
            'method': method,
            'nonce': '%d' % int(time.time() * 10),
            # 'nonce': 1515332961,
        })

        params_string = self._encode_params_url(params)
        params_signed = hmac.new(self.api_secret.encode(), msg=params_string.encode(), digestmod=hashlib.sha512).hexdigest()

        hdrs = {
            'Key': self.api_key,
            'Sign': params_signed,
            'Connection': 'close',
            'User-Agent': 'python-cointracking-api/%s (https://github.com/tbl42/python-cointracking-api)' % (__version__),
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
                'success': True,
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
        """ TODO: desc """
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
        """ TODO: desc """
        return self._api_query('getBalance')

    #
    # getHistoricalSummary
    #
    def getHistoricalSummary(self, **args):
        """ TODO: desc """
        params = {
            'btc': 0,
        }
        params.update(args)
        return self._api_query('getHistoricalSummary', params)

    #
    # getHistoricalCurrency
    #
    def getHistoricalCurrency(self, **args):
        """ TODO: desc """
        params = {
            'currency': 'ETH',
        }
        params.update(args)
        return self._api_query('getHistoricalCurrency', params)

    #
    # getGroupedBalance
    #
    def getGroupedBalance(self, **args):
        """ TODO: desc """
        params = {
            'group': 'exchange',
        }
        params.update(args)
        return self._api_query('getGroupedBalance', params)

    #
    # getGains
    #
    def getGains(self, **args):
        """ TODO: desc """
        params = {
            'method': 'FIFO',
        }
        params.update(args)
        return self._api_query('getGains', params)
