import json
import requests
import socket

from contextlib import closing
from urllib.parse import urljoin


class Error(Exception):
    """ Base exception class """

    pass


class ConflictError(Error):
    """ Raised when a request returns a 409 Conflict error."""

    def __init__(self, msg):
        Error.__init__(self, msg)


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
        self._apikey = apikey
        self._verify = verify

        # Check if the SIP host is alive.
        if ':' in sip_host:
            host = sip_host.split(':')[0]
            port = int(sip_host.split(':')[1])
        else:
            host = sip_host
            port = 443

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(2)
            if sock.connect_ex((host, port)) != 0:
                raise ConnectionError('Unable to connect to SIP at {}:{}'.format(host, port))

    def post_file(self, endpoint, file_path):
        """ Performs a POST request to the SIP API using the JSON contents of the file path. """

        with open(file_path) as f:
            data = json.load(f)
        self.post(endpoint, data)

    def post(self, endpoint, data):
        """ Performs a POST request to the SIP API. """

        # Clean up the given endpoint.
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        endpoint = endpoint.replace('api/', '')

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.post(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        if request.status_code == 204:
            response = ''
        else:
            response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            if request.status_code == 409:
                raise ConflictError(request.text)
            else:
                raise RequestError(request.text)

        return response

    def get(self, endpoint):
        """ Performs a GET request to the SIP API. """

        # Clean up the given endpoint.
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        endpoint = endpoint.replace('api/', '')

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.get(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)

        if not str(request.status_code).startswith('2'):
            raise RequestError(request.text)

        response = json.loads(request.text)

        return response

    def get_all_pages(self, endpoint):
        """ Performs multiple GET requests to get all of the paginated results. """

        all_items = []

        result = self.get(endpoint)

        if 'items' in result:
            all_items += result['items']
            next_page = result['_links']['next']
            while next_page:
                result = self.get(next_page)
                if result['items']:
                    all_items += result['items']
                next_page = result['_links']['next']
        else:
            if isinstance(result, dict):
                all_items = [result]
            else:
                all_items = result

        return all_items

    def put(self, endpoint, data):
        """ Performs a PUT request to the SIP API. """

        # Clean up the given endpoint.
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        endpoint = endpoint.replace('api/', '')

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.put(urljoin(self._api_url, endpoint), json=data, headers=headers, verify=self._verify)
        response = json.loads(request.text)

        if not str(request.status_code).startswith('2'):
            if request.status_code == 409:
                raise ConflictError(request.text)
            else:
                raise RequestError(request.text)

        return response

    def delete(self, endpoint):
        """ Performs a DELETE request to the SIP API. """

        # Clean up the given endpoint.
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        endpoint = endpoint.replace('api/', '')

        headers = {'Authorization': 'Apikey {}'.format(self._apikey)}
        request = requests.delete(urljoin(self._api_url, endpoint), headers=headers, verify=self._verify)
        response = request.text

        if not str(request.status_code).startswith('2'):
            if request.status_code == 409:
                raise ConflictError(request.text)
            else:
                raise RequestError(request.text)

        return response
