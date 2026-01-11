#importing libraries and modules
import os
import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFileDialog

class UploadPage(QWidget):
    
    next_requested = pyqtSignal()

    def __init__(self,data_handler):
        super().__init__()

        self.data_handler = data_handler

        layout = QVBoxLayout()

        self.title = QLabel("Review Analyser") 
        font = self.title.font() #increasing font size and weight to clearly show application title
        font.setPointSize(50)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.label = QLabel("Load CSV file:")
        font.setPointSize(30) #smaller font size is used for secondary text
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.button = QPushButton("Browse files") #browse files button
        font = self.button.font()
        font.setPointSize(15)
        self.button.setFont(font)
        self.button.setFixedSize(120,50)
        self.button.clicked.connect(self.browse_files)

        self.next_button = QPushButton("Next") #next button (disabled for now)
        self.next_button.setEnabled(False)
        self.next_button.setFixedSize(100,30)

        self.file_label = QLabel() #will display selected file name
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.error_label = QLabel() # holds error message if required
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.next_button.clicked.connect(self.next_requested.emit)

        layout.addStretch() # vertical stretches are used to adjust the position of text within the page
        layout.addWidget(self.title)
        layout.addStretch() 
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.file_label)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addWidget(self.next_button)
        layout.setAlignment(self.next_button, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        self.setLayout(layout)
    
    def browse_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose CSV file", # window title
            "", # opens the last directory the user visited
            "CSV files (*.csv)" # only CSV files are selectable
        )
        if not file_path: # user cancels
            return 
        is_valid, message = self.data_handler.validate_file(file_path)
        if is_valid:
            self.error_label.setText("")
            self.next_button.setEnabled(True)
        if not is_valid:
            self.next_button.setEnabled(False) # in case user previously selected a valid file
            self.error_label.setText(message)
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"Selected file: {file_name}")

class MainWindow(QMainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler

        self.setWindowTitle("Review Analyser")
        self.setMinimumSize(800,600)

        self.stack = QStackedWidget()
 
        self.upload_page = UploadPage(data_handler)
        self.stack.addWidget(self.upload_page)

        self.setCentralWidget(self.stack)
        self.upload_page.next_requested.connect(self.go_next)
    
    def go_next(self):
        pass

