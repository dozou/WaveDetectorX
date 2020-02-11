from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
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


class SlideBar(QWidget):
    def __init__(self, parent=None):
        super(SlideBar, self).__init__(parent)
        self.value = 0.0
        self.slider = QSlider(Qt.Horizontal)
        self.label = QLabel("%.4f" % self.value)

        self.slider.valueChanged.connect(self.__update)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Detect sensitivity: "))
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def __update(self):
        self.value = self.slider.value()/1000
        self.label.setText("%.3f" % self.value)
