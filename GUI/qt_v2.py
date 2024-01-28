import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

# Import the DemoClass from your module
from your_module import DemoClass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Demo Application")

        # Create input label and line edit
        self.input_label = QLabel("Input:", self)
        self.input_label.setGeometry(20, 20, 100, 30)

        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.setGeometry(120, 20, 200, 30)

        # Create result label
        self.result_label = QLabel("Result:", self)
        self.result_label.setGeometry(20, 70, 100, 30)

        # Create result display label
        self.result_display_label = QLabel(self)
        self.result_display_label.setGeometry(120, 70, 200, 30)

        # Create submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(20, 120, 300, 30)
        self.submit_button.clicked.connect(self.calculate_result)

    def calculate_result(self):
        # Get the input value from the line edit
        input_value = self.input_line_edit.text()

        # Create an instance of DemoClass
        demo_obj = DemoClass()

        # Call the specific function and get the result
        result = demo_obj.your_function(input_value)

        # Display the result in the result display label
        self.result_display_label.setText(result)

    def closeEvent(self, event):
        # Override the close event to prevent application exit
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())