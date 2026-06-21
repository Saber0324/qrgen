from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QColor
from qrgen.gui.drop_target import ImageDropTarget
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
        upload_button_icon = QtGui.QPixmap(str(ASSETS_DIR / "upload.svg"))

        layout = QtWidgets.QHBoxLayout(self)
        self.upload_label = QtWidgets.QLabel("No image found")
        upload_button = QtWidgets.QPushButton()
        upload_button.setIcon(upload_button_icon)
        upload_button.clicked.connect(self._on_upload_button_clicked)

        layout.addWidget(self.upload_label)
        layout.addWidget(upload_button)

        self.upload_dialog = QtWidgets.QDialog()
        self.upload_dialog.setWindowTitle("qrgen")
        upload_layout = QtWidgets.QHBoxLayout(self.upload_dialog)
        self.upload_dropable = ImageDropTarget()
        upload_layout.addWidget(self.upload_dropable)

    def _on_upload_button_clicked(self):
        result = self.upload_dialog.exec()
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return
        self.upload_label.setText(f"Icon: {self.upload_dropable._dropped_file}")
