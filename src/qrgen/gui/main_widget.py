from PySide6 import QtCore, QtGui, QtWidgets
from qrgen.main import generated_path


class MainWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.top_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.data_line = QtWidgets.QLineEdit()
        self.data_line.setPlaceholderText("Insert information")

        self.last_generated_pixmap = QtGui.QPixmap(str(generated_path / "qrcode"))
        self.display_label = QtWidgets.QLabel()
        self.display_label.setPixmap(self.last_generated_pixmap)

        self.create_button = QtWidgets.QPushButton()
        self.create_button.setText("Create")
        self.create_button.clicked.connect(self._on_create_button_click)

        self.qr_code_label = QtWidgets.QLabel()
        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self._on_save_button_click)

        self.setWindowTitle("qr creator")
        self.setLayout(self.top_layout)
        self.top_layout.addWidget(self.data_line)
        self.top_layout.addWidget(self.display_label)
        self.top_layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.save_button)

    def _on_create_button_click(self):
        print(self.create_button.text())

    def _on_save_button_click(self):
        print(self.save_button.text())


def run_gui():
    app = QtWidgets.QApplication()
    widget = MainWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    run_gui()
