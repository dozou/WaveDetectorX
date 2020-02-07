from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import (QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.Qt import (QLineEdit, QListWidget, QListWidgetItem, QSlider)
from PyQt5.QtCore import Qt
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from decoder import S1TDecoder
from detector import Detector
from control_panel import ControlWidget
from item import Item


class WaveDetectorX(QWidget):
    def __init__(self, parent=None):
        super(WaveDetectorX, self).__init__(parent)
        self.setWindowTitle("WaveDetectorX")
        self.open_button = QPushButton("OPEN")
        self.save_button = QPushButton("SVAE")
        self.control_panel = ControlWidget()
        self.dirctory_textline = QLineEdit()
        self.list = QListWidget()
        self.adjust_slider = QSlider(Qt.Horizontal)

        self.open_button.clicked.connect(self.open_button_click)
        self.save_button.clicked.connect(self.save)
        self.control_panel.next_button.clicked.connect(self.next)
        self.control_panel.prev_button.clicked.connect(self.prev)
        self.adjust_slider.valueChanged.connect(self.__update)
        self.list.itemClicked.connect(self.__update)

        layout = QVBoxLayout()
        layout.addWidget(self.dirctory_textline)
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.list)
        layout.addWidget(self.control_panel)
        layout.addWidget(self.adjust_slider)

        self.setLayout(layout)
        self.path = pathlib.Path()
        self.datas = list()
        self.index = 0
        
    def open_button_click(self):
        self.list.clear()
        self.path = pathlib.Path(self.dirctory_textline.text())
        self.datas = [S1TDecoder(i) for i in self.path.glob("*.S1T")]
        if len(self.datas) > 0:
            for i in self.datas:
                self.list.addItem(Item(i))
            self.list.setCurrentRow(0)
            self.__plot(init=True)

    def next(self):
        self.index += 1
        self.list.setCurrentRow(self.index)
        self.__plot()

    def prev(self):
        if self.index > 0:
            self.index -= 1
        self.list.setCurrentRow(self.index)
        self.__plot()

    def __update(self):
        self.__plot()
    
    def __plot(self, init:int =  False):
        d = self.list.currentItem().data
        x = d.x()
        y = d.y()
        dtctr = Detector(x,y)
        idx = dtctr.detect(self.adjust_slider.value()/1000)

        if init:
            self.lines, = plt.plot(x, y)
            self.point, = plt.plot(x[idx], y[idx], marker=".")
            plt.pause(.1)
        else:
            self.lines.set_data(x, y)
            print("Motor: %s"%d.name)
            print("Detect index:%d"%idx)
            print("Detect position:%.2f"%x[idx])
            print("Detect load:%.3f"%(y[idx]*1000))
            print()
            self.point.set_data(x[idx], y[idx])
            
            plt.xlim(x.min(), x.max())
            plt.ylim(y.min(), y.max())
            plt.pause(.001)

    def save(self):
        t = pd.DataFrame()
        file_name = pathlib.Path(str(self.path) + "\\detect_data.xlsx")
        t.to_excel(file_name)


if __name__ == "__main__":
    app = QApplication([])
    a = WaveDetectorX()
    a.show()
    app.exec_()

