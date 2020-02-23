from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.Qt import (QPushButton,  QHBoxLayout, QDoubleValidator)
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
        self.scale = 10000
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(10)
        self.label = QLineEdit("%.4f" % self.value)

        self.slider.valueChanged.connect(self.__changed_slider)
        self.label.textChanged.connect(self.__changed_label)

        self.label.setValidator(QDoubleValidator())

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Detect sensitivity: "))
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.__changed_slider()

    def __changed_label(self):
        value = float(self.label.text()) * self.scale
        self.slider.setValue(value)

    def __changed_slider(self):
        self.value = self.slider.value() * (1/self.scale)
        self.label.setText("%.4f" % self.value)
