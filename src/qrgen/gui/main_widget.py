import io

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from qrgen.gui.custom_buttons import InputLine, UploadButton
from qrgen.gui.custom_widgets import ModuleCard, ColorPickWdg, ExportWidget
from qrgen.qr_code.qr_generator import QRGenerator
from qrgen.gui.helpers import svg_to_pixmap, embed_logo


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.qr_svg = None
        self.setWindowTitle("qrgen")
        self.setMinimumSize(700, 400)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        top_layout = QtWidgets.QHBoxLayout(self)
        top_layout.addWidget(self._build_scroll_area())
        top_layout.addWidget(self._build_preview_frame())

    def _build_scroll_area(self):
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        container_layout.addWidget(self._build_content_card())
        container_layout.addWidget(self._build_design_card())

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        return scroll

    def _build_preview_frame(self):
        preview_frame = QtWidgets.QFrame()
        preview_frame.setFixedWidth(250)
        preview_frame.setObjectName("preview_frame")
        preview_frame.setStyleSheet(
            """
            QFrame#preview_frame {
                border: 1px solid #606090;
                border-radius: 14px;
            }
            """
        )

        preview_layout = QtWidgets.QVBoxLayout(preview_frame)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.preview_label = QtWidgets.QLabel()
        self.preview_label.setPixmap(QtGui.QPixmap())
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_widget = ExportWidget("Generate and save")

        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.save_widget)

        return preview_frame

    def _build_content_card(self):
        self.insert_url = InputLine("Insert content")
        content_card = ModuleCard("CONTENT")
        content_card.add_widget(self.insert_url)
        return content_card

    def _build_design_card(self):
        design_card = ModuleCard("DESIGN")
        design_card.add_widget(self._build_tabs_widget())
        return design_card

    def _build_color_tab(self):
        self.qr_color_button = ColorPickWdg("QR color", "#000")
        self.bg_color_button = ColorPickWdg("Background color", "#FFF")

        color_widget = QtWidgets.QWidget()
        self.color_main_layout = QtWidgets.QVBoxLayout(color_widget)

        color_button_layout = QtWidgets.QHBoxLayout()
        self.color_main_layout.addLayout(color_button_layout)

        color_button_layout.addWidget(self.qr_color_button)
        color_button_layout.addWidget(self.bg_color_button)

        return color_widget

    def _build_gradient_combo(self):
        self.grad_options_combo = QtWidgets.QComboBox()
        self.grad_options_combo.addItems(["None", "Vertical", "Diagonal", "Horizontal"])
        self.grad_options_combo.setBaseSize(70, 30)
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
        return self.grad_options_combo

    def _build_gradient_buttons(self):
        self.grad_start_button = ColorPickWdg("Start color", "#000")
        self.grad_end_button = ColorPickWdg("End color", "#000")

        self.gradient_buttons_widget = QtWidgets.QWidget()
        self.gradient_buttons_layout = QtWidgets.QHBoxLayout(
            self.gradient_buttons_widget
        )

        self.gradient_buttons_layout.addWidget(self.grad_start_button)
        self.gradient_buttons_layout.addWidget(self.grad_end_button)
        self.gradient_buttons_layout.setContentsMargins(0, 0, 0, 0)

        return self.gradient_buttons_widget

    def _build_gradient_offset_slide(self):
        grad_offset_widget = QtWidgets.QWidget()
        grad_offset_layout = QtWidgets.QVBoxLayout(grad_offset_widget)

        grad_offset_label = QtWidgets.QLabel("Gradient offset:")

        self.grad_offset_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.grad_offset_slider.setRange(0, 100)
        self.grad_offset_slider.setValue(0)

        grad_offset_layout.addWidget(grad_offset_label)
        grad_offset_layout.addWidget(self.grad_offset_slider)

        return grad_offset_widget

    def _build_gradient_tab(self):
        gradient_tab_widget = QtWidgets.QWidget()
        gradient_tab_layout = QtWidgets.QVBoxLayout(gradient_tab_widget)

        gradient_config_layout = QtWidgets.QHBoxLayout()
        gradient_tab_layout.addLayout(gradient_config_layout)

        gradient_tab_label = QtWidgets.QLabel("Select gradient style:")

        gradient_config_layout.addWidget(gradient_tab_label)
        gradient_config_layout.addWidget(self._build_gradient_combo())
        gradient_config_layout.addStretch()

        gradient_tab_layout.addWidget(self._build_gradient_buttons())
        gradient_tab_layout.addWidget(self._build_gradient_offset_slide())
        return gradient_tab_widget

    def _build_logo_tab(self):
        self.upload_button = UploadButton("Upload an image")
        self.upload_button.setMaximumHeight(80)
        return self.upload_button

    def _build_shape_tab(self):
        shape_widget = QtWidgets.QWidget()
        shape_layout = QtWidgets.QVBoxLayout(shape_widget)
        self.shape_list = QtWidgets.QListWidget()
        self.shape_list.addItems(["Default", "Rounded", "Dotted"])

        shape_layout.addWidget(self.shape_list)
        return shape_widget

    def _build_tabs_widget(self):
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

        tabs_widget.addTab(self._build_color_tab(), "Color")
        tabs_widget.addTab(self._build_gradient_tab(), "Gradient")
        tabs_widget.addTab(self._build_logo_tab(), "Logo")
        tabs_widget.addTab(self._build_shape_tab(), "Shape")

        return tabs_widget

    def _connect_signals(self):
        self.save_widget.generate_button.clicked.connect(self._on_generate)
        self.save_widget.save_button.clicked.connect(self._on_save)

    def _on_generate(self):
        url = self.insert_url.url_line.text()
        if not url:
            return

        qr = QRGenerator(content=url)

        shape = (
            self.shape_list.currentItem().text()
            if self.shape_list.currentItem()
            else "Default"
        )
        color = self.qr_color_button.color.name()
        bg_color = self.bg_color_button.color.name()
        gradient = self.grad_options_combo.currentText()
        grad_start = self.grad_start_button.color.name()
        grad_end = self.grad_end_button.color.name()
        grad_offset = self.grad_offset_slider.value() / 100

        svg = qr.build_svg(
            shape=shape,
            color=color,
            bg_color=bg_color,
            gradient=gradient,
            grad_start_color=grad_start,
            grad_end_color=grad_end,
            grad_offset=grad_offset,
        )

        if svg:
            self.qr_svg = svg
            if self.upload_button.file_path:
                pil_image = embed_logo(svg, self.upload_button.file_path)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer.seek(0)
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(buffer.read())
            else:
                pixmap = svg_to_pixmap(svg)
            self.preview_label.setPixmap(pixmap)

    def _on_save(self):
        if not self.qr_svg:
            print("No qr found")
            self._on_generate()
        filename = self.save_widget.save_title.text() or "qr_code.svg"
        save_path = self.save_widget.save_path / filename

        if save_path.exists():
            stem = save_path.stem
            suffix = save_path.suffix
            counter = 1
            while save_path.exists():
                save_path = self.save_widget.save_path / f"{stem}_{counter}{suffix}"
                counter += 1

        if self.qr_svg:
            print(save_path)
            save_path.write_text(self.qr_svg)


def run_gui():
    app = QtWidgets.QApplication()
    widget = MainWidget()
    widget.show()
    app.exec()


if __name__ == "__main__":
    run_gui()
