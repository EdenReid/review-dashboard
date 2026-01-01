#importing libraries and modules
import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFileDialog

class UploadPage(QWidget):
    
    next_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

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

        self.button = QPushButton("Browse files")
        font = self.button.font()
        font.setPointSize(15)
        self.button.setFont(font)
        self.button.setFixedSize(120,50)
        self.button.clicked.connect(self.browse_files)

        self.next_button = QPushButton("Next") #next button (disabled for now)
        self.next_button.setEnabled(False)
        self.next_button.setFixedSize(100,30)

        self.next_button.clicked.connect(self.next_requested.emit)

        layout.addStretch() # vertical stretches are used to adjust the position of text within the page
        layout.addWidget(self.title)
        layout.addStretch() 
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.next_button)
        layout.addStretch()
        layout.setAlignment(self.next_button, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        self.setLayout(layout)
    
    def browse_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose CSV file", # window title 
            "", # starting directory (last directory the user visited)
            "CSV files (*.csv)" # only CSV files are visible and selectable
        )
        if not file_path: # user cancels
            return 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Review Analyser")
        self.setMinimumSize(800,600)

        self.stack = QStackedWidget()

        self.upload_page = UploadPage()
        self.stack.addWidget(self.upload_page)

        self.setCentralWidget(self.stack)
        self.upload_page.next_requested.connect(self.go_next)
    
    def go_next(self):
        pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()