from pathlib import Path
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
