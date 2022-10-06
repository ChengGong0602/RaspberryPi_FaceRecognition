from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QApplication,
    QHBoxLayout,
)

application = QApplication([])

mainWindow = QWidget()

mainWindow.setGeometry(0, 0, 350, 400)
mainWindow.setWindowTitle('Horizontal Layout')

horizontalLayout = QHBoxLayout()

for num in range(6):
    label = QLabel()
    pixmap = QPixmap('cat.jpg')
    label.setPixmap(pixmap)
    horizontalLayout.addWidget(label)

mainWindow.setLayout(horizontalLayout)
mainWindow.show()

application.exec()