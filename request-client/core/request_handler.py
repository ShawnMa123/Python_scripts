from .http_client import HttpClient
from PyQt5.QtCore import QObject, pyqtSignal

class RequestHandler(QObject):
    request_started = pyqtSignal()
    request_finished = pyqtSignal(object)
    request_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.http_client = HttpClient()

    def send_request(self, method, url, headers=None, body=None):
        self.request_started.emit()

        try:
            # Convert headers from list of tuples to dictionary
            headers_dict = dict(headers) if headers else {}

            # Send the request
            response = self.http_client.send_request(method, url, headers_dict, body)

            # Emit the response
            self.request_finished.emit(response)

        except Exception as e:
            # Emit any unexpected errors
            self.request_error.emit(str(e))

    def set_proxy(self, proxy_url):
        try:
            self.http_client.set_proxy(proxy_url)
        except Exception as e:
            self.request_error.emit(f"Error setting proxy: {str(e)}")

    def clear_proxy(self):
        try:
            self.http_client.clear_proxy()
        except Exception as e:
            self.request_error.emit(f"Error clearing proxy: {str(e)}")

    def set_ssl_verify(self, verify):
        try:
            self.http_client.set_ssl_verify(verify)
        except Exception as e:
            self.request_error.emit(f"Error setting SSL verification: {str(e)}")

    def set_timeout(self, timeout):
        try:
            self.http_client.set_timeout(timeout)
        except Exception as e:
            self.request_error.emit(f"Error setting timeout: {str(e)}")

    def close(self):
        self.http_client.close()
