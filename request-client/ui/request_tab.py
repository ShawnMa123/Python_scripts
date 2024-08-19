from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QComboBox)
from PyQt5.QtCore import pyqtSignal

class RequestTab(QWidget):
    request_sent = pyqtSignal(object)

    def __init__(self, http_client, history_db):
        super().__init__()
        self.http_client = http_client
        self.history_db = history_db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Method selection
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH"])
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        layout.addLayout(method_layout)

        # Headers input
        layout.addWidget(QLabel("Headers:"))
        self.headers_input = QTextEdit()
        self.headers_input.setPlaceholderText("Enter headers in Key: Value format, one per line")
        layout.addWidget(self.headers_input)

        # Body input
        layout.addWidget(QLabel("Body:"))
        self.body_input = QTextEdit()
        layout.addWidget(self.body_input)

        # Send button
        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_request)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_request(self):
        url = self.url_input.text()
        method = self.method_combo.currentText()
        headers = self.parse_headers()
        body = self.body_input.toPlainText()

        # Send the request using the http_client
        response = self.http_client.send_request(method, url, headers, body)

        # Save to history
        self.history_db.add_request(method, url, headers, body)

        # Emit the response
        self.request_sent.emit(response)

    def parse_headers(self):
        headers = {}
        header_text = self.headers_input.toPlainText()
        for line in header_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

    def clear_fields(self):
        self.url_input.clear()
        self.method_combo.setCurrentIndex(0)
        self.headers_input.clear()
        self.body_input.clear()

