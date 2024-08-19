import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse

class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url, headers=None, body=None):
        try:
            # Ensure the URL has a scheme
            if not urlparse(url).scheme:
                url = f"http://{url}"

            # Prepare the request
            request_kwargs = {
                'method': method,
                'url': url,
                'headers': headers or {},
                'timeout': 30  # Set a default timeout
            }

            # Add body for appropriate methods
            if method in ['POST', 'PUT', 'PATCH']:
                request_kwargs['data'] = body

            # Send the request
            response = self.session.request(**request_kwargs)

            # Raise an exception for bad status codes
            response.raise_for_status()

            return response

        except RequestException as e:
            # Handle request exceptions
            error_response = requests.Response()
            error_response.status_code = getattr(e.response, 'status_code', 500)
            error_response.text = str(e)
            error_response.elapsed = getattr(e.response, 'elapsed', None)
            error_response.headers = getattr(e.response, 'headers', {})
            return error_response

    def set_proxy(self, proxy_url):
        """Set a proxy for all requests."""
        self.session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

    def clear_proxy(self):
        """Clear any set proxy."""
        self.session.proxies = {}

    def set_ssl_verify(self, verify):
        """Set SSL verification for HTTPS requests."""
        self.session.verify = verify

    def set_timeout(self, timeout):
        """Set a default timeout for all requests."""
        self.session.timeout = timeout

    def close(self):
        """Close the session."""
        self.session.close()
