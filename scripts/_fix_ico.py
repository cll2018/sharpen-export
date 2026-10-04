# -*- coding: utf-8 -*-
"""One-off: build a real multi-resolution favicon.ico.

Pillow 12's ICO writer silently ignores append_images (writes a single
16x16 entry — the root cause of the 338-byte favicon). ICO images are
PNG-compressed here, which every modern browser supports.
"""
import io
import os
import struct

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE = (11, 79, 138)
SIZES = [16, 32, 48, 64]

FONT = None
for cand in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
    if os.path.exists(cand):
        FONT = cand
        break


def make(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = max(1, int(size * 0.22))
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BLUE)
    fs = int(size * 0.66)
    f = ImageFont.truetype(FONT, fs) if FONT else ImageFont.load_default()
    bbox = d.textbbox((0, 0), "S", font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] + size * 0.04
    d.text((x, y), "S", font=f, fill=(255, 255, 255, 255))
    return img


def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def build_ico(images, out_path):
    # ICO header: reserved(2) type(2)=1 count(2)
    n = len(images)
    header = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    entries = []
    data = b""
    for img, blob in images:
        w = img.width
        h = img.height
        # directory entry: w,h,colors,reserved,planes,bitcount,size,offset
        entries.append(struct.pack(
            "<BBBBHHII",
            w if w < 256 else 0,
            h if h < 256 else 0,
            0, 0, 1, 32, len(blob), offset,
        ))
        data += blob
        offset += len(blob)
    with open(out_path, "wb") as f:
        f.write(header + b"".join(entries) + data)


blobs = [(make(s), None) for s in SIZES]
images = [(img, png_bytes(img)) for img, _ in blobs]
out = os.path.join(ROOT, "favicon.ico")
build_ico(images, out)

d = open(out, "rb").read()
print("favicon.ico:", len(d), "bytes,", struct.unpack("<H", d[4:6])[0], "images")

# sanity: Pillow can read every entry back
ico = Image.open(out)
for i in range(struct.unpack("<H", d[4:6])[0]):
    ico.seek(i)
    print(" entry", i, ico.size, ico.format)
