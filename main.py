import sys
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QGridLayout, QLabel, QPushButton, QVBoxLayout , QWidget,QFileDialog
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Test window name")

window.setFixedWidth(720)
window.setFixedHeight(720)

screenGeometry = QDesktopWidget().screenGeometry()
window.move(screenGeometry.width() // 2 - window.width() // 2,screenGeometry.height() // 2 - window.height() // 2)
window.setStyleSheet("background: #121212;")

grid=QGridLayout()
window.setLayout(grid)

logo = QPixmap("logo.png")
logo_label= QLabel()
logo_label.setPixmap(logo)
logo_label.setAlignment(QtCore.Qt.AlignCenter)
# logo_label.setStyleSheet("margin-top: 900px;")

test_button = QPushButton("Test")
test_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
test_button.setStyleSheet("*{border: 4px solid '#BC006C'; border-radius: 45px; font-size: 35px; color: 'white' ; padding: 25px 0;} *:hover{background:'#BC006C';}")


grid.addWidget(logo_label,0,0)
grid.addWidget(test_button,1,0)


window.show()

sys.exit(app.exec())