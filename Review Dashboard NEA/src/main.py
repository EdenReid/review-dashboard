from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Review Analyser")
        layout = QVBoxLayout()

        self.label = QLabel("Review Analyser") 
        self.button = QPushButton("Browse files")
        self.button.clicked.connect(self.button_clicked)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)
        self.setMinimumSize(400,300)

    def button_clicked(self):
        self.label.setText("Button clicked")
        self.button.setText("Thanks for clicking")

app = QApplication([])

window = MainWindow()
window.show()

app.exec()