from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from qrgen.gui.constants import ASSETS_DIR
from qrgen.gui.custom_buttons import InsertUrl, UploadButton
from qrgen.qr_code.qr_generator import generated_path
from qrgen.gui.custom_widgets import ModuleCard, ColorPickWdg


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
        self.setMinimumSize(700, 400)
        top_layout = QtWidgets.QHBoxLayout(self)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(container)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        preview = QtWidgets.QFrame()
        preview.setFixedWidth(250)
        preview.setObjectName("preview_frame")
        preview.setStyleSheet("""
            QFrame#preview_frame {
                border: 1px solid #606090;
                border-radius: 14px;
            }
        """)

        preview_layout = QtWidgets.QVBoxLayout()
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        preview.setLayout(preview_layout)

        preview_label = QtWidgets.QLabel()
        preview_label.setPixmap(scaled_pixmap)
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        preview_layout.addWidget(preview_label)

        top_layout.addWidget(scroll)
        top_layout.addWidget(preview)

        tabs_widget = QtWidgets.QTabWidget()
        tabs_widget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        tabs_widget.setStyleSheet("""
                        QTabWidget::pane {
                            background: transparent;
                            border: 3px;
                        }
                        QTabBar {
                            background: transparent;
                        }
                        QTabBar::tab {
                            padding: 3px 10px;
                            border-radius: 10px;
                            margin: 2px;
                        }
                        QTabBar::tab:selected {
                            background: lightgrey;
                            color: black;
                        }
        """)

        self.qr_color_button = ColorPickWdg("QR color", "#000")
        self.bg_color_button = ColorPickWdg("Background color", "#FFF")

        self.grad_options_combo = QtWidgets.QComboBox()
        self.grad_options_combo.addItems(["None", "Vertical", "Circular", "Horizontal"])
        self.grad_options_combo.setBaseSize(70, 30)
        self.grad_options_combo.currentTextChanged.connect(self._on_grad_option_change)
        self.grad_options_combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #606090;
                    border-radius: 6px;
                    padding: 0px 8px;
                }
                QComboBox::drop-down {
                    width: 0px;
                }
                QComboBox QAbstractItemView {
                    border-radius: 6px;
                    border: 1px solid #606090;

                } """)
        self.grad_options_combo.setSizeAdjustPolicy(
            QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.grad_start_button = ColorPickWdg("Start color", "#000")
        self.grad_end_button = ColorPickWdg("End color", "#000")

        color_widget = QtWidgets.QWidget()

        self.color_main_layout = QtWidgets.QVBoxLayout(color_widget)

        color_button_layout = QtWidgets.QHBoxLayout()

        self.gradient_widget = QtWidgets.QWidget()
        self.gradient_buttons_layout = QtWidgets.QHBoxLayout(self.gradient_widget)

        gradient_config_widget = QtWidgets.QWidget()
        gradient_config_layout = QtWidgets.QHBoxLayout(gradient_config_widget)

        gradient_config_label = QtWidgets.QLabel("Select gradient style:")

        gradient_config_layout.addWidget(gradient_config_label)
        gradient_config_layout.addWidget(self.grad_options_combo)
        gradient_config_layout.addStretch()

        self.gradient_buttons_layout.addWidget(self.grad_start_button)
        self.gradient_buttons_layout.addWidget(self.grad_end_button)
        self.gradient_buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.color_main_layout.addWidget(gradient_config_widget)
        self.color_main_layout.addLayout(color_button_layout)

        color_button_layout.addWidget(self.qr_color_button)
        color_button_layout.addWidget(self.bg_color_button)

        self.color_main_layout.addWidget(self.gradient_widget)
        self.gradient_widget.setVisible(False)

        tabs_widget.addTab(color_widget, "Color")

        self.upload_button = UploadButton("Upload an image")

        tabs_widget.addTab(self.upload_button, "Logo")

        tabs_widget.addTab(QtWidgets.QWidget(), "Shape")

        content_card = ModuleCard("CONTENT")
        content_card.add_widget(InsertUrl("Insert url"))
        container_layout.addWidget(content_card)

        container_layout.setSpacing(10)

        design_card = ModuleCard("DESIGN")
        design_card.add_widget(tabs_widget)
        container_layout.addWidget(design_card)

    def _on_bg_color_selected(self):
        print(self.bg_color_button.color)

    def _on_grad_option_change(self, text):
        self.gradient_widget.setVisible(text != "None")


def run_gui():
    app = QtWidgets.QApplication()
    widget = MainWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    run_gui()
