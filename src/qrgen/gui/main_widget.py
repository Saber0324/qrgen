from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from qrgen.gui.custom_buttons import UploadButton
from qrgen.qr_code.qr_generator import generated_path
from qrgen.gui.module_card import ModuleCard
from qrgen.gui.color_picker import ColorPickWdg


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        last_generated_pixmap = QtGui.QPixmap(str(generated_path / "qrcode"))
        scaled_pixmap = last_generated_pixmap.scaled(
            200,
            200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.setWindowTitle("qrgen")
        top_layout = QtWidgets.QHBoxLayout(self)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(container)

        preview = QtWidgets.QFrame()
        preview.setFixedWidth(250)

        preview_layout = QtWidgets.QVBoxLayout()
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        preview.setLayout(preview_layout)

        preview_label = QtWidgets.QLabel()
        preview_label.setPixmap(scaled_pixmap)

        upload_button = UploadButton("Upload an image")

        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(upload_button)

        top_layout.addWidget(scroll)
        top_layout.addWidget(preview)

        content_card = ModuleCard("CONTENT")
        content_card.add_widget(QtWidgets.QLabel("Your website URL"))
        content_card.add_widget(QtWidgets.QLineEdit())
        container_layout.addWidget(content_card)

        design_card = ModuleCard("DESIGN")
        design_card.add_widget(ColorPickWdg("Background color", "#FFF"))
        design_card.add_widget(ColorPickWdg("QR color", "#000"))
        container_layout.addWidget(design_card)


class ImageDropTarget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__("Drop Image Here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaaaaa")
        self.setFixedSize(150, 50)
        self.setAcceptDrops(True)

        self._dropped_file = None

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
        pix = QtGui.QPixmap(self._dropped_file).scaled(100, 100)
        self.setPixmap(pix)


def run_gui():
    app = QtWidgets.QApplication()
    widget = MainWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    run_gui()
