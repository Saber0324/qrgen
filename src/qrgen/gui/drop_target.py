from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


class ImageDropTarget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__("Drop Image Here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaaaaa")
        self.setFixedSize(200, 150)
        self.setAcceptDrops(True)

        self._dropped_file: str | None = None

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if not mime.hasUrls():
            return
        elif len(mime.urls()) != 1:
            return

        url = mime.urls()[0]
        local_path = url.toLocalFile()
        if local_path.endswith(".png"):
            event.accept()
            self._dropped_file = local_path

    def dropEvent(self, event):
        if self._dropped_file is not None:
            pix = QtGui.QPixmap(self._dropped_file).scaled(100, 100)
            self.setPixmap(pix)
