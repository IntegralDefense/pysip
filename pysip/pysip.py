import json
import requests

from urllib.parse import urljoin


class Error(Exception):
    """ Base exception class """

    pass


class AccessTokenExpired(Error):
    """ Raised when the access token has expired. """

    def __init__(self):
        Error.__init__(self, 'Access token has expired')


class RefreshTokenExpired(Error):
    """ Raised when the refresh token has expired. """

    def __init__(self):
        Error.__init__(self, 'Refresh token has expired')


class InvalidLogin(Error):
    """ Raised when the user supplies an invalid username or password. """

    def __init__(self):
        Error.__init__(self, 'Invalid username or password')


class InvalidRequest(Error):
    """ Raised when a request returns an error. """

    def __init__(self, msg):
        Error.__init__(self, msg)


class Client:
    def __init__(self, sip_host, verify=True):

        """
        :param sip_host: server:port where SIP is running
        :param verify: True/False or a path to a certificate to use for verification
        """

        self._api_url = 'https://{}/api/'.format(sip_host)
        self._auth_url = 'https://{}/auth'.format(sip_host)
        self._refresh_url = 'https://{}/refresh'.format(sip_host)

        self._verify = verify
        self._access_token = None
        self._refresh_token = None

    def login(self, username, password):
        """ Logs into SIP to obtain an access and refresh token. """

        request = requests.post(self._auth_url, data={'username': username, 'password': password}, verify=self._verify)

        if request.status_code == 401:
            raise InvalidLogin

        response = json.loads(request.text)
        self._access_token = response['access_token']
        self._refresh_token = response['refresh_token']

    def refresh_token(self):
        """ Refreshes the access token. """

        if self._refresh_token:
            headers = {'Authorization': 'Bearer {}'.format(self._refresh_token)}
            request = requests.post(self._refresh_url, headers=headers, verify=self._verify)

            if request.status_code == 401:
                raise RefreshTokenExpired

            response = json.loads(request.text)
            self._access_token = response['access_token']

    def post(self, endpoint, data):
        """ Performs a POST request to the SIP API. """

        headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
        request = requests.post(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if request.status_code == 401 and response['msg'] == 'Token has expired':
            raise AccessTokenExpired

        return response

    def get(self, endpoint):
        """ Performs a GET request to the SIP API. """

        headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
        request = requests.get(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if request.status_code == 401 and response['msg'] == 'Token has expired':
            raise AccessTokenExpired

        return response

    def put(self, endpoint, data):
        """ Performs a PUT request to the SIP API. """

        headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
        request = requests.put(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if request.status_code == 401 and response['msg'] == 'Token has expired':
            raise AccessTokenExpired

        return response

    def delete(self, endpoint):
        """ Performs a DELETE request to the SIP API. """

        headers = {'Authorization': 'Bearer {}'.format(self._access_token)}
        request = requests.delete(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if request.status_code == 401 and response['msg'] == 'Token has expired':
            raise AccessTokenExpired

        return response
