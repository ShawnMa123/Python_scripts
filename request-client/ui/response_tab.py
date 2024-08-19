from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTextEdit, QTabWidget, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt
import json


class ResponseTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Status and time
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Status: ")
        self.time_label = QLabel("Time: ")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.time_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Response content tabs
        self.content_tabs = QTabWidget()

        # Raw response tab
        self.raw_response = QTextEdit()
        self.raw_response.setReadOnly(True)
        self.content_tabs.addTab(self.raw_response, "Raw")

        # Headers tab
        self.headers_tree = QTreeWidget()
        self.headers_tree.setHeaderLabels(["Header", "Value"])
        self.content_tabs.addTab(self.headers_tree, "Headers")

        # JSON tab
        self.json_tree = QTreeWidget()
        self.json_tree.setHeaderLabels(["Key", "Value"])
        self.content_tabs.addTab(self.json_tree, "JSON")

        layout.addWidget(self.content_tabs)
        self.setLayout(layout)

    def display_response(self, response):
        # Update status and time
        self.status_label.setText(f"Status: {response.status_code}")
        self.time_label.setText(f"Time: {response.elapsed.total_seconds():.2f} s")

        # Update raw response
        self.raw_response.setText(response.text)

        # Update headers
        self.headers_tree.clear()
        for key, value in response.headers.items():
            item = QTreeWidgetItem(self.headers_tree)
            item.setText(0, key)
            item.setText(1, value)

        # Update JSON view if applicable
        self.json_tree.clear()
        try:
            json_data = json.loads(response.text)
            self.populate_json_tree(json_data)
            self.content_tabs.setTabEnabled(2, True)  # Enable JSON tab
        except json.JSONDecodeError:
            self.content_tabs.setTabEnabled(2, False)  # Disable JSON tab if not valid JSON

    def populate_json_tree(self, data, parent=None):
        if parent is None:
            parent = self.json_tree.invisibleRootItem()

        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, str(key))
                if isinstance(value, (dict, list)):
                    self.populate_json_tree(value, item)
                else:
                    item.setText(1, str(value))
        elif isinstance(data, list):
            for i, value in enumerate(data):
                item = QTreeWidgetItem(parent)
                item.setText(0, str(i))
                if isinstance(value, (dict, list)):
                    self.populate_json_tree(value, item)
                else:
                    item.setText(1, str(value))

    def clear_response(self):
        self.status_label.setText("Status: ")
        self.time_label.setText("Time: ")
        self.raw_response.clear()
        self.headers_tree.clear()
        self.json_tree.clear()
        self.content_tabs.setTabEnabled(2, False)  # Disable JSON tab

