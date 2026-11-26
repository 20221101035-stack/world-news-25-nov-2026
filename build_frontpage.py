#!/usr/bin/env python3
"""Build the 25 Nov 2026 world-news front page (1024x1024 PNG, <=1 MiB).

All text is composed with PIL (Liberation Sans) so nothing can come out
garbled; the only AI-generated asset is the lead photograph (burning tanker
in the Strait of Hormuz), which carries no text. Run: python3 build_frontpage.py
Writes entry.png in this directory.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (17, 17, 17)
RED = (163, 18, 30)
GREY = (74, 70, 64)
NAVY = (31, 58, 95)
TEAL = (14, 110, 110)
GREEN = (46, 110, 58)
AMBER = (176, 106, 0)
SLATE = (90, 86, 78)

F_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
F_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, f, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36
x0, x1 = MX, W - MX

# ---- Masthead ----
y = 14
f_mast = font(F_BOLD, 60)
t = 'THE WORLD TODAY'
d.text(((W - d.textlength(t, font=f_mast)) / 2, y), t, font=f_mast, fill=INK)
y += 74
d.line([(x0, y), (x1, y)], fill=INK, width=4)
y += 8
# Date band: solid red, white bold — the date must be unmissable.
d.rectangle([(x0, y), (x1, y + 44)], fill=RED)
f_date = font(F_BOLD, 25)
t = 'WEDNESDAY, 25 NOVEMBER 2026'
d.text(((W - d.textlength(t, font=f_date)) / 2, y + 8), t, font=f_date, fill=(255, 255, 255))
y += 44 + 12

# ---- Lead story: photo left, text right ----
lead = Image.open('lead-photo.webp').convert('RGB')
lw, lh = 560, 300
# Centre-crop the 1920x1280 photo to the lead box aspect.
iw, ih = lead.size
scale = max(lw / iw, lh / ih)
nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
lead = lead.resize((nw, nh), Image.LANCZOS)
cx, cy = (nw - lw) // 2, (nh - lh) // 2
lead = lead.crop((cx, cy, cx + lw, cy + lh))
img.paste(lead, (x0, y))
tx = x0 + lw + 22
tw = x1 - tx
f_kick = font(F_BOLD, 17)
d.text((tx, y + 2), 'STRAIT OF HORMUZ', font=f_kick, fill=RED)
f_h1 = font(F_BOLD, 33)
lines = wrap(d, 'TWO TANKERS HIT BY MINES, ABLAZE', f_h1, tw)
yy = draw_lines(d, lines, tx, y + 32, f_h1, INK, 40)
f_deck = font(F_REG, 18)
lines = wrap(d, 'Iran says the ships took an unauthorised route. Houthis claim a hit on '
                "Saudi Arabia's Ras Tanura refinery; a strike on a Riyadh tower injured 11.",
             f_deck, tw)
draw_lines(d, lines, tx, yy + 10, f_deck, GREY, 24)
y += lh + 12
d.line([(x0, y), (x1, y)], fill=INK, width=2)
y += 14

# ---- Grid: 3 columns x 2 rows ----
col_w = (x1 - x0 - 2 * 20) // 3
row_h = 234
f_h3 = font(F_BOLD, 21)
f_d3 = font(F_REG, 16)
f_k3 = font(F_BOLD, 15)

panels = [
    # (bar colour, kicker, headline, deck)
    (NAVY, 'SPACE',
     "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT",
     'Shenzhou-24 docks with Tiangong; Muhammad Zeeshan Ali is the first foreign '
     'astronaut aboard China\u2019s station.'),
    (RED, 'WASHINGTON',
     'HUAWEI CONVICTED ON 10 OF 12 COUNTS',
     'US jury finds the Chinese firm guilty of trade-secret theft and bank fraud; '
     'clears it of racketeering.'),
    (AMBER, 'MARKETS',
     'ASIAN STOCKS TUMBLE AS CHIP FEARS SPREAD',
     'Seoul\u2019s KOSPI plunges 6.2%, Nikkei falls 2.8%. The Dow holds above 50,000.'),
    (TEAL, 'PACIFIC',
     'SOLOMONS SIGN PACT BARRING FOREIGN BASES',
     'Treaty with Australia rules out any foreign military base on the islands.'),
    (GREEN, 'CLIMATE',
     'COP31 TALKS END WITH NO DEAL',
     'Pope Leo XIV voices concern as the UN climate summit fails to agree.'),
    (SLATE, 'IN BRIEF', None, None),
]

brief = [
    'Ukraine drones set two Russian oil refineries ablaze in Samara.',
    'Sudan: RSF drone strikes kill 19 civilians in two cities.',
    'Gaza: Israeli strike kills a Hamas security chief and his family.',
    'Libya vows retaliation for two naval officers killed in a Ukrainian sea-drone attack.',
]

for i, (bar, kick, head, deck) in enumerate(panels):
    cx = x0 + (i % 3) * (col_w + 20)
    cy = y + (i // 3) * (row_h + 12)
    d.rectangle([(cx, cy), (cx + col_w, cy + 5)], fill=bar)
    d.text((cx, cy + 13), kick, font=f_k3, fill=RED)
    if head is None:
        by = cy + 42
        f_bf = font(F_REG, 15)
        for item in brief:
            lines = wrap(d, '\u2022  ' + item, f_bf, col_w)
            by = draw_lines(d, lines, cx, by, f_bf, GREY, 19)
            by += 4
    else:
        lines = wrap(d, head, f_h3, col_w)
        yy = draw_lines(d, lines, cx, cy + 42, f_h3, INK, 26)
        lines = wrap(d, deck, f_d3, col_w)
        draw_lines(d, lines, cx, yy + 6, f_d3, GREY, 21)

y = y + 2 * row_h + 12
d.line([(x0, y), (x1, y)], fill=INK, width=2)
y += 8
f_ft = font(F_REG, 15)
t = 'THE WORLD TODAY  \u00b7  25 NOVEMBER 2026'
d.text(((W - d.textlength(t, font=f_ft)) / 2, y), t, font=f_ft, fill=GREY)
print('final content bottom y =', y + 20, 'of', H)

img.save('entry.png', optimize=True)
print('entry.png bytes:', os.path.getsize('entry.png'))
print('size:', img.size)
