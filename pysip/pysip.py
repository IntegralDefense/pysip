import json
import requests

from urllib.parse import urljoin


class Error(Exception):
    """ Base exception class """

    pass


class RequestError(Error):
    """ Raised when a request returns an error. """

    def __init__(self, msg):
        Error.__init__(self, msg)


class Client:
    def __init__(self, sip_host, apikey, verify=True):

        """
        :param sip_host: server:port where SIP is running
        :param apikey: API key to use for SIP access
        :param verify: True/False or a path to a certificate to use for verification
        """

        self._api_url = 'https://{}/api/'.format(sip_host)
        self._auth_url = 'https://{}/auth'.format(sip_host)
        self._refresh_url = 'https://{}/refresh'.format(sip_host)

        self._apikey = apikey
        self._verify = verify

    def post(self, endpoint, data):
        """ Performs a POST request to the SIP API. """

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.post(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            raise RequestError

        return response

    def get(self, endpoint):
        """ Performs a GET request to the SIP API. """

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.get(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            raise RequestError

        return response

    def put(self, endpoint, data):
        """ Performs a PUT request to the SIP API. """

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.put(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            raise RequestError

        return response

    def delete(self, endpoint):
        """ Performs a DELETE request to the SIP API. """

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.delete(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            raise RequestError

        return response
