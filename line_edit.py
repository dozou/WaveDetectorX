from PyQt5.Qt import QLineEdit
import pathlib


class LineEdit(QLineEdit):

    def __init__(self, text=""):
        super(LineEdit, self).__init__(text)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            print("Drag...")
            e.accept()

    def dropEvent(self, e):
        print("drop...")
        if e.mimeData().hasUrls():
            url = e.mimeData().urls()
            url = pathlib.Path(url[0].toLocalFile())
            if url.is_file():
                url = url.parent
            self.setText(str(url))
