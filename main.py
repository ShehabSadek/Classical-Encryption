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
    button.setStyleSheet("font-family: 'Times New Roman'; font-size: 32;")
    button.setObjectName("encrypt")
    return button

def create_label(text):
    label = QLabel(text)
    label.setStyleSheet("color: white; font-family: 'Times New Roman'; font-size: 32;")  
    return label

def create_text_area(name):
    text_edit = QTextEdit()
    text_edit.setFontPointSize(22)  
    text_edit.setStyleSheet("color: white; font-family: 'Times New Roman';")  
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
        layout = QHBoxLayout()  # Change to QHBoxLayout
        layout.addWidget(self.main_button)
        layout.addWidget(self.secondary_button)
        self.setLayout(layout)

class LowerPart(QWidget):
    def __init__(self, upper_part, parent=None):
        super(LowerPart, self).__init__(parent)
        self.upper_part = upper_part
        self.setup_layout()

    def setup_layout(self):
        layout = QHBoxLayout()  # Change to QHBoxLayout
        encryption_types = ["Ceaser", "Playfair", "Hill", "Vigenere", "Vernam"]
        for encryption in encryption_types:
            if encryption == "Vigenere":
                split_button = SplitButton("Vigenere-Repeat", "Vigenere-Auto")
                split_button.main_button.clicked.connect(self.on_button_clicked)
                split_button.secondary_button.clicked.connect(self.on_button_clicked)
                layout.addWidget(split_button)
            else:
                button = create_button(encryption)
                button.clicked.connect(self.on_button_clicked)
                layout.addWidget(button)

        self.setLayout(layout)

    def on_button_clicked(self):
        sender_button = self.sender()
        tag = sender_button.text()
        text = self.upper_part.findChild(QTextEdit, "Plain Text").toPlainText()
        key_text = self.upper_part.findChild(QTextEdit, "Key").toPlainText()

        try:
            with open('plain_text.txt', 'a') as plain_text_file:
                plain_text_file.write(text + '\n')
        except Exception as e:
            print(f"Error writing to plain_text.txt: {e}")

        if not text or not key_text:
            result = "Both Plain Text and Key must be provided."
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
            write_to_file(result)
            return

        result = ""
        if tag == "Ceaser":
            try:
                key = int(key_text)
            except ValueError:
                key = None
            if key is not None:
                result = ceaser(text, int(key))
                self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
        elif tag == "Playfair":
            result = playfair(key_text, text)
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
        elif tag == "Hill":
            result = hill(text)
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
        elif tag == "Vigenere-Repeat":
            result = vigenere(key_text, text, False)
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
        elif tag == "Vigenere-Auto":
            result = vigenere(key_text, text, True)
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)
        elif tag == "Vernam":
            result = vernam(key_text, text)
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText(result)

        try:
            with open('encryption_results.txt', 'a') as file:
                file.write(result + '\n')
        except Exception as e:
            print(f"Error writing to encryption_results.txt: {e}")



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
