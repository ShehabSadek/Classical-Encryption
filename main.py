import sys
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QHBoxLayout, QLabel, QPushButton, QVBoxLayout , QWidget,QFileDialog,QTextEdit
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore
from network_sec import *

class UpperPart(QWidget):
    def __init__(self, parent=None):
        super(UpperPart, self).__init__(parent)
        labels_layout = QVBoxLayout()
        upper_layout = QHBoxLayout()
        labels=[]
        text_edits=[]
        for label_text in ["Plain Text", "Key", "Cipher Text"]:
            label = create_label(label_text)
            text_edit = create_textArea(label_text)
            labels.append(label)
            text_edits.append(text_edit)

            labels_layout.addWidget(label)
            labels_layout.addWidget(text_edit)

        text_edits[-1].setReadOnly(True)

        self.setLayout(labels_layout)

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
        layout = QHBoxLayout()

        for i in ["Ceaser","Playfair","Hill","Vigenere","Vernam"]:
            button = create_button(i)
            button.clicked.connect(self.on_button_clicked)

            if i == "Vigenere":
                button=SplitButton("Vigenere-Repeat", "Vigenere-Auto")
                button.main_button.clicked.connect(self.on_button_clicked)
                button.secondary_button.clicked.connect(self.on_button_clicked)
            layout.addWidget(button)


        self.setLayout(layout)

    def on_button_clicked(self):
        sender_button = self.sender()
        # self.upper_part.findChild(QTextEdit,"Key").setText(sender_button.text())
        tag = sender_button.text()
        text=self.upper_part.findChild(QTextEdit,"Plain Text").toPlainText()
        key_text = self.upper_part.findChild(QTextEdit, "Key").toPlainText()
        if not text or not key_text:
            self.upper_part.findChild(QTextEdit, "Cipher Text").setText("Both Plain Text and Key must be provided.")
            return
        if tag=="Ceaser":
            try:
                key = int(key_text)
            except ValueError:
                key = None
            if key is not None:
                self.upper_part.findChild(QTextEdit,"Cipher Text").setText(ceaser(text,int(key)))
            else:
                self.upper_part.findChild(QTextEdit,"Cipher Text").setText("Enter a valid shift number!")
        if tag=="Playfair":
            self.upper_part.findChild(QTextEdit,"Cipher Text").setText(playfair(key_text,text))

        if tag=="Hill":
            self.upper_part.findChild(QTextEdit,"Cipher Text").setText(hill(text))
            self.upper_part.findChild(QTextEdit,"Key").setText("Key matrix is predefined.")

        if tag=="Vigenere-Repeat":
            self.upper_part.findChild(QTextEdit,"Cipher Text").setText(vigenere(key_text,text,False))
        if tag=="Vigenere-Auto":
            self.upper_part.findChild(QTextEdit,"Cipher Text").setText(vigenere(key_text,text,True))
        
        if tag=="Vernam":
            self.upper_part.findChild(QTextEdit,"Cipher Text").setText(vernam(key_text,text))
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("./assets/logo.png"))

        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        with open(css, "r") as style_file:
            self.setStyleSheet(style_file.read())
        self.setFixedSize(900, 550)
        self.setGeometry(x, y,900, 550)
        background_label = QLabel(self)
        pixmap = QPixmap("./assets/cyber.jpg")
        background_label.setPixmap(pixmap)
        background_label.resize(self.size())
        background_label.lower()
        self.setWindowTitle("Network Security Project")

        upper_part = UpperPart(self)
        lower_part = LowerPart(upper_part,self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(upper_part)
        main_layout.addWidget(lower_part)
        self.setLayout(main_layout)

def create_button(encryption):
    button = QPushButton(encryption)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedHeight(90)

    button.setObjectName("encrypt")
    return button

def create_label(text):
    label = QLabel(text)
    return label

def create_textArea(name):
    text_edit = QTextEdit()
    text_edit.setFontPointSize(30)
    text_edit.setObjectName(name)
    return text_edit

if __name__ == "__main__":
    app = QApplication(sys.argv)
    css="./main.css"
    with open(css, "r") as style_file:
        app.setStyleSheet(style_file.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
