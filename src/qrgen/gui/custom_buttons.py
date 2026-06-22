from PySide6 import QtWidgets, QtGui, QtCore, QtSvg
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from qrgen.gui.custom_widgets import ImageDropTarget
from qrgen.gui.constants import ASSETS_DIR


class ColorButton(QtWidgets.QPushButton):
    def __init__(self, color: QColor = QColor("#000000")):
        super().__init__()
        self.color = color

        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.clicked.connect(self.open_color_dialog)

    def open_color_dialog(self):
        selected_color = QtWidgets.QColorDialog().getColor()
        if selected_color.isValid():
            self.color = selected_color
        self.setStyleSheet(f"background-color: {self.color.name()}")


class UploadButton(QtWidgets.QGroupBox):
    def __init__(self, text: str):
        super().__init__(text)
        upload_icon_path = ASSETS_DIR / "upload.svg"
        upload_icon_text = upload_icon_path.read_text()
        upload_icon_text = upload_icon_text.replace('fill="#000000"', 'fill="#606090"')
        renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(upload_icon_text.encode()))
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #606090;
                border-radius: 6px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 3px;
            }
        """)

        layout = QtWidgets.QHBoxLayout(self)
        self.upload_label = QtWidgets.QLabel("No image selected")
        upload_button = QtWidgets.QPushButton()
        upload_button.setIcon(QtGui.QIcon(pixmap))
        upload_button.setFixedSize(QSize(30, 30))
        upload_button.setFlat(True)
        upload_button.clicked.connect(self._on_upload_button_clicked)

        layout.addWidget(self.upload_label)
        layout.addWidget(upload_button)

        self.upload_dialog = QtWidgets.QDialog()
        self.upload_dialog.setWindowTitle("qrgen")
        upload_layout = QtWidgets.QHBoxLayout(self.upload_dialog)
        self.upload_dropable = ImageDropTarget()
        upload_layout.addWidget(self.upload_dropable)

    def _on_upload_button_clicked(self, dialog: QtWidgets.QDialog):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.svg)"
        )
        if file_path:
            self.upload_label.setText(f"{file_path.split('/')[-1]}")
            dialog.accept()


class InsertUrl(QtWidgets.QGroupBox):
    def __init__(self, text: str):
        super().__init__(text)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #606090;
                border-radius: 6px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 3px;
            }
        """)
        layout = QtWidgets.QVBoxLayout(self)
        url_line = QtWidgets.QLineEdit()
        url_line.setPlaceholderText("https://example.com")
        url_line.setStyleSheet("""
                    QLineEdit {
                        border-width: 3px;
                        border-style: solid;
                        border-color: transparent;
                        padding: 4px;
                    }
                    QLineEdit:focus {
                        border-color: transparent;
                    }""")
        layout.addWidget(url_line)
