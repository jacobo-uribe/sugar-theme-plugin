#!/usr/bin/env python3
"""Look closer at a screenshot, or put two side by side.

    python3 zoom.py crop  IMAGE X0 Y0 X1 Y1 [--scale 3] [--out OUT.png]
    python3 zoom.py grid  IMAGE [--step 100] [--out OUT.png]
    python3 zoom.py side  LEFT RIGHT [--out OUT.png]

crop  cuts the box (pixels from the top-left) and enlarges it, so small text, borders,
      padding and icon strokes become readable.
grid  draws a labelled pixel grid over the image so you can read coordinates and
      measure gaps before cropping.
side  scales two images to the same width and joins them left/right, for comparing a
      reference against a clone.

Needs Pillow: python3 -m pip install --user pillow
"""
import argparse
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is not installed. Run: python3 -m pip install --user pillow")


def crop(a):
    im = Image.open(a.image)
    box = im.crop((a.x0, a.y0, a.x1, a.y1))
    box = box.resize((box.width * a.scale, box.height * a.scale), Image.LANCZOS)
    out = a.out or f"crop-{a.x0}-{a.y0}-{a.x1}-{a.y1}.png"
    box.save(out)
    print(f"{out}  {box.width}x{box.height}  (x{a.scale} of {a.x1 - a.x0}x{a.y1 - a.y0})")


def grid(a):
    im = Image.open(a.image).convert("RGB")
    d = ImageDraw.Draw(im)
    for x in range(0, im.width, a.step):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0), width=1)
        d.text((x + 2, 2), str(x), fill=(255, 0, 0))
    for y in range(0, im.height, a.step):
        d.line([(0, y), (im.width, y)], fill=(255, 0, 0), width=1)
        d.text((2, y + 2), str(y), fill=(255, 0, 0))
    out = a.out or "grid.png"
    im.save(out)
    print(f"{out}  {im.width}x{im.height}  grid every {a.step}px")


def side(a):
    l, r = Image.open(a.left).convert("RGB"), Image.open(a.right).convert("RGB")
    w = min(l.width, r.width)
    l = l.resize((w, round(l.height * w / l.width)), Image.LANCZOS)
    r = r.resize((w, round(r.height * w / r.width)), Image.LANCZOS)
    gap = 16
    out_im = Image.new("RGB", (w * 2 + gap, max(l.height, r.height)), (255, 255, 255))
    out_im.paste(l, (0, 0))
    out_im.paste(r, (w + gap, 0))
    out = a.out or "side-by-side.png"
    out_im.save(out)
    print(f"{out}  {out_im.width}x{out_im.height}  left={a.left} right={a.right}")


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("crop"); c.add_argument("image"); [c.add_argument(n, type=int) for n in ("x0", "y0", "x1", "y1")]
c.add_argument("--scale", type=int, default=3); c.add_argument("--out"); c.set_defaults(fn=crop)
g = sub.add_parser("grid"); g.add_argument("image"); g.add_argument("--step", type=int, default=100); g.add_argument("--out"); g.set_defaults(fn=grid)
s = sub.add_parser("side"); s.add_argument("left"); s.add_argument("right"); s.add_argument("--out"); s.set_defaults(fn=side)
args = p.parse_args()
args.fn(args)
