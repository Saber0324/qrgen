from PySide6 import QtWidgets


class ModuleCard(QtWidgets.QFrame):
    def __init__(self, title: str):
        super().__init__()

        module_layout = QtWidgets.QVBoxLayout(self)

        header = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header)

        title_label = QtWidgets.QLabel(title)

        self.toggle_btn = QtWidgets.QPushButton("↑")
        self.toggle_btn.setFlat(True)
        self.toggle_btn.clicked.connect(self._toggle)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)

        self.body = QtWidgets.QWidget()
        self.body_layout = QtWidgets.QVBoxLayout(self.body)

        module_layout.addWidget(header)
        module_layout.addWidget(self.body)

    def _toggle(self):
        visible = self.body.isVisible()
        self.toggle_btn.setText("↑" if visible else "↓")
        self.body.setVisible(not visible)

    def add_wiget(self, widget: QtWidgets.QWidget):
        self.body_layout.addWidget(widget)
