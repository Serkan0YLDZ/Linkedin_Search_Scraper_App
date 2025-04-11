from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt, QEasingCurve, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor
import sys
import os
from dotenv import load_dotenv, set_key
from pathlib import Path
from main import LinkedinScraper, ScrapingConfig, BrowserManager
import json

def apply_dark_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #353535;
        }
        QWidget {
            font-family: 'Segoe UI', Arial;
            font-size: 12px;
        }
        QLabel {
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
        }
        QLineEdit {
            padding: 8px;
            background-color: #252525;
            border: 2px solid #454545;
            border-radius: 5px;
            color: white;
        }
        QLineEdit:focus {
            border: 2px solid #0078d4;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #1084d8;
        }
        QPushButton:pressed {
            background-color: #006cbd;
        }
        QMessageBox {
            background-color: #353535;
        }
        QMessageBox QLabel {
            color: white;
        }
        QMessageBox QPushButton {
            min-width: 80px;
        }
        #themeButton {
            padding: 5px 10px;
            font-size: 11px;
            background-color: #454545;
        }
        #themeButton:hover {
            background-color: #555555;
        }
    """)

def apply_light_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 120, 212))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 212))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QWidget {
            font-family: 'Segoe UI', Arial;
            font-size: 12px;
        }
        QLabel {
            color: #000000;
            font-size: 13px;
            font-weight: bold;
        }
        QLineEdit {
            padding: 8px;
            background-color: #ffffff;
            border: 2px solid #cccccc;
            border-radius: 5px;
            color: black;
        }
        QLineEdit:focus {
            border: 2px solid #0078d4;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #1084d8;
        }
        QPushButton:pressed {
            background-color: #006cbd;
        }
        QMessageBox {
            background-color: #f0f0f0;
        }
        QMessageBox QLabel {
            color: black;
        }
        QMessageBox QPushButton {
            min-width: 80px;
        }
        #themeButton {
            padding: 5px 10px;
            font-size: 11px;
            background-color: #e0e0e0;
            color: black;
        }
        #themeButton:hover {
            background-color: #d0d0d0;
        }
    """)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel('LinkedIn Login')
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        email_layout = QVBoxLayout()
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter your LinkedIn email')
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)

        password_layout = QVBoxLayout()
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your LinkedIn password')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        self.next_button = QPushButton('Next')
        self.next_button.setFixedWidth(200)
        self.next_button.clicked.connect(self.save_credentials)

        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def save_credentials(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in both email and password fields.')
            return

        try:
            env_path = Path('.env')
            env_path.touch(exist_ok=True)

            load_dotenv()

            set_key('.env', 'LINKEDIN_EMAIL', email)
            set_key('.env', 'LINKEDIN_PASSWORD', password)

            load_dotenv(override=True)

            self.parent().setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save credentials: {str(e)}')

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel('LinkedIn Profile Search')
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        keyword_layout = QVBoxLayout()
        keyword_label = QLabel('Search Keyword:')
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText('Enter search keyword')
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)

        count_layout = QVBoxLayout()
        count_label = QLabel('Number of Profiles:')
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText('Enter number of profiles to scrape')
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_input)

        self.search_button = QPushButton('Search')
        self.search_button.setFixedWidth(200)
        self.search_button.clicked.connect(self.start_search)

        layout.addLayout(keyword_layout)
        layout.addLayout(count_layout)
        layout.addWidget(self.search_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def start_search(self):
        keyword = self.keyword_input.text().strip()
        count = self.count_input.text().strip()

        if not keyword or not count:
            QMessageBox.warning(self, 'Error', 'Please fill in both search fields.')
            return

        try:
            count_int = int(count)
            if count_int <= 0:
                raise ValueError('Profile count must be positive')

            config = ScrapingConfig(search_term=keyword, max_profiles=count_int)
            scraper = LinkedinScraper(config)
            scraper.initialize_browser()
            scraper.run_scraping()
            BrowserManager.close_driver(scraper.driver)
            QMessageBox.information(self, 'Process Completed', 'Process completed! You can view the data in the exports folder.')

        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid positive number for profile count.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to start search: {str(e)}')

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.check_existing_cookies()

    def check_existing_cookies(self):
        cookies_path = os.path.join('cookies', 'linkedin_cookies.json')
        if os.path.exists(cookies_path):
            reply = QMessageBox.question(
                self,
                'Previous Login Found',
                'You have previously logged in. Would you like to use the saved login?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                self.initUI()
                self.stacked_widget.setCurrentIndex(1)  
            else:
                try:
                    os.remove(cookies_path)
                except Exception as e:
                    QMessageBox.warning(self, 'Warning', f'Could not delete cookies file: {str(e)}')
                self.initUI()
        else:
            self.initUI()

    def initUI(self):
        self.setWindowTitle('LinkedIn Profile Scraper')
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(400, 300)

        self.theme_button = QPushButton('🌙 Dark' if not self.is_dark_theme else '☀️ Light')
        self.theme_button.setObjectName('themeButton')
        self.theme_button.setFixedSize(80, 30)
        self.theme_button.clicked.connect(self.toggle_theme)

        theme_widget = QWidget()
        theme_layout = QHBoxLayout(theme_widget)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_button)
        theme_layout.setContentsMargins(10, 10, 10, 0)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(theme_widget)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.setCentralWidget(main_widget)

        self.login_window = LoginWindow()
        self.search_window = SearchWindow()

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.search_window)

        self.center()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            apply_dark_theme(QApplication.instance())
            self.theme_button.setText('☀️ Light')
        else:
            apply_light_theme(QApplication.instance())
            self.theme_button.setText('🌙 Dark')

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    ex = MainApplication()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()