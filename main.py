from typing import List, Any

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.Qt import (QPushButton, QVBoxLayout, QListWidget, QSlider, QMessageBox)
from PyQt5.QtCore import Qt
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from decoder import S1TDecoder
from detector import Detector
from control_panel import ControlWidget, SlideBar
from item import Item
from line_edit import LineEdit


class WaveDetectorX(QWidget):

    def __init__(self, parent=None):
        super(WaveDetectorX, self).__init__(parent)
        self.setWindowTitle("WaveDetectorX")
        self.open_button = QPushButton("OPEN")
        self.save_button = QPushButton("SVAE")
        self.control_panel = ControlWidget()
        self.directory_text_line = LineEdit()
        self.list = QListWidget()
        self.adjust_slider = SlideBar()

        self.open_button.clicked.connect(self.open_button_click)
        self.save_button.clicked.connect(self.save)
        self.control_panel.next_button.clicked.connect(self.next)
        self.control_panel.prev_button.clicked.connect(self.prev)
        self.adjust_slider.slider.valueChanged.connect(self.__update)
        self.list.itemClicked.connect(self.__update)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("↓Drag and drop folder onto following."))
        layout.addWidget(self.directory_text_line)
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.list)
        layout.addWidget(self.control_panel)
        layout.addWidget(self.adjust_slider)
        self.setLayout(layout)

        self.setAcceptDrops(True)

        self.path = pathlib.Path()
        self.data = list()
        self.index = 0

    def open_button_click(self):
        self.list.clear()
        self.path = pathlib.Path(self.directory_text_line.text())
        path = list(self.path.glob("*.S1T"))
        path.sort()
        self.data = [S1TDecoder(i) for i in path]
        print("Open...")
        print("Find files: %s" % str(self.data))
        if len(self.data) > 0:
            for i in self.data:
                self.list.addItem(Item(i))
            self.list.setCurrentRow(0)
            self.__plot(init=True)
            print("QlistWidget count: %d" % self.list.count())
        else:
            QMessageBox.warning(self.parent(), "Error!! ", "<p>Not found S1T file.</p>", QMessageBox.Ok)

    def next(self):
        if self.index < (self.list.count()-1):
            self.index += 1
            self.list.setCurrentRow(self.index)
            self.__plot()

    def prev(self):
        if self.index > 0:
            self.index -= 1
        self.list.setCurrentRow(self.index)
        self.__plot()

    def __update(self):
        if self.list.count() > 0:
            self.__plot()

    def __plot(self, init: int = False):
        item = self.list.currentItem()
        d = item.data
        x = d.x()
        y = d.y()
        dtctr = Detector(x, y)
        idx = dtctr.detect(self.adjust_slider.value)
        item.set_detect_index(idx)

        if init:
            self.lines, = plt.plot(x, y)
            self.point, = plt.plot(x[idx], y[idx], marker=".")
            plt.pause(.1)
        else:
            self.lines.set_data(x, y)
            print("Sample Name: %s" % d.name)
            print("Detect index:%d" % idx)
            print("Detect position:%.2f[mm]" % x[idx])
            print("Detect load:%.2f[N]" % (y[idx] * 1000))
            print()
            self.point.set_data(x[idx], y[idx])

            plt.xlim(x.min(), x.max())
            plt.ylim(y.min(), y.max()+y.max()/10)
            plt.pause(.001)

    def save(self):
        file_name = self.path / "detect_data.xlsx"
        if file_name.exists():
            ret = QMessageBox.warning(self.parent(),
                                      "Overwrite",
                                      "Are you sure you want to overwrite the detect_data.xlsx",
                                      QMessageBox.No,
                                      QMessageBox.Save)
            if ret == QMessageBox.No:
                return

        if self.list.count() > 0:
            detect_data = []
            for i in range(self.list.count()):
                d = self.list.item(i)  # type:Item
                detect_data.append({
                    "Test Name": d.data.name,
                    "Index": d.detect_index,
                    "Distance [mm]": d.detect_distance,
                    "Loads [kN]": d.detect_load,
                })

            t = pd.DataFrame(
                detect_data
            )
            t.to_excel(file_name)
            QMessageBox.information(self.parent(), "Info", "Compleate writed file: %s" % file_name, QMessageBox.Ok)
        else:
            QMessageBox.warning(self.parent(),"Error", "Nothing data.", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication([])
    a = WaveDetectorX()
    a.show()
    app.exec_()
