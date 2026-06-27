import io
from pathlib import Path
from PIL import Image
from PySide6 import QtGui, QtCore, QtSvg


def recolor_svg(path: Path, color: str) -> QtGui.QPixmap:
    svg_text = path.read_text().replace('fill="#000000"', f'fill="{color}"')
    renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_text.encode()))
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def svg_to_pixmap(svg_string: str, size: int = 290) -> QtGui.QPixmap:
    renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_string.encode()))
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def embed_logo(svg_string: str, logo: Path):
    pixmap = svg_to_pixmap(svg_string)
    buffer = QtCore.QByteArray()
    device = QtCore.QBuffer(buffer)
    device.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(device, "PNG")
    device.close()

    qr_image = Image.open(io.BytesIO(buffer.data()))

    if logo.suffix == ".svg":
        logo_image = svg_logo_to_pil(logo)
    else:
        logo_image = Image.open(logo).convert("RGBA")

    logo_size = qr_image.width // 4
    logo_image = logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    pos_x = (qr_image.width - logo_size) // 2
    pos_y = (qr_image.height - logo_size) // 2

    qr_image.paste(logo_image, (pos_x, pos_y), logo_image)

    return qr_image


def svg_logo_to_pil(logo_path: Path) -> Image.Image:
    pixmap = QtGui.QPixmap(str(logo_path))
    buffer = QtCore.QByteArray()
    device = QtCore.QBuffer(buffer)
    device.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(device, "PNG")
    device.close()
    return Image.open(io.BytesIO(buffer.data())).convert("RGBA")
