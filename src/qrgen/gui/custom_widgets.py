from pathlib import Path
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize, Qt

from qrgen.constants import ASSETS_DIR, GENERATED_DIR


class ImageDropTarget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__("Drop Image Here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaaaaa")
        self.setFixedSize(200, 150)
        self.setAcceptDrops(True)

        self._dropped_file: str | None = None
        self.file_name: str | None = None

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
            event.accept
            self.file_name = Path(self._dropped_file).name


class ModuleCard(QtWidgets.QFrame):
    def __init__(self, title: str):
        super().__init__()

        module_layout = QtWidgets.QVBoxLayout(self)
        module_layout.setContentsMargins(10, 10, 10, 6)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.setObjectName("module_card")
        self.setStyleSheet("""
            QFrame#module_card {
                border: 1px solid #606090;
                border-radius: 14px;
            }
        """)

        header = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header)

        title_label = QtWidgets.QLabel(title)
        title_label.setFont(QtGui.QFont("Jetbrains Mono Nerd"))
        title_label.setStyleSheet(
            """QLabel {
                font-size: 14px;
            }
            """
        )

        self.toggle_btn = QtWidgets.QPushButton("↑")
        self.toggle_btn.setFlat(True)
        self.toggle_btn.setFixedSize(QSize(25, 25))
        self.toggle_btn.clicked.connect(self._toggle)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)
        header_layout.setContentsMargins(0, 0, 0, 5)

        self.body = QtWidgets.QWidget()
        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 10, 0, 10)

        module_layout.addWidget(header)
        module_layout.setSpacing(0)
        module_layout.addWidget(separator)
        module_layout.addWidget(self.body)

    def _toggle(self):
        visible = self.body.isVisible()
        self.toggle_btn.setText("↓" if visible else "↑")
        self.body.setVisible(not visible)

    def add_widget(self, widget: QtWidgets.QWidget):
        self.body_layout.addWidget(widget)


class ColorPickWdg(QtWidgets.QGroupBox):
    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, text: str, default_color: str):
        super().__init__(text)

        layout = QtWidgets.QHBoxLayout(self)
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
        self.setMaximumHeight(70)

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
        self.color_changed.emit(color)

    @property
    def color(self):
        return self.current_color


class ExportWidget(QtWidgets.QGroupBox):
    def __init__(self, text: str):
        super().__init__(text)
        self.download_icon = QtGui.QIcon(str(ASSETS_DIR / "download.svg"))

        self.save_path: Path = GENERATED_DIR

        layout = QtWidgets.QVBoxLayout(self)

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

        layout.addWidget(self._build_generate_widget())
        layout.addWidget(self._build_save_widget())
        layout.addWidget(self._build_save_path_widget())

        self.select_path_button.clicked.connect(self._on_select_path)

    def _build_save_widget(self):
        save_widget = QtWidgets.QWidget()
        save_layout = QtWidgets.QHBoxLayout(save_widget)

        self.save_title = QtWidgets.QLineEdit()
        self.save_title.setPlaceholderText("qr_code.png")

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save")
        self.save_button.setIcon(self.download_icon)

        save_layout.addWidget(self.save_title)
        save_layout.addWidget(self.save_button)

        return save_widget

    def _build_generate_widget(self):
        generate_widget = QtWidgets.QWidget()
        generate_layout = QtWidgets.QHBoxLayout(generate_widget)

        self.generate_button = QtWidgets.QPushButton()
        self.generate_button.setText("Generate preview")

        generate_layout.addWidget(self.generate_button)

        return generate_widget

    def _build_save_path_widget(self):
        save_path_widget = QtWidgets.QWidget()
        save_path_layout = QtWidgets.QHBoxLayout(save_path_widget)

        self.select_path_button = QtWidgets.QPushButton()
        self.select_path_button.setText("Select save directory")

        save_path_layout.addWidget(self.select_path_button)

        return save_path_widget

    def _on_select_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select save directory")
        if path:
            self.save_path = Path(path)
