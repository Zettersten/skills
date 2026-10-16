#!/usr/bin/env python3
"""Write examples/custom/mymod_01.tga, the texture sheet used by the example mod.

Pure Python (no PIL). 128x64, 32-bit uncompressed TGA, top-left origin so that
texture coordinates in the XML equal pixel positions in an image editor.

Layout (x, y, w, h):
  dialog 9-slice   (0, 0, 24, 24)   caps 4px, centre 16px   -> fresizeimage_mymod_dlg
  bar track        (0, 28, 18, 10)  caps 1px, repeat 16px   -> hresizeimage_mymod_bar_bg
  bar fill (red)   (0, 40, 18, 10)                          -> hresizeimage_mymod_bar_fg
  button normal    (32, 28, 40, 12)                         -> button_mymod_40 Normal / Disabled
  button highlit   (72, 28, 40, 12)                         -> NormalHighlit
  button pressed   (32, 42, 40, 12)                         -> Pressed / PressedHighlit
"""

from __future__ import annotations

import struct
from pathlib import Path

W, H = 128, 64
px = [[(0, 0, 0, 0) for _ in range(W)] for _ in range(H)]  # RGBA, fully transparent


def rect(x: int, y: int, w: int, h: int, rgba: tuple[int, int, int, int]) -> None:
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px[yy][xx] = rgba


def frame(x: int, y: int, w: int, h: int, fill, edge, inner) -> None:
    rect(x, y, w, h, fill)
    rect(x, y, w, 1, edge)
    rect(x, y + h - 1, w, 1, edge)
    rect(x, y, 1, h, edge)
    rect(x + w - 1, y, 1, h, edge)
    rect(x + 1, y + 1, w - 2, 1, inner)
    rect(x + 1, y + 1, 1, h - 2, inner)


# dialog: dark translucent body, gold edge, soft inner highlight
frame(0, 0, 24, 24, fill=(18, 16, 12, 215), edge=(166, 128, 32, 255), inner=(90, 70, 20, 255))

# bar track
rect(0, 28, 18, 10, (40, 40, 40, 255))
rect(0, 28, 18, 1, (10, 10, 10, 255))
rect(0, 37, 18, 1, (10, 10, 10, 255))
rect(0, 28, 1, 10, (10, 10, 10, 255))
rect(17, 28, 1, 10, (10, 10, 10, 255))

# bar fill: red with a lighter top line
rect(0, 40, 18, 10, (170, 28, 28, 255))
rect(0, 40, 18, 1, (230, 90, 90, 255))
rect(0, 49, 18, 1, (110, 10, 10, 255))

# buttons
frame(32, 28, 40, 12, fill=(60, 48, 24, 255), edge=(166, 128, 32, 255), inner=(110, 86, 30, 255))   # normal
frame(72, 28, 40, 12, fill=(84, 66, 30, 255), edge=(220, 180, 60, 255), inner=(150, 118, 40, 255))  # highlit
frame(32, 42, 40, 12, fill=(36, 28, 14, 255), edge=(166, 128, 32, 255), inner=(60, 48, 20, 255))    # pressed


def write_tga(path: Path) -> None:
    header = struct.pack(
        "<BBBHHBHHHHBB",
        0,      # id length
        0,      # no colour map
        2,      # uncompressed true-colour
        0, 0, 0,  # colour map spec
        0, 0,   # origin
        W, H,
        32,     # bits per pixel
        0x28,   # descriptor: 8 alpha bits, top-left origin
    )
    body = bytearray()
    for row in px:                      # top-left origin: first row written is the top row
        for r, g, b, a in row:
            body += bytes((b, g, r, a))  # TGA stores BGRA
    path.write_bytes(header + bytes(body))


if __name__ == "__main__":
    out = Path(__file__).parent / "custom" / "mymod_01.tga"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_tga(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
