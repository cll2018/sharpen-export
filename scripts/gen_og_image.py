# -*- coding: utf-8 -*-
"""Generate the default social share image (assets/img/og-default.png,
1200x630) used by og:image / twitter:image on every page that has no
product- or news-specific image.

Layout: brand-blue gradient background, Sharpen wordmark + company name +
product-line tagline on the left; a two-tile product photo collage with
rounded corners on the right.

Usage: python scripts/gen_og_image.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "og-default.jpg")
W, H = 1200, 630

BLUE = (11, 79, 138)
BLUE_DARK = (7, 58, 102)
ORANGE = (232, 119, 46)
WHITE = (255, 255, 255)
SOFT = (224, 235, 245)

BOLD = r"C:\Windows\Fonts\arialbd.ttf"
REG = r"C:\Windows\Fonts\arial.ttf"


def vgradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        base.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t)
                                    for i in range(3)))
    return base.resize((w, h))


def rounded(img, radius):
    img = img.convert("RGB")
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1],
                        radius=radius, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), mask)
    return out


def cover(img, size):
    """Center-crop img to fill size."""
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def main():
    canvas = vgradient((W, H), BLUE, BLUE_DARK).convert("RGBA")

    # right-side product collage (2 tiles)
    tile_w, tile_h, gap = 400, 260, 24
    x0 = W - tile_w - 70
    y0 = (H - (tile_h * 2 + gap)) // 2
    for i, name in enumerate(("sic-wafer.webp", "diamond-wheels.webp")):
        src = Image.open(os.path.join(ROOT, "assets", "img", name))
        tile = rounded(cover(src, (tile_w, tile_h)), 18)
        canvas.alpha_composite(tile, (x0, y0 + i * (tile_h + gap)))

    d = ImageDraw.Draw(canvas)

    # orange accent bar
    d.rectangle([70, 150, 82, 340], fill=ORANGE)

    f_word = ImageFont.truetype(BOLD, 110)
    f_tag = ImageFont.truetype(REG, 28)

    d.text((110, 165), "Sharpen", font=f_word, fill=WHITE)

    # company name auto-fitted so it never runs under the product collage
    name = "CHANGSHA SHARPEN NEW MATERIALS CO., LTD."
    size = 34
    while size > 18:
        f_name = ImageFont.truetype(BOLD, size)
        if d.textlength(name, font=f_name) <= 590:
            break
        size -= 1
    d.text((112, 308), name, font=f_name, fill=SOFT)

    # divider + tagline
    d.line([112, 380, 700, 380], fill=(255, 255, 255, 90), width=2)
    d.text((112, 410), "Diamond & CBN Grinding Wheels", font=f_tag, fill=WHITE)
    d.text((112, 455), "PM High-Speed Steel · TiNiCo Heat Spreaders",
           font=f_tag, fill=WHITE)
    d.text((112, 520), "www.sapu-cn.online", font=f_tag, fill=ORANGE)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.convert("RGB").save(OUT, format="JPEG", quality=88, optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
