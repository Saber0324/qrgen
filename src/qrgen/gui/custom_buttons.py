from PySide6 import QtWidgets
from PySide6.QtGui import QColor


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
