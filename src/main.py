from PyQt6.QtWidgets import QApplication

from data.review_data_handler import ReviewDataHandler
from ui.dashboard_ui import MainWindow 

def main():
    app = QApplication([]) 

    data_handler = ReviewDataHandler()
    window = MainWindow(data_handler)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()