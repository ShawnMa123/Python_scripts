import json
from PyQt5.QtCore import QObject, pyqtSignal

class ResponseHandler(QObject):
    response_processed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def process_response(self, response):
        processed_response = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'elapsed': str(response.elapsed),
            'content': self._format_content(response),
            'size': len(response.content),
            'encoding': response.encoding,
            'url': response.url,
        }
        self.response_processed.emit(processed_response)

    def _format_content(self, response):
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            try:
                return json.dumps(response.json(), indent=2)
            except json.JSONDecodeError:
                return response.text
        elif 'text' in content_type or 'xml' in content_type:
            return response.text
        else:
            return f"Binary content ({len(response.content)} bytes)"

    def get_response_summary(self, processed_response):
        return {
            'status_code': processed_response['status_code'],
            'elapsed': processed_response['elapsed'],
            'size': processed_response['size'],
            'type': processed_response['headers'].get('Content-Type', 'Unknown')
        }

    def get_response_headers(self, processed_response):
        return processed_response['headers']

    def get_response_body(self, processed_response):
        return processed_response['content']
