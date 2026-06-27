from pathlib import Path
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize
from qrgen.constants import ASSETS_DIR
from qrgen.gui.helpers import recolor_svg


class UploadButton(QtWidgets.QGroupBox):
    def __init__(self, text: str):
        super().__init__(text)
        upload_icon_path = ASSETS_DIR / "upload.svg"
        self.file_path: Path | None = None

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
        self.setMaximumHeight(80)

        layout = QtWidgets.QHBoxLayout(self)
        self.upload_label = QtWidgets.QLabel("No image selected")
        upload_button = QtWidgets.QPushButton()
        upload_button.setIcon(QtGui.QIcon(recolor_svg(upload_icon_path, "#606090")))
        upload_button.setFixedSize(QSize(30, 30))
        upload_button.setFlat(True)
        upload_button.clicked.connect(self._on_upload_button_clicked)

        layout.addWidget(self.upload_label)
        layout.addWidget(upload_button)

    def _on_upload_button_clicked(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.svg *.webp)",
        )
        if file_path:
            self.file_path = Path(file_path)
            self.upload_label.setText(f"{self.file_path.name}")


class InputLine(QtWidgets.QGroupBox):
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
        self.url_line = QtWidgets.QLineEdit()
        self.url_line.setPlaceholderText("https://example.com")
        self.url_line.setStyleSheet("""
                    QLineEdit {
                        border-width: 3px;
                        border-style: solid;
                        border-color: transparent;
                        padding: 4px;
                    }
                    QLineEdit:focus {
                        border-color: transparent;
                    }""")
        layout.addWidget(self.url_line)
