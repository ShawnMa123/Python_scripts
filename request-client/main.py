import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, \
    QPushButton, QComboBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
import requests

from utils.xml_formatter import format_xml, is_valid_xml, highlight_xml
from database.history_db import HistoryDatabase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced HTTP Client")
        self.setGeometry(100, 100, 1000, 800)

        self.history_db = HistoryDatabase()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Request section
        request_layout = QHBoxLayout()
        method_combo = QComboBox()
        method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH"])
        self.url_input = QLineEdit()
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_request)

        request_layout.addWidget(method_combo)
        request_layout.addWidget(self.url_input)
        request_layout.addWidget(send_button)

        main_layout.addLayout(request_layout)

        # Tabs for request details, response, and history
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Request details tab
        request_tab = QWidget()
        request_layout = QVBoxLayout()
        request_tab.setLayout(request_layout)

        self.headers_input = QTextEdit()
        self.headers_input.setPlaceholderText("Enter headers (one per line, key: value)")
        request_layout.addWidget(QLabel("Headers:"))
        request_layout.addWidget(self.headers_input)

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Enter request body")
        request_layout.addWidget(QLabel("Body:"))
        request_layout.addWidget(self.body_input)

        tabs.addTab(request_tab, "Request")

        # Response tab
        response_tab = QWidget()
        response_layout = QVBoxLayout()
        response_tab.setLayout(response_layout)

        self.response_status = QLabel()
        response_layout.addWidget(self.response_status)

        self.response_headers = QTextEdit()
        self.response_headers.setReadOnly(True)
        response_layout.addWidget(QLabel("Response Headers:"))
        response_layout.addWidget(self.response_headers)

        self.response_body = QTextEdit()
        self.response_body.setReadOnly(True)
        response_layout.addWidget(QLabel("Response Body:"))
        response_layout.addWidget(self.response_body)

        tabs.addTab(response_tab, "Response")

        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout()
        history_tab.setLayout(history_layout)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["ID", "Method", "URL", "Timestamp"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.cellDoubleClicked.connect(self.load_history_entry)
        history_layout.addWidget(self.history_table)

        clear_history_button = QPushButton("Clear History")
        clear_history_button.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_history_button)

        tabs.addTab(history_tab, "History")

        self.load_history()

    def send_request(self):
        url = self.url_input.text()
        method = self.sender().parent().findChild(QComboBox).currentText()
        headers = self.parse_headers(self.headers_input.toPlainText())
        body = self.body_input.toPlainText()

        try:
            response = requests.request(method, url, headers=headers, data=body)
            self.display_response(response)
            self.history_db.add_entry(method, url, str(headers), body, response.status_code, response.text)
            self.load_history()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Request Error", str(e))

    def parse_headers(self, headers_text):
        headers = {}
        for line in headers_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

    def display_response(self, response):
        self.response_status.setText(f"Status: {response.status_code} {response.reason}")
        self.response_headers.setText("\n".join([f"{k}: {v}" for k, v in response.headers.items()]))

        body = response.text
        if is_valid_xml(body):
            body = format_xml(body)
            self.response_body.setPlainText(body)
            self.apply_xml_highlighting()
        else:
            self.response_body.setPlainText(body)

    def apply_xml_highlighting(self):
        highlights = highlight_xml(self.response_body.toPlainText())
        cursor = self.response_body.textCursor()
        for start, length, format in highlights:
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length)
            cursor.setCharFormat(format)

    def load_history(self):
        self.history_table.setRowCount(0)
        for entry in self.history_db.get_all_entries():
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(str(entry[0])))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(entry[1]))
            self.history_table.setItem(row_position, 2, QTableWidgetItem(entry[2]))
            self.history_table.setItem(row_position, 3, QTableWidgetItem(entry[7]))

    def load_history_entry(self, row, column):
        entry_id = int(self.history_table.item(row, 0).text())
        entry = self.history_db.get_entry_by_id(entry_id)
        if entry:
            method, url, headers, body = entry[1], entry[2], entry[3], entry[4]
            self.url_input.setText(url)
            self.headers_input.setPlainText(headers)
            self.body_input.setPlainText(body)
            method_combo = self.findChild(QComboBox)
            method_combo.setCurrentText(method)

    def clear_history(self):
        reply = QMessageBox.question(self, "Clear History", "Are you sure you want to clear all history?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history_db.clear_history()
            self.load_history()

    def closeEvent(self, event):
        self.history_db.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
