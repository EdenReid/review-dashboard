#importing libraries and modules
import os
import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFileDialog, QHBoxLayout, QCalendarWidget

class UploadPage(QWidget):

    next_requested = pyqtSignal()

    def __init__(self, data_handler):
        super().__init__()

        self.data_handler = data_handler
        layout = QVBoxLayout()

        title = QLabel("Review Analyser")
        font = title.font()
        font.setPointSize(50)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        label = QLabel("Load CSV file:")
        font.setPointSize(30)
        font.setBold(False)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.button = QPushButton("Browse files")
        font = self.button.font()
        font.setPointSize(15)
        self.button.setFont(font)
        self.button.setFixedSize(120, 50)
        self.button.clicked.connect(self.browse_files)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.setFixedSize(100, 30)
        self.next_button.clicked.connect(self.next_requested.emit)

        self.file_label = QLabel()
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.file_label)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignHCenter)
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
        is_valid, message, df = self.data_handler.validate_file(file_path)
        if is_valid:
            self.error_label.setText("")
            self.next_button.setEnabled(True)
        if not is_valid:
            self.next_button.setEnabled(False) # in case user previously selected a valid file
            self.error_label.setText(message)
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"Selected file: {file_name}")
        return df

class CalendarPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Review Analyser") 
        font = title.font()
        font.setPointSize(50)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        calendars_layout = QHBoxLayout()

        font.setPointSize(20)
        font.setBold(False)

        start_layout = QVBoxLayout()
        start_label1 = QLabel("Start date:")
        start_label1.setFont(font)
        start_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        start_label2 = QLabel()
        start_label2.setFont(font)
        start_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        start_calendar = QCalendarWidget()

        start_layout.addWidget(start_label1)
        start_layout.addWidget(start_label2)
        start_layout.addWidget(start_calendar)

        end_layout = QVBoxLayout()
        end_label1 = QLabel("End date:")
        end_label1.setFont(font)
        end_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        end_label2 = QLabel()
        end_label2.setFont(font)
        end_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        end_calendar = QCalendarWidget()

        end_layout.addWidget(end_label1)
        end_layout.addWidget(end_label2)
        end_layout.addWidget(end_calendar)

        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(start_layout)
        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(end_layout)
        calendars_layout.addSpacing(20)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addLayout(calendars_layout)
        layout.addStretch()

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler

        self.setWindowTitle("Review Analyser")
        self.setMinimumSize(800,600)

        self.stack = QStackedWidget()
 
        upload_page = UploadPage(data_handler)
        calendar_page = CalendarPage()
        self.stack.addWidget(upload_page)
        self.stack.addWidget(calendar_page)

        self.setCentralWidget(self.stack)

        upload_page.next_requested.connect(self.go_next)
    
    def go_next(self):
        currentIndex = self.stack.currentIndex()
        self.stack.setCurrentIndex(currentIndex + 1)

