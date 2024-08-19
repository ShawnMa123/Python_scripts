from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMenuBar, QAction
from PyQt5.QtCore import Qt
from .request_tab import RequestTab
from .response_tab import ResponseTab


class MainWindow(QMainWindow):
    def __init__(self, http_client, history_db):
        super().__init__()
        self.http_client = http_client
        self.history_db = history_db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Python API Client")
        self.setGeometry(100, 100, 1000, 600)

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create and add tabs
        self.request_tab = RequestTab(self.http_client, self.history_db)
        self.response_tab = ResponseTab()

        self.tab_widget.addTab(self.request_tab, "Request")
        self.tab_widget.addTab(self.response_tab, "Response")

        # Connect signals
        self.request_tab.request_sent.connect(self.handle_response)

        # Create menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        clear_action = QAction('Clear All', self)
        clear_action.triggered.connect(self.clear_all)
        edit_menu.addAction(clear_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def handle_response(self, response):
        self.response_tab.display_response(response)
        self.tab_widget.setCurrentIndex(1)  # Switch to response tab

    def clear_all(self):
        self.request_tab.clear_fields()
        self.response_tab.clear_response()

    def show_about(self):
        # Implement about dialog
        pass

