import sys
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QHBoxLayout, QLabel, QPushButton, QVBoxLayout , QWidget,QFileDialog,QTextEdit
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore

widgets = {"logo":[],
            "button":[],
            "score":[],
            "quest":[],
            "type1":[],
            "type2":[],
            "type3":[],
            "type4":[]
           }

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

    def update_text(self, new_text):
        self.label.setText(new_text)

class LowerPart(QWidget):
    def __init__(self, upper_part, parent=None):
        super(LowerPart, self).__init__(parent)
        self.upper_part = upper_part
        layout = QHBoxLayout()

        for i in ["Ceaser","Playfair","Hill","Vigenere","Vernam"]:
            button = create_button(i)
            button.clicked.connect(self.on_button_clicked)
            layout.addWidget(button)

        self.setLayout(layout)

    def on_button_clicked(self):
        sender_button = self.sender()
        new_text = f"Button {sender_button.text()} was pressed!"
        self.upper_part.update_text(new_text)
        
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

def main_frame():
    logo = QPixmap("logo.png")
    logo_label= QLabel()
    logo_label.setPixmap(logo)
    logo_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["logo"].append(logo_label)
    # logo_label.setStyleSheet("margin-top: 900px;")

    test_button = QPushButton("Test")
    test_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    test_button.setStyleSheet("*{border: 4px solid '#BC006C'; border-radius: 45px; font-size: 35px; color: 'white' ; padding: 25px 0;} *:hover{background:'#BC006C';}")
    widgets["button"].append(test_button)

    #grid.addWidget(widgets["logo"][-1],0,0)
    #grid.addWidget(widgets["button"][-1],1,0)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    css="./main.css"
    with open(css, "r") as style_file:
        app.setStyleSheet(style_file.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
