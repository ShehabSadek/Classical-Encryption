import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QDesktopWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    QWidget, QTextEdit
)
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5 import QtCore
from network_sec import *

def create_button(encryption):
    button = QPushButton(encryption)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedHeight(90)
    button.setObjectName("encrypt")
    return button

def create_label(text):
    label = QLabel(text)
    return label

def create_text_area(name):
    text_edit = QTextEdit()
    text_edit.setFontPointSize(30)
    text_edit.setObjectName(name)
    return text_edit

class UpperPart(QWidget):
    def __init__(self, parent=None):
        super(UpperPart, self).__init__(parent)
        self.labels_layout = QVBoxLayout()
        self.setup_labels()
        self.setLayout(self.labels_layout)

    def setup_labels(self):
        labels = []
        text_edits = []
        for label_text in ["Plain Text", "Key", "Cipher Text"]:
            label = create_label(label_text)
            text_edit = create_text_area(label_text)
            labels.append(label)
            text_edits.append(text_edit)

            self.labels_layout.addWidget(label)
            self.labels_layout.addWidget(text_edit)

        text_edits[-1].setReadOnly(True)

class SplitButton(QWidget):
    def __init__(self, main_text, secondary_text, parent=None):
        super(SplitButton, self).__init__(parent)
        self.main_button = create_button(main_text)
        self.secondary_button = create_button(secondary_text)
        layout = QVBoxLayout()
        layout.addWidget(self.main_button)
        layout.addWidget(self.secondary_button)
        self.setLayout(layout)

class LowerPart(QWidget):
    def __init__(self, upper_part, parent=None):
        super(LowerPart, self).__init__(parent)
        self.upper_part = upper_part
        self.setup_layout()

    def setup_layout(self):
        layout = QHBoxLayout()
        encryption_types = ["Ceaser", "Playfair", "Hill", "Vigenere", "Vernam"]
        for encryption in encryption_types:
            button = create_button(encryption)
            button.clicked.connect(self.on_button_clicked)

            if encryption == "Vigenere":
                button = SplitButton("Vigenere-Repeat", "Vigenere-Auto")
                button.main_button.clicked.connect(self.on_button_clicked)
                button.secondary_button.clicked.connect(self.on_button_clicked)
            layout.addWidget(button)
        self.setLayout(layout)

    def on_button_clicked(self):
        sender_button = self.sender()
        tag = sender_button.text()
        text = self.upper_part.findChild(QTextEdit, "Plain Text").toPlainText()
        key_text = self.upper_part.findChild(QTextEdit, "Key").toPlainText()

        if not text or not key_text:
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText("Both Plain Text and Key must be provided.")
            return

        if tag == "Ceaser":
            try:
                key = int(key_text)
            except ValueError:
                key = None
            if key is not None:
                self.upper_part.findChild(QTextEdit, "Cipher Text").setText(ceaser(text, int(key)))
            else:
                self.upper_part.findChild(QTextEdit, "Cipher Text").setText("Enter a valid shift number.")
        elif tag == "Playfair":
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(playfair(key_text, text))
        elif tag == "Hill":
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(hill(text))
            self.upper_part.findChild(QTextEdit, "Key").setText("Key matrix is predefined.")
        elif tag == "Vigenere-Repeat":
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(vigenere(key_text, text, False))
        elif tag == "Vigenere-Auto":
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(vigenere(key_text, text, True))
        elif tag == "Vernam":
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(vernam(key_text, text))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        if getattr(sys, 'frozen', False):
            script_directory = sys._MEIPASS
        else:
            script_directory = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(script_directory, 'assets', 'cyber.jpg')
        pixmap = QPixmap(img_dir)

        self.setWindowIcon(QIcon(os.path.join(script_directory, 'assets', 'logo.png')))
        self.setup_window_geometry()

        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.resize(self.size())
        background_label.lower()

        self.setWindowTitle("Network Security Project")

        upper_part = UpperPart(self)
        lower_part = LowerPart(upper_part, self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(upper_part)
        main_layout.addWidget(lower_part)
        self.setLayout(main_layout)

    def setup_window_geometry(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, 900, 550)
        self.setFixedSize(900, 550)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        script_directory = sys._MEIPASS
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(script_directory, 'assets', 'main.css')
    with open(css_path, "r") as style_file:
        app.setStyleSheet(style_file.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
