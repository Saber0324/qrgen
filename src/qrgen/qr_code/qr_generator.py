from typing import cast
import segno


def _is_dark(matrix, row, col):
    if row < 0 or col < 0 or row >= len(matrix) or col >= len(matrix[0]):
        return False
    return bool(matrix[row][col])


class QRGenerator:
    def __init__(self, content: str, micro: bool = False) -> None:
        self.generated_qr = segno.make(content=content, error="H", micro=micro)

    def show(self):
        if self.generated_qr:
            self.generated_qr.show(delete_after=30)
        else:
            print("No QR has been generated")

    def build_svg(
        self,
        shape: str,
        color: str,
        bg_color: str,
        gradient: str = "None",
        grad_start_color: str | None = None,
        grad_end_color: str | None = None,
        grad_offset: float = 0.0,
    ) -> str | None:
        if self.generated_qr.matrix:
            module_size = 10
            quiet_zone = 4
            matrix_size = len(self.generated_qr.matrix)
            total_size = (matrix_size + quiet_zone * 2) * module_size

            svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_size}" height="{total_size}">'
            svg += (
                f'<rect width="{total_size}" height="{total_size}" fill="{bg_color}"/>'
            )

            directions = {
                "Horizontal": (
                    str(int(total_size * grad_offset)),
                    "0",
                    str(total_size),
                    "0",
                ),
                "Vertical": (
                    "0",
                    str(int(total_size * grad_offset)),
                    "0",
                    str(total_size),
                ),
                "Diagonal": (
                    str(int(total_size * grad_offset)),
                    str(int(total_size * grad_offset)),
                    str(total_size),
                    str(total_size),
                ),
            }

            if gradient != "None" and grad_start_color and grad_end_color:
                x1, y1, x2, y2 = directions[gradient]
                svg += f'<defs><linearGradient id="grad" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">'
                svg += f'<stop offset="0%" stop-color="{grad_start_color}"/>'
                svg += f'<stop offset="100%" stop-color="{grad_end_color}"/>'
                svg += "</linearGradient></defs>"
                fill = "url(#grad)"
            else:
                fill = color

            offset = quiet_zone * module_size
            for y, row in enumerate(self.generated_qr.matrix):
                for x, cell in enumerate(row):
                    if cell:
                        cx = offset + x * module_size
                        cy = offset + y * module_size

                        if shape == "Dotted":
                            r = module_size // 2
                            svg += f'<circle cx="{cx + r}" cy="{cy + r}" r="{r}" fill="{fill}"/>'

                        elif shape == "Rounded":
                            r = 3
                            svg += f'<rect x="{cx}" y="{cy}" width="{module_size}" height="{module_size}" rx="{r}" ry="{r}" fill="{fill}"/>'

                            if _is_dark(self.generated_qr.matrix, y, x + 1):
                                svg += f'<rect x="{cx + module_size - r}" y="{cy}" width="{r * 2}" height="{module_size}" fill="{fill}"/>'

                            if _is_dark(self.generated_qr.matrix, y + 1, x):
                                svg += f'<rect x="{cx}" y="{cy + module_size - r}" width="{module_size}" height="{r * 2}" fill="{fill}"/>'

                            if _is_dark(self.generated_qr.matrix, y, x - 1):
                                svg += f'<rect x="{cx - r}" y="{cy}" width="{r * 2}" height="{module_size}" fill="{fill}"/>'

                            if _is_dark(self.generated_qr.matrix, y - 1, x):
                                svg += f'<rect x="{cx}" y="{cy - r}" width="{module_size}" height="{r * 2}" fill="{fill}"/>'

                        else:
                            svg += f'<rect x="{cx}" y="{cy}" width="{module_size}" height="{module_size}" fill="{fill}"/>'

            svg += "</svg>"
            return svg
        else:
            print("No QR has been generated")


if __name__ == "__main__":
    qr = QRGenerator(content="test")
    with open("test.svg", "w") as f:
        f.write(
            cast(
                str,
                qr.build_svg(
                    "Rounded", "#606090", "#FFF", "Vertical", "#606090", "#FF0000", 0.4
                ),
            )
        )

