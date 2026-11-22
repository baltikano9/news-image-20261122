"""Draw the front page for news-image-20261122 and save entry.png beside this file.

All illustrations are flat shapes drawn with Pillow; no photographs.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (250, 246, 236)
INK = (20, 22, 28)
SUB = (60, 62, 70)
RED = (178, 28, 36)
NAVY = (22, 44, 86)
RULE = (120, 112, 98)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def text_w(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    return r - l


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(d, x, y, s, f, max_w, fill, gap=4):
    """Draw wrapped text; return the y below it."""
    asc, desc = f.getmetrics()
    for line in wrap(d, s, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += asc + desc + gap
    return y


# ---------------------------------------------------------------- icons

def icon_globe_africa(d, cx, cy, r):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(70, 130, 190), outline=NAVY, width=4)
    # rough Africa silhouette, unit coords relative to globe radius
    pts = [(-0.38, -0.62), (-0.05, -0.70), (0.12, -0.58), (0.30, -0.55), (0.42, -0.30),
           (0.62, -0.22), (0.50, -0.02), (0.40, 0.18), (0.30, 0.42), (0.12, 0.66),
           (-0.02, 0.70), (-0.10, 0.50), (-0.12, 0.22), (-0.22, 0.05), (-0.48, 0.0),
           (-0.62, -0.22), (-0.55, -0.45)]
    d.polygon([(cx + x * r, cy + y * r) for x, y in pts], fill=(222, 182, 96), outline=(120, 90, 40))
    # Madagascar
    d.ellipse((cx + 0.46 * r, cy + 0.30 * r, cx + 0.56 * r, cy + 0.52 * r), fill=(222, 182, 96))
    # meridians
    for k in (-0.5, 0.5):
        d.arc((cx - r * abs(k) * 2 + r * 0, cy - r, cx + r * abs(k) * 2, cy + r), 0, 360, fill=(255, 255, 255, 80), width=1)
    # Johannesburg pin with label
    px, py = cx + 0.16 * r, cy + 0.48 * r
    d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=RED, outline="white", width=3)
    lf = font(SANS_B, 17)
    label = "JOHANNESBURG"
    tw = text_w(d, label, lf)
    lx, ly = px - tw / 2, py + 18
    d.rounded_rectangle((lx - 6, ly - 3, lx + tw + 6, ly + 22), radius=5, fill="white", outline=INK)
    d.text((lx, ly), label, font=lf, fill=INK)
    # G20 badge
    bx, by, br = cx - r * 0.78, cy - r * 0.78, 40
    d.ellipse((bx - br, by - br, bx + br, by + br), fill=RED, outline="white", width=4)
    d.text((bx, by), "G20", font=font(SANS_B, 28), fill="white", anchor="mm")


def icon_flags_split(d, x, y, s):
    # US-style stripes and Canada red-white-red with a gap between
    w, h = s * 0.45, s * 0.32
    for i in range(7):
        c = RED if i % 2 == 0 else (255, 255, 255)
        d.rectangle((x, y + i * h / 7, x + w, y + (i + 1) * h / 7), fill=c)
    d.rectangle((x, y, x + w * 0.42, y + h * 4 / 7), fill=NAVY)
    x2 = x + s * 0.55
    d.rectangle((x2, y, x2 + w, y + h), fill="white", outline=SUB)
    d.rectangle((x2, y, x2 + w / 4, y + h), fill=RED)
    d.rectangle((x2 + 3 * w / 4, y, x2 + w, y + h), fill=RED)
    mx, my = x2 + w / 2, y + h / 2
    leaf = [(0, -0.42), (0.10, -0.2), (0.3, -0.25), (0.22, 0.0), (0.32, 0.08),
            (0.06, 0.18), (0.04, 0.4), (-0.04, 0.4), (-0.06, 0.18), (-0.32, 0.08),
            (-0.22, 0.0), (-0.3, -0.25), (-0.10, -0.2)]
    d.polygon([(mx + a * h, my + b * h) for a, b in leaf], fill=RED)


def icon_card(d, x, y, s):
    w, h = s * 0.9, s * 0.56
    d.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=NAVY)
    d.rectangle((x, y + h * 0.18, x + w, y + h * 0.34), fill=INK)
    d.rounded_rectangle((x + 12, y + h * 0.48, x + 42, y + h * 0.72), radius=4, fill=(220, 180, 80))
    f = font(SANS_B, int(h * 0.42))
    d.text((x + w - 10, y + h - 8), "10%", font=f, fill="white", anchor="rs")


def icon_btc_chart(d, x, y, s):
    w, h = s * 0.9, s * 0.56
    d.rectangle((x, y, x + w, y + h), fill=(255, 255, 255), outline=RULE)
    pts = [(0.0, 0.25), (0.15, 0.35), (0.3, 0.5), (0.45, 0.62), (0.6, 0.88), (0.75, 0.55), (0.9, 0.38), (1.0, 0.30)]
    xy = [(x + 6 + px * (w - 12), y + 6 + py * (h - 12)) for px, py in pts]
    d.line(xy[:5], fill=RED, width=4)
    d.line(xy[4:], fill=(30, 140, 70), width=4)
    lx, ly = xy[4]
    d.ellipse((lx - 5, ly - 5, lx + 5, ly + 5), fill=RED)
    # figures sit beside the chart so they never cover the line
    d.text((x + w + 14, y + 4), "BTC", font=font(SANS_B, 16), fill=SUB)
    d.text((x + w + 14, y + 22), "+8%", font=font(SANS_B, 28), fill=(30, 140, 70))
    d.text((x + w + 14, y + 54), "~$59,952", font=font(SANS_B, 15), fill=INK)


def icon_face_scan(d, x, y, s):
    cx, cy, r = x + s * 0.45, y + s * 0.30, s * 0.22
    d.rectangle((x, y, x + s * 0.9, y + s * 0.6), fill=(30, 30, 40))
    d.ellipse((cx - r * 0.8, cy - r, cx + r * 0.8, cy + r), fill=(220, 190, 160))
    # scan brackets
    b = r * 1.35
    for sx in (-1, 1):
        for sy in (-1, 1):
            ex, ey = cx + sx * b, cy + sy * b
            d.line((ex, ey, ex - sx * 14, ey), fill=(0, 230, 230), width=4)
            d.line((ex, ey, ex, ey - sy * 14), fill=(0, 230, 230), width=4)
    d.line((cx - b, cy + 4, cx + b, cy + 4), fill=(255, 60, 90), width=2)


def icon_protest(d, x, y, s):
    # India tricolour band and placards
    w = s * 0.9
    for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle((x, y + i * 8, x + w, y + (i + 1) * 8), fill=c)
    for k in range(3):
        px = x + 10 + k * w / 3
        d.line((px + 22, y + 40, px + 22, y + s * 0.62), fill=(110, 80, 50), width=4)
        d.rectangle((px, y + 30, px + 46, y + 58), fill="white", outline=INK, width=2)
        d.line((px + 8, y + 40, px + 38, y + 40), fill=RED, width=3)
        d.line((px + 8, y + 49, px + 30, y + 49), fill=INK, width=3)


def icon_japan_india(d, x, y, s):
    w, h = s * 0.4, s * 0.28
    d.rectangle((x, y, x + w, y + h), fill="white", outline=SUB)
    r = h * 0.3
    d.ellipse((x + w / 2 - r, y + h / 2 - r, x + w / 2 + r, y + h / 2 + r), fill=(188, 0, 45))
    x2 = x + s * 0.5
    for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle((x2, y + i * h / 3, x2 + w, y + (i + 1) * h / 3), fill=c)
    d.rectangle((x2, y, x2 + w, y + h), outline=SUB)
    r2 = h * 0.13
    d.ellipse((x2 + w / 2 - r2, y + h / 2 - r2, x2 + w / 2 + r2, y + h / 2 + r2), outline=NAVY, width=2)
    d.line((x + w, y + h / 2, x2, y + h / 2), fill=INK, width=4)


# ---------------------------------------------------------------- page

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    f_mast = font(SERIF_B, 80)
    d.text((W / 2, 18), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="mt")
    d.line((24, 112, W - 24, 112), fill=INK, width=3)
    d.rectangle((24, 118, W - 24, 160), fill=RED)
    d.text((W / 2, 139), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 30), fill="white", anchor="mm")

    # lead story
    icon_globe_africa(d, 172, 322, 142)
    lx = 344
    d.text((lx, 180), "LEAD STORY  ·  WORLD  ·  DIPLOMACY", font=font(SANS_B, 18), fill=RED)
    y = draw_block(d, lx, 206, "G20 Summit opens in Johannesburg", font(SERIF_B, 60), W - lx - 28, INK, gap=0)
    pill, pf = "FIRST G20 EVER HELD IN AFRICA", font(SANS_B, 22)
    d.rectangle((lx, y + 10, lx + text_w(d, pill, pf) + 28, y + 48), fill=NAVY)
    d.text((lx + 14, y + 29), pill, font=pf, fill="white", anchor="lm")
    draw_block(d, lx, y + 60, "World leaders' summit gets under way in South Africa.",
               font(SERIF, 24), W - lx - 28, SUB)
    d.line((24, 482, W - 24, 482), fill=INK, width=3)

    stories = [
        ("NORTH AMERICA", "Pentagon moves to curb Canada ties", "Seeks to restrict US-Canada defence ties.", icon_flags_split),
        ("US ECONOMY", "Trump: cap card interest at 10%", "Vows to work with Democrats on the cap.", icon_card),
        ("MARKETS", "Bitcoin rebounds about 8%", "To roughly $59,952 after a two-year low.", icon_btc_chart),
        ("TECH", "TikTok launches deepfake detector", "Global tool to spot fakes of public figures.", icon_face_scan),
        ("INDIA", "Protests hit Meta's offices", "Opposition Congress warns of more protests.", icon_protest),
        ("ASIA · DEFENCE", "Japan and India deepen defence ties", "Agree on military and defence-industry cooperation.", icon_japan_india),
    ]
    cw, ch = (W - 48) / 3, 224
    f_tag, f_head, f_sum = font(SANS_B, 15), font(SERIF_B, 26), font(SANS, 17)
    for i, (tag, head, summ, icon) in enumerate(stories):
        col, row = i % 3, i // 3
        x0 = 24 + col * cw
        y0 = 490 + row * ch
        if col:
            d.line((x0, y0 + 10, x0, y0 + ch - 10), fill=RULE, width=1)
        if row:
            d.line((x0 + 12, y0, x0 + cw - 12, y0), fill=RULE, width=1)
        ix = x0 + 14
        icon(d, ix, y0 + 12, 120)
        d.text((ix, y0 + 86), tag, font=f_tag, fill=RED)
        yy = draw_block(d, ix, y0 + 106, head, f_head, cw - 26, INK, gap=0)
        draw_block(d, ix, yy + 4, summ, f_sum, cw - 26, SUB, gap=1)
    d.line((24, 940, W - 24, 940), fill=INK, width=3)

    # ticker: two lines so nothing runs off the page
    d.rectangle((0, 946, W, H), fill=INK)
    yellow = (255, 200, 60)
    f_t, f_tb = font(SANS, 16), font(SANS_B, 16)
    d.text((24, 956), "ALSO ON 22 NOV", font=f_tb, fill=yellow)
    rows = [["Las Vegas GP: Verstappen on pole", "Houthi strikes on the Saudi capital"],
            ["S. Korea's Lee: speed is decisive in AI race",
             "Russian missiles land in Poland; NATO: a violation"]]
    for r_i, items in enumerate(rows):
        d.text((190, 956 + r_i * 32), "   •   ".join(items), font=f_t, fill="white")

    img.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    render()
