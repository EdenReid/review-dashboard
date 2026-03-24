import os
from PyQt6.QtCore import Qt, pyqtSignal, QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QHeaderView, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QStackedWidget, 
                             QFileDialog, QHBoxLayout, QCalendarWidget, QTableWidget, QTableWidgetItem, QTabWidget)

class UploadPage(QWidget):

    next_requested = pyqtSignal()

    def __init__(self, data_handler):
        super().__init__()

        self.data_handler = data_handler
        layout = QVBoxLayout()

        #main title label
        title = QLabel("Review Analyser")
        font = title.font()
        font.setPointSize(50)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #instruction label
        label = QLabel("Load CSV file:")
        font.setPointSize(30)
        font.setBold(False)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #information label
        info_label = QLabel("Please note: CSV must include headers 'Date' and 'Review' and all dates should be in dd/mm/yyyy form.")
        font.setPointSize(10)
        info_label.setFont(font)
        info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #file browse button
        self.button = QPushButton("Browse files")
        font = self.button.font()
        font.setPointSize(15)
        self.button.setFont(font)
        self.button.setFixedSize(120, 50)
        self.button.clicked.connect(self.browse_files)

        #next button
        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.setFixedSize(100, 30)
        self.next_button.clicked.connect(self.next_requested.emit)

        #file path label
        self.file_label = QLabel()
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #arrange all widgets in the vertical layout with spacing
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
        # opens file dialog to let user select a CSV file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose CSV file", # window title
            "", # opens the last directory the user visited
            "CSV files (*.csv)" # only CSV files are selectable
        )
        if not file_path: # user cancels
            return 

        #validates the selected file using the data handler
        is_valid, message, df = self.data_handler.validate_file(file_path)
        if is_valid:
            #valid file: clear errors, enable next button, store data
            self.error_label.setText("")
            self.next_button.setEnabled(True)
            self.df = df
        else:
            #invalid file: disable next button, show error message
            self.next_button.setEnabled(False) # in case user previously selected a valid file
            self.error_label.setText(message)

        # displays file name
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"Selected file: {file_name}")

class CalendarPage(QWidget):
    # date selection page
    back_requested = pyqtSignal()  # signal for going back to previous page
    next_requested = pyqtSignal()  # signal for proceeding to next page

    def __init__(self, data_handler):        
        super().__init__()
        self.data_handler = data_handler

        layout = QVBoxLayout()  # Main vertical layout

        #title label
        title = QLabel("Review Analyser") 
        font = title.font()
        font.setPointSize(50)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        calendars_layout = QHBoxLayout()  # Horizontal layout for side-by-side calendars

        font.setPointSize(20)
        font.setBold(False)

        #start date section
        start_layout = QVBoxLayout()
        start_label1 = QLabel("Start date:")
        start_label1.setFont(font)
        start_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.start_label2 = QLabel()  # Will show selected start date
        self.start_label2.setFont(font)
        self.start_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.start_calendar = QCalendarWidget()
        self.start_calendar.selectionChanged.connect(self.on_date_changed)

        start_layout.addWidget(start_label1)
        start_layout.addWidget(self.start_label2)
        start_layout.addWidget(self.start_calendar)

        #end date section
        end_layout = QVBoxLayout()
        end_label1 = QLabel("End date:")
        end_label1.setFont(font)
        end_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.end_label2 = QLabel()  # Will show selected end date
        self.end_label2.setFont(font)
        self.end_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.end_calendar = QCalendarWidget()
        self.end_calendar.selectionChanged.connect(self.on_date_changed)

        end_layout.addWidget(end_label1)
        end_layout.addWidget(self.end_label2)
        end_layout.addWidget(self.end_calendar)

        self.error_label = QLabel()  #validation error messages
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)  # Initially disabled until valid dates selected
        self.next_button.setFixedSize(100, 30)
        self.next_button.clicked.connect(self.next_requested.emit)

        # Arrange calendar layouts side by side
        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(start_layout)
        calendars_layout.addSpacing(20)
        calendars_layout.addLayout(end_layout)
        calendars_layout.addSpacing(20)

        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(100, 30)
        self.back_button.clicked.connect(self.back_requested.emit)

        # Add all elements to main layout
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
        # set minimum and maximum selectable dates based on data range
        self.min_date = min_date
        self.max_date = max_date

        min_qdate = QDate(min_date.year, min_date.month, min_date.day)
        max_qdate = QDate(max_date.year, max_date.month, max_date.day)

        # set start calendar bounds and initial selection
        self.start_calendar.setMinimumDate(min_qdate)
        self.start_calendar.setMaximumDate(max_qdate)
        self.start_calendar.setSelectedDate(min_qdate)

        # set end calendar bounds and initial selection
        self.end_calendar.setMinimumDate(min_qdate)
        self.end_calendar.setMaximumDate(max_qdate)
        self.end_calendar.setSelectedDate(max_qdate)

    def update_start_label(self):
        # update start date display label with formatted selected date
        qdate = self.start_calendar.selectedDate()
        self.start_label2.setText(qdate.toString("dd MMMM yyyy"))

    def update_end_label(self):
        # update end date display label with formatted selected date
        qdate = self.end_calendar.selectedDate()
        self.end_label2.setText(qdate.toString("dd MMMM yyyy"))

    def capture_selected_dates(self):
        # store current calendar selections as Python date objects
        self.start_date = self.start_calendar.selectedDate().toPyDate()
        self.end_date = self.end_calendar.selectedDate().toPyDate()

    def validate_date_range(self):
        # check if start date is before end date, update UI accordingly
        if self.start_date > self.end_date:
            self.error_label.setText("Start date cannot be after end date")
            self.next_button.setEnabled(False)
        else:
            self.error_label.setText("")
            self.next_button.setEnabled(True)

    def on_date_changed(self):
        # updates elements when calendar selection changes
        self.capture_selected_dates()
        self.validate_date_range()
        self.update_start_label()
        self.update_end_label()

class ReviewPage(QWidget):

    back_requested = pyqtSignal()  # signal for going back to date selection

    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.init_ui()

    def init_ui(self):
        #initialises page with tabs for two different analysis windows
       main_layout = QVBoxLayout()

       self.tabs = QTabWidget()
       self.reviews_tab = QWidget()  
       self.sentiment_tab = QWidget()

       self.tabs.addTab(self.reviews_tab, "Reviews")
       self.tabs.addTab(self.sentiment_tab, "Sentiment analysis")

       self.init_reviews_tab()
       self.init_sentiment_tab()
       main_layout.addWidget(self.tabs)
       
       #back button
       back_button = QPushButton("Back")
       back_button.setFixedSize(100, 30)
       back_button.clicked.connect(self.back_requested.emit)
       main_layout.addWidget(back_button)

       self.setLayout(main_layout)
    
    def init_reviews_tab(self):
        #set up reviews tab
        layout = QHBoxLayout()

        #main reviews table
        self.review_table = QTableWidget()
        self.review_table.setColumnCount(3)
        self.review_table.setHorizontalHeaderLabels(["Date","Review","Sentiment score"]) 
        self.review_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) #read-only
        self.review_table.setSortingEnabled(False)

        header = self.review_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  #date column fits content
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  #review column stretches
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  #score column fits content

        #enables word wrapping for long reviews
        self.review_table.setWordWrap(True)
        self.review_table.setTextElideMode(Qt.TextElideMode.ElideNone)

        self.review_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents  #row height adjusts to content
        )

        #keywords panel
        keywords_layout = QVBoxLayout()
        
        keywords_label = QLabel("Most common keywords")
        font = keywords_label.font()
        font.setPointSize(20)
        font.setBold(True)
        keywords_label.setFont(font)
        keywords_layout.addWidget(keywords_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        #configure keywords table
        self.keywords_table = QTableWidget()
        self.keywords_table.setColumnCount(2)
        self.keywords_table.setHorizontalHeaderLabels(["Keyword","Frequency"])
        self.keywords_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.keywords_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.keywords_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.keywords_table.setSortingEnabled(False)
        keywords_layout.addWidget(self.keywords_table)

        layout.addWidget(self.review_table)
        layout.addLayout(keywords_layout)

        self.reviews_tab.setLayout(layout)

    def populate_table(self, df):
        # fill reviews table with review data 
        if df is None:
            return 
        
        self.review_table.setRowCount(0)  # Clear existing rows

        self.review_table.setRowCount(len(df))  # Set row count to match data

        # Populate each row with review data
        for row_index, (_, row) in enumerate(df.iterrows()):
            date_str = row["Date"].strftime("%d/%m/%Y")  # Format date for display
            review_text = row["Review"]
            sentiment_score = row["Sentiment"]

            self.review_table.setItem(row_index, 0, QTableWidgetItem(date_str))
            self.review_table.setItem(row_index, 1, QTableWidgetItem(review_text))
            self.review_table.setItem(row_index, 2, QTableWidgetItem(str(sentiment_score)))

        self.review_table.resizeRowsToContents()  # adjust row heights to fit content

    def populate_keywords_table(self, keywords):
        # fill keywords table
        if keywords is None:
            return
        
        self.keywords_table.setRowCount(0)  # Clear existing rows
        self.keywords_table.setRowCount(len(keywords))  # Set row count

        # Populate each row with keyword data
        for row_index, (keyword, freq) in enumerate(keywords):

            keyword_item = QTableWidgetItem(keyword)
            self.keywords_table.setItem(row_index, 0, keyword_item)
            keyword_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            
            frequency_item = QTableWidgetItem(str(freq))
            self.keywords_table.setItem(row_index, 1, frequency_item)
            frequency_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def init_sentiment_tab(self):

        # sentiment analysis tab with chart and summary panels

        self.figure = Figure()  # Matplotlib figure for the chart
        self.canvas = FigureCanvas(self.figure)  # Qt canvas to display matplotlib figure
        self.ax = self.figure.add_subplot(111)  # Single subplot for the chart

        main_layout = QHBoxLayout()  # Side-by-side layout

        # Left panel for average score 
        self.left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Right panel for the chart
        self.right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas)

        self.left_panel.setLayout(left_layout)
        self.right_panel.setLayout(right_layout)

        main_layout.addWidget(self.left_panel, 1)  # Left panel gets 1 part
        main_layout.addWidget(self.right_panel, 2)  # Right panel gets 2 parts (wider)

        self.sentiment_tab.setLayout(main_layout)

        self.init_average_sentiment_panel(left_layout)  # Add summary panel to left side

    def init_average_sentiment_panel(self, layout):
        # left panel showing average sentiment score and classification
        title = QLabel("Average sentiment score:")
        font = title.font()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font) 
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.avg_score_label = QLabel("0.0")  # Will show the calculated average
        score_font = self.avg_score_label.font()
        score_font.setPointSize(40)
        score_font.setBold(True)    
        self.avg_score_label.setFont(score_font)
        self.avg_score_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)    

        self.classification_label = QLabel("Neutral")  # Will show Positive/Negative/Neutral
        classification_font = self.classification_label.font()  
        classification_font.setPointSize(20)
        classification_font.setBold(True)
        self.classification_label.setFont(classification_font)
        self.classification_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        description = QLabel("Sentiment is scored from 0 to 5 inclusive and \nrecorded to the nearest 0.1.")
        description_font = description.font()
        description_font.setPointSize(10)
        description.setFont(description_font)

        description.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add all elements to the layout with spacing
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.avg_score_label)
        layout.addWidget(self.classification_label)
        layout.addSpacing(10)
        layout.addWidget(description)
        layout.addStretch()

    def update_average_sentiment(self, average_score, classification):
        # Update the average sentiment display with new values and color coding
        self.avg_score_label.setText(str(average_score))
        self.classification_label.setText(classification)

        # colour code the classification label
        if classification == "Positive":
            self.classification_label.setStyleSheet("color: green;")
        elif classification == "Negative":
            self.classification_label.setStyleSheet("color: red;")
        else:
            self.classification_label.setStyleSheet("color: orange;")
 
    def plot_sentiment_graph(self, daily_avg):
        #sentiment graph

        if daily_avg is None:
            return  

        self.ax.clear()  # Clear previous plot

        # smoothed trend line using 14-day rolling average
        smoothed = daily_avg.rolling(window=14).mean()

        # raw data as faint line and smoothed data as bold line
        self.ax.plot(daily_avg.index, daily_avg.values, alpha=0.3, label="Raw data")
        self.ax.plot(smoothed.index, smoothed.values, linewidth=3, label="Smoothed data")

        # chart labels and formatting
        self.ax.set_title("Daily Average Sentiment Over Time")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Sentiment Score")

        self.ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels

        self.ax.legend()  # show legend (explains two different lines)

        self.figure.tight_layout()  # Adjust layout to prevent clipping

        self.canvas.draw()

class MainWindow(QMainWindow):
    # main application window

    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        from analysis.review_analyser import ReviewAnalyser
        self.analyser = ReviewAnalyser()

        # configure main window properties
        self.setWindowTitle("Review Analyser")
        self.setMinimumSize(800,600)

        self.stack = QStackedWidget()  # widget stack for page navigation
 
        # Create all page widgets
        self.upload_page = UploadPage(data_handler)
        self.calendar_page = CalendarPage(data_handler)
        self.review_page = ReviewPage(data_handler)

        # Add pages to the stack
        self.stack.addWidget(self.upload_page)
        self.stack.addWidget(self.calendar_page)
        self.stack.addWidget(self.review_page)

        self.setCentralWidget(self.stack)

        # Connect navigation signals
        self.upload_page.next_requested.connect(self.go_next)
        self.calendar_page.back_requested.connect(self.go_back)
        self.calendar_page.next_requested.connect(self.go_next)
        self.review_page.back_requested.connect(self.go_back)

    
    def go_next(self):

        currentIndex = self.stack.currentIndex()

        if currentIndex == 0:  # from upload to calendar page
            min_date, max_date = self.data_handler.find_min_max_dates(self.data_handler.data)
            self.calendar_page.set_date_bounds(min_date, max_date)  # set calendar limits

        elif currentIndex == 1:  # from calendar to review page
            # get selected date range and filter data
            start_date = self.calendar_page.start_date
            end_date = self.calendar_page.end_date

            df = self.data_handler.get_sorted_reviews(start_date, end_date)
            df = self.analyser.get_sentiment_scores(df)  # add sentiment analysis
            keywords = self.analyser.get_most_common_words(df)  #extract keywords

            # Update review page
            self.review_page.populate_table(df)
            self.review_page.populate_keywords_table(keywords)

            # calculate and display sentiment summary
            avg_score, classification = self.analyser.get_average_sentiment(df)
            self.review_page.update_average_sentiment(avg_score, classification)
            daily_avg = self.analyser.get_daily_average_sentiments(df, start_date, end_date)
            self.review_page.plot_sentiment_graph(daily_avg)

        self.stack.setCurrentIndex(currentIndex + 1)  # advance to next page

    def go_back(self):
        # backward navigation to previous page
        currentIndex = self.stack.currentIndex()
        self.stack.setCurrentIndex(currentIndex - 1)

