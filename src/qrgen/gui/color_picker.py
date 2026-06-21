from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


class ColorPickWdg(QtWidgets.QGroupBox):
    def __init__(self, text: str, default_color: str):
        super().__init__(text)

        layout = QtWidgets.QHBoxLayout(self)

        self.color_lbl = QtWidgets.QLabel("#FFFFFF")
        self.color_swatch = QtWidgets.QPushButton()
        self.color_swatch.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.color_swatch.setFixedSize(32, 32)

        layout.addWidget(self.color_lbl)
        layout.addWidget(self.color_swatch)

        self.color_dlg = QtWidgets.QColorDialog()

        self.color_swatch.clicked.connect(self._on_color_swatch_clicked)
        self.set_color(QtGui.QColor(default_color))

    def _on_color_swatch_clicked(self):
        result = self.color_dlg.exec()
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return

        self.set_color(self.color_dlg.currentColor())

    def set_color(self, color: QtGui.QColor):
        self.current_color = color
        hex_color = color.name()

        self.color_lbl.setText(hex_color.upper())
        self.color_swatch.setStyleSheet(f"background-color: {hex_color};")

    def color(self):
        return self.current_color
