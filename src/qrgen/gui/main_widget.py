from PySide6 import QtCore, QtGui, QtWidgets
from qrgen.qr_code import qr_generator
from qrgen.qr_code.qr_generator import generated_path
from qrgen.gui.module_card import ModuleCard


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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

        top_layout.addWidget(scroll)
        top_layout.addWidget(preview)

        last_generated_pixmap = QtGui.QPixmap(str(generated_path / "qrcode"))
        display_label = QtWidgets.QLabel()
        display_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        display_label.setPixmap(last_generated_pixmap)

        content_card = ModuleCard("CONTENT")
        content_card.add_widget(QtWidgets.QLabel("Your website URL"))
        content_card.add_widget(QtWidgets.QLineEdit())
        container_layout.addWidget(content_card)


def run_gui():
    app = QtWidgets.QApplication()
    widget = MainWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    run_gui()
