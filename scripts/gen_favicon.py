# -*- coding: utf-8 -*-
"""Generate a multi-resolution favicon.ico at the repo root by reproducing the
designed favicon.svg (blue rounded square #0b4f8a + white "S").

Placing favicon.ico at the site root means the browser's implicit /favicon.ico
request returns 200 instead of 404. A *single source of truth* for the icon
mark is favicon.svg in assets/img; this script only rasterizes it for the
legacy .ico path (some browsers / crawlers still hit /favicon.ico).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE = (11, 79, 138)  # #0b4f8a
SIZES = [16, 32, 48, 64]

# Prefer a bold Arial; fall back gracefully.
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


def make(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = max(1, int(size * 0.22))  # 14/64 of the SVG viewBox
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BLUE)
    fs = int(size * 0.66)  # 42/64 of the SVG font-size
    f = ImageFont.truetype(FONT, fs) if FONT else ImageFont.load_default()
    bbox = d.textbbox((0, 0), "S", font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] + size * 0.04  # nudge down to mirror SVG baseline
    d.text((x, y), "S", font=f, fill=(255,255,255,255))
    return img


def main():
    imgs = [make(s) for s in SIZES]
    out = os.path.join(ROOT, "favicon.ico")
    # First image sets the default; append the rest so the .ico carries every size.
    imgs[0].save(out, format="ICO", append_images=imgs[1:], sizes=[(s, s) for s in SIZES])
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
