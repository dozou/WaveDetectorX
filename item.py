from PyQt5.Qt import (QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.Qt import (QLineEdit, QListWidget, QListWidgetItem, QSlider)
from PyQt5.QtCore import Qt
from decoder import S1TDecoder
from detector import Detector

class Item(QListWidgetItem):
    def __init__(self, data:S1TDecoder, parent=None):
        super(Item, self).__init__(data.name,parent)
        self.data = data