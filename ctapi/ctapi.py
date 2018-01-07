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
# URI_API = 'http://127.0.0.1:8080/'


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
            'nonce': 1515332961, #int(time.time() * 10),
        })

        params_string = self._encode_params_url(params)
        # params_signed = hmac.new(self.api_secret.encode(), msg='limit=1&method=getTrades&nonce=1515332961', digestmod=hashlib.sha512).hexdigest()
        # params_signed = hmac.new(self.api_secret.encode(), msg=params_string.encode(), digestmod=hashlib.sha512).hexdigest()
        params_signed = hmac.new(self.api_secret.encode(), msg='limit=1&method=getTrades&nonce=1515332961', digestmod=hashlib.sha512).hexdigest()

        hdrs = {
            'Key': self.api_key,
            'Sign': params_signed,
            'Connection': 'close',
            # 'Content-Type': 'text/text'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }

        logger.debug("="*30)
        logger.debug(params)
        logger.debug(params_string)
        logger.debug(params_signed)
        logger.debug(hdrs)
        logger.debug(self.api_key)
        logger.debug(self.api_secret)
        logger.debug("="*30)

        try:
            # r = requests.post(URI_API, headers=hdrs, data=params_string, verify=False)
            r = requests.post(URI_API, headers=hdrs, data='limit=1&method=getTrades&nonce=1515332962', verify=False)
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
    # ORDERS
    ###########################################################################

    #
    # showOrderbook
    #
    def getTrades(self, **args):
        """ TODO """
        params = {
            'limit': 1,
            # 'limit': 'all',
            # 'order': 'ASC',
            # 'start': 1200000000,
            # 'end': 1450000000,
        }
        params.update(args)
        return self._api_query('getTrades', params)

# async function coinTracking(method, params) {
#     params.method = method;
#     params.nonce = moment().unix();
#
#     var post_data = http_build_query(params, {leave_brackets: false});
#
#     var hash = crypto.createHmac('sha512', secret);
#     hash.update(post_data);
#     var sign = hash.digest('hex');
#
#     var headers =  { 'Key': key, 'Sign': sign};
#
#     var form = new FormData();
#     for(var paramKey in params) {
#         var value = params[paramKey];
#         form.append(paramKey, value);
#     }
#
#     var result = await fetch(url, {
#         method: 'POST',
#         body:   form,
#         headers: headers,
#     });
#     var json = await result.json();
#     return json;
# }
#
# async function getTrades() {
#     var params={};
#     params.limit=200;
#
#     var res = await coinTracking('getTrades', params);
#     console.log(res);
# }
