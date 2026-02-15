#importing libraries and modules
import os
import sys
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtWidgets import QHeaderView, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFileDialog, QHBoxLayout, QCalendarWidget, QTableWidget, QTableWidgetItem, QTabWidget
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

        info_label = QLabel("Please note: CSV must include headers 'Date' and 'Review' and all dates should be in dd/mm/yyyy form.")
        font.setPointSize(10)
        info_label.setFont(font)
        info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        layout.addWidget(info_label)
        layout.addStretch()
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
            self.df = df
        if not is_valid:
            self.next_button.setEnabled(False) # in case user previously selected a valid file
            self.error_label.setText(message)
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"Selected file: {file_name}")

class CalendarPage(QWidget):
    
    back_requested = pyqtSignal()
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

        calendars_layout = QHBoxLayout()

        font.setPointSize(20)
        font.setBold(False)

        start_layout = QVBoxLayout()
        start_label1 = QLabel("Start date:")
        start_label1.setFont(font)
        start_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.start_label2 = QLabel()
        self.start_label2.setFont(font)
        self.start_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.start_calendar = QCalendarWidget()
        self.start_calendar.selectionChanged.connect(self.on_date_changed)

        start_layout.addWidget(start_label1)
        start_layout.addWidget(self.start_label2)
        start_layout.addWidget(self.start_calendar)

        end_layout = QVBoxLayout()
        end_label1 = QLabel("End date:")
        end_label1.setFont(font)
        end_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.end_label2 = QLabel()
        self.end_label2.setFont(font)
        self.end_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.end_calendar = QCalendarWidget()
        self.end_calendar.selectionChanged.connect(self.on_date_changed)

        end_layout.addWidget(end_label1)
        end_layout.addWidget(self.end_label2)
        end_layout.addWidget(self.end_calendar)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.setFixedSize(100, 30)
        self.next_button.clicked.connect(self.next_requested.emit)

        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(start_layout)
        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(end_layout)
        calendars_layout.addSpacing(20)

        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(100, 30)
        self.back_button.clicked.connect(self.back_requested.emit)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addLayout(calendars_layout)
        layout.addStretch()
        layout.addWidget(self.error_label)
        layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.back_button)
        
        self.on_date_changed()

        self.setLayout(layout)

    def set_date_bounds(self, min_date, max_date):
        self.min_date = min_date
        self.max_date = max_date

        min_qdate = QDate(min_date.year, min_date.month, min_date.day)
        max_qdate = QDate(max_date.year, max_date.month, max_date.day)

        self.start_calendar.setMinimumDate(min_qdate)
        self.start_calendar.setMaximumDate(max_qdate)
        self.start_calendar.setSelectedDate(min_qdate)

        self.end_calendar.setMinimumDate(min_qdate)
        self.end_calendar.setMaximumDate(max_qdate) 
        self.end_calendar.setSelectedDate(max_qdate)

    def update_start_label(self):
        qdate = self.start_calendar.selectedDate()
        self.start_label2.setText(qdate.toString("dd MMMM yyyy"))

    def update_end_label(self):
        qdate = self.end_calendar.selectedDate()
        self.end_label2.setText(qdate.toString("dd MMMM yyyy"))

    def capture_selected_dates(self):
        self.start_date = self.start_calendar.selectedDate().toPyDate()
        self.end_date = self.end_calendar.selectedDate().toPyDate()

    def validate_date_range(self):
        if self.start_date > self.end_date:
            self.error_label.setText("Start date cannot be after end date")
            self.next_button.setEnabled(False)
        elif self.start_date <= self.end_date:
            self.error_label.setText("")
            self.next_button.setEnabled(True)

    def on_date_changed(self):
        self.capture_selected_dates()
        self.validate_date_range()
        self.update_start_label()
        self.update_end_label()

class ReviewPage(QWidget):

    back_requested = pyqtSignal()

    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.init_ui()

    def init_ui(self):
       main_layout = QVBoxLayout()

       self.tabs = QTabWidget()
       self.reviews_tab = QWidget()
       self.sentiment_tab = QWidget()

       self.tabs.addTab(self.reviews_tab, "Reviews")
       self.tabs.addTab(self.sentiment_tab, "Sentiment analysis") 

       self.init_reviews_tab()
       main_layout.addWidget(self.tabs)
       
       back_button = QPushButton("Back")
       back_button.setFixedSize(100, 30)
       back_button.clicked.connect(self.back_requested.emit)
       main_layout.addWidget(back_button)

       self.setLayout(main_layout)
    
    def init_reviews_tab(self):
        layout = QHBoxLayout()

        self.review_table = QTableWidget()
        self.review_table.setColumnCount(3)
        self.review_table.setHorizontalHeaderLabels(["Date","Review","Sentiment score"]) 
        self.review_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.review_table.setSortingEnabled(False)

        header = self.review_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.review_table.setWordWrap(True)
        self.review_table.setTextElideMode(Qt.TextElideMode.ElideNone)

        self.review_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        keywords_layout = QVBoxLayout()
        
        keywords_label = QLabel("Most common keywords")
        font = keywords_label.font()
        font.setPointSize(20)
        font.setBold(True)
        keywords_label.setFont(font)
        keywords_layout.addWidget(keywords_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.keywords_table = QTableWidget()
        self.keywords_table.setColumnCount(3)
        self.keywords_table.setHorizontalHeaderLabels(["Rank","Keyword","Frequency"])
        self.keywords_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.keywords_table.setSortingEnabled(False)
        keywords_layout.addWidget(self.keywords_table)

        layout.addWidget(self.review_table)
        layout.addLayout(keywords_layout)

        self.reviews_tab.setLayout(layout)

    def populate_table(self, df):
        
        if df is None:
            return 
        
        self.review_table.setRowCount(0) #clear existing rows

        self.review_table.setRowCount(len(df))

        for row_index, (_, row) in enumerate(df.iterrows()):
            date_str = row["Date"].strftime("%d/%m/%Y") #format date
            review_text = row["Review"]

            self.review_table.setItem(row_index, 0, QTableWidgetItem(date_str))
            self.review_table.setItem(row_index, 1, QTableWidgetItem(review_text))
            self.review_table.setItem(row_index, 2, QTableWidgetItem("")) #sentiment score row empty for now

        self.review_table.resizeRowsToContents()

class MainWindow(QMainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler

        self.setWindowTitle("Review Analyser")
        self.setMinimumSize(800,600)

        self.stack = QStackedWidget()
 
        self.upload_page = UploadPage(data_handler)
        self.calendar_page = CalendarPage(data_handler)
        self.review_page = ReviewPage(data_handler)

        self.stack.addWidget(self.upload_page)
        self.stack.addWidget(self.calendar_page)
        self.stack.addWidget(self.review_page)

        self.setCentralWidget(self.stack)

        self.upload_page.next_requested.connect(self.go_next)
        self.calendar_page.back_requested.connect(self.go_back)
        self.calendar_page.next_requested.connect(self.go_next)
        self.review_page.back_requested.connect(self.go_back)
    
    def go_next(self):
        currentIndex = self.stack.currentIndex()
        if currentIndex == 0:
            min_date, max_date = self.data_handler.find_min_max_dates(self.data_handler.data)
            self.calendar_page.set_date_bounds(min_date, max_date)

        if currentIndex == 1:
            start_date = self.calendar_page.start_date
            end_date = self.calendar_page.end_date
            sorted_df = self.data_handler.get_sorted_reviews(start_date, end_date)
            self.review_page.populate_table(sorted_df)

        self.stack.setCurrentIndex(currentIndex + 1)

    def go_back(self):
        currentIndex = self.stack.currentIndex()
        self.stack.setCurrentIndex(currentIndex - 1)

