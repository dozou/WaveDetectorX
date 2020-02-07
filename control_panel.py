
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import (QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.Qt import (QLineEdit, QListWidget, QListWidgetItem, QSlider)

class ControlWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Prev")

        layout = QHBoxLayout()
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        self.setLayout(layout)
