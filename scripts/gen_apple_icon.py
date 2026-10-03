# -*- coding: utf-8 -*-
"""Generate a standard 180x180 apple-touch-icon.png in assets/img by
reproducing the designed favicon mark (blue rounded square #0b4f8a + white "S")
— same single source of truth as favicon.svg / favicon.ico.

Apple expects a SQUARE icon (180x180 recommended). The previous
apple-touch-icon link pointed to logo.png (261x71 wide), which iOS crops
awkwardly. This script produces the proper square PNG."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE = (11, 79, 138)  # #0b4f8a — same as favicon.svg / favicon.ico
SIZE = 180

for cand in (
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
):
    if os.path.exists(cand):
        FONT = cand
        break
else:
    FONT = None


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(SIZE * 0.22)  # mirror the SVG rounded-square radius
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=r, fill=BLUE)
    fs = int(SIZE * 0.66)
    f = ImageFont.truetype(FONT, fs) if FONT else ImageFont.load_default()
    bbox = d.textbbox((0, 0), "S", font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (SIZE - tw) / 2 - bbox[0]
    y = (SIZE - th) / 2 - bbox[1] + SIZE * 0.04
    d.text((x, y), "S", font=f, fill=(255, 255, 255, 255))
    out = os.path.join(ROOT, "assets", "img", "apple-touch-icon.png")
    img.save(out, format="PNG")
    print("wrote %s (%dx%d, %d bytes)" % (out, SIZE, SIZE, os.path.getsize(out)))


if __name__ == "__main__":
    main()
