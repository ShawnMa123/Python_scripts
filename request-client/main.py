import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from core.http_client import HttpClient
from core.request_handler import RequestHandler
from core.response_handler import ResponseHandler
from utils.json_formatter import format_json, is_valid_json, highlight_json
from utils.xml_formatter import format_xml, is_valid_xml, highlight_xml
from database.history_db import HistoryDatabase

def main():
    app = QApplication(sys.argv)

    # Initialize core components
    http_client = HttpClient()
    request_handler = RequestHandler()  # Initialize without parameters
    response_handler = ResponseHandler()

    # Initialize database
    history_db = HistoryDatabase()

    # Create main window
    main_window = MainWindow(
        http_client=http_client,  # Pass http_client directly
        request_handler=request_handler,
        response_handler=response_handler,
        format_json=format_json,
        is_valid_json=is_valid_json,
        highlight_json=highlight_json,
        format_xml=format_xml,
        is_valid_xml=is_valid_xml,
        highlight_xml=highlight_xml,
        history_db=history_db
    )

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
