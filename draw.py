#!/usr/bin/env python3
"""Draw entry.png: one image summing up world news of Friday 20 November 2026.

Six stories, verified against reporting dated 20 November 2026:
  1. Trump pushes the Iran war decision to 2027: "see what happens" after Jan 1.
  2. Cyclone Akvan hits Odisha; 300,000 evacuated, 423 rescue teams deployed.
  3. Anthropic shares close 17% higher on their first day of Nasdaq trading.
  4. Houthi missile damages the PIF Tower, Riyadh's tallest, home to the
     Saudi sovereign wealth fund; no injuries reported.
  5. Engine trouble forces Japan's Hayabusa2 probe to scrap its asteroid landing.
  6. Europe says it is ready to negotiate with Russia at the Berlin summit,
     but a Ukraine peace deal must come first.

Output: entry.png, 1024x1024, under 1 MiB. Run: python3 draw.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# Palette
PAPER = (246, 241, 231)
NAVY = (18, 32, 62)
NAVY2 = (28, 49, 94)
GOLD = (201, 162, 39)
INK = (22, 24, 32)
GREY = (74, 78, 88)
CARD = (255, 255, 255)
BORDER = (18, 32, 62)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(FONT_BOLD, 52)
F_KICKER = font(FONT_BOLD, 20)
F_TAG = font(FONT_BOLD, 17)
F_HEAD = font(FONT_BOLD, 25)
F_SUB = font(FONT_REG, 18)
F_FOOT = font(FONT_BOLD, 17)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(draw, cx, cy, r, color, rot=0):
    import math
    pts = []
    for i in range(10):
        ang = math.radians(rot - 90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color)


def burst(draw, cx, cy, r, color):
    """Jagged explosion burst."""
    import math, random
    random.seed(7)
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5)
        rad = r * random.uniform(0.55, 1.0)
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color)


# ---------------------------------------------------------------- panels
def panel(draw, x, y, w, h, tag, color):
    draw.rectangle([x + 3, y + 4, x + w + 3, y + h + 4], fill=(210, 204, 190))
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 32], fill=color)
    draw.text((x + 12, y + 6), tag, font=F_TAG, fill=(255, 255, 255))
    return (x, y + 32, w, 110)  # art box


def panel_text(draw, x, y, w, headline, sub):
    tx, tw = x + 14, w - 28
    lines = wrap(draw, headline, F_HEAD, tw)[:2]
    ly = y + 150
    for ln in lines:
        draw.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 30
    sub_lines = wrap(draw, sub, F_SUB, tw)[:2]
    sy = y + 212
    for ln in sub_lines:
        draw.text((tx, sy), ln, font=F_SUB, fill=GREY)
        sy += 22


# ------------------------------------------------------- panel illustrations
def art_iran(draw, bx, by, bw, bh):
    # dusk sky over the White House
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(226, 232, 244))
    draw.rectangle([bx, by + 76, bx + bw, by + bh], fill=(120, 145, 120))
    # white house: main block + portico + dome-ish roof
    draw.rectangle([bx + 150, by + 52, bx + 328, by + 100], fill=(245, 245, 240), outline=NAVY2)
    draw.rectangle([bx + 138, by + 96, bx + 340, by + 104], fill=(230, 230, 225), outline=NAVY2)
    for i in range(5):
        px = bx + 164 + i * 32
        draw.rectangle([px, by + 62, px + 12, by + 96], fill=(200, 205, 215), outline=NAVY2)
    draw.polygon([(bx + 200, by + 52), (bx + 278, by + 52), (bx + 239, by + 34)], fill=(245, 245, 240), outline=NAVY2)
    draw.ellipse([bx + 232, by + 38, bx + 246, by + 52], fill=NAVY2)
    # flag
    draw.line([bx + 392, by + 18, bx + 392, by + 96], fill=(60, 60, 60), width=3)
    for i in range(5):
        draw.rectangle([bx + 395, by + 18 + i * 6, bx + 435, by + 24 + i * 6],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([bx + 395, by + 18, bx + 415, by + 30], fill=(60, 59, 110))
    # calendar page stamped 2027
    draw.rectangle([bx + 26, by + 22, bx + 116, by + 96], fill=(255, 255, 255), outline=(150, 40, 40), width=3)
    draw.rectangle([bx + 26, by + 22, bx + 116, by + 44], fill=(150, 40, 40))
    draw.text((bx + 38, by + 50), "2027", font=font(FONT_BOLD, 26), fill=(150, 40, 40))
    draw.text((bx + 38, by + 80), "JAN 1+", font=font(FONT_BOLD, 14), fill=GREY)


def art_cyclone(draw, bx, by, bw, bh):
    # dark storm sky and sea
    draw.rectangle([bx, by, bx + bw, by + 62], fill=(70, 80, 100))
    draw.rectangle([bx, by + 62, bx + bw, by + bh], fill=(30, 70, 110))
    for wy in (72, 86, 100):
        for wx in range(0, bw, 46):
            draw.arc([bx + wx, by + wy, bx + wx + 30, by + wy + 12], 180, 360,
                     fill=(140, 200, 235), width=2)
    # spiral cyclone: concentric arcs
    cx, cy = bx + 250, by + 52
    for r, col in [(44, (255, 255, 255)), (34, (200, 220, 240)), (24, (160, 190, 220)), (14, (120, 160, 200))]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 470, fill=col, width=5)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # rain streaks
    for rx, ry in [(60, 10), (90, 26), (120, 8), (380, 12), (410, 28), (440, 10)]:
        draw.line([bx + rx, by + ry, bx + rx - 6, by + ry + 16], fill=(180, 200, 225), width=3)
    # evacuation arrow / shelter sign
    draw.rectangle([bx + 330, by + 62, bx + 452, by + 104], fill=(255, 255, 255), outline=(150, 40, 40), width=2)
    draw.text((bx + 340, by + 66), "300,000", font=font(FONT_BOLD, 18), fill=(150, 40, 40))
    draw.text((bx + 340, by + 88), "EVACUATED", font=font(FONT_BOLD, 11), fill=GREY)


def art_ipo(draw, bx, by, bw, bh):
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(232, 244, 232))
    # rising bars
    bars = [(30, 30), (80, 42), (130, 38), (180, 58), (230, 74), (280, 96)]
    for x0, hgt in bars:
        draw.rectangle([bx + x0, by + bh - 12 - hgt, bx + x0 + 34, by + bh - 12],
                       fill=(34, 139, 34))
    # trend arrow
    draw.line([(bx + 30, by + 78), (bx + 110, by + 62), (bx + 190, by + 44),
               (bx + 290, by + 14)], fill=(0, 100, 0), width=4)
    draw.polygon([(bx + 290, by + 14), (bx + 272, by + 16), (bx + 286, by + 30)], fill=(0, 100, 0))
    # ticker tag
    draw.rectangle([bx + 330, by + 18, bx + 452, by + 62], fill=NAVY)
    draw.text((bx + 344, by + 26), "ANT", font=font(FONT_BOLD, 28), fill=(255, 255, 255))
    draw.text((bx + 330, by + 68), "+17% DAY 1", font=font(FONT_BOLD, 18), fill=(0, 100, 0))


def art_riyadh(draw, bx, by, bw, bh):
    # night sky over Riyadh financial district
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(30, 34, 52))
    for sx, sy in [(40, 14), (90, 30), (150, 10), (330, 18), (420, 28), (455, 12)]:
        star(draw, bx + sx, by + sy, 3, (255, 255, 255))
    # skyline silhouettes
    for tx, tw, th in [(30, 40, 44), (80, 34, 60), (380, 44, 52), (432, 36, 66)]:
        draw.rectangle([bx + tx, by + bh - th, bx + tx + tw, by + bh], fill=(60, 66, 90))
        for wy in range(by + bh - th + 8, by + bh - 6, 12):
            draw.rectangle([bx + tx + 8, wy, bx + tx + 16, wy + 6], fill=(255, 220, 120))
    # PIF Tower: tallest, twisted top
    draw.polygon([(bx + 190, by + 6), (bx + 250, by + 6), (bx + 262, by + bh), (bx + 178, by + bh)],
                 fill=(150, 170, 200), outline=(220, 230, 240))
    for wy in range(by + 16, by + bh - 8, 14):
        draw.line([bx + 196, wy, bx + 248, wy], fill=(90, 110, 140), width=1)
    # blast + smoke on the tower
    burst(draw, bx + 292, by + 28, 26, (255, 140, 0))
    burst(draw, bx + 292, by + 28, 14, (255, 220, 60))
    draw.ellipse([bx + 304, by + 0, bx + 330, by + 22], fill=(110, 110, 110))
    draw.ellipse([bx + 322, by + 0, bx + 346, by + 16], fill=(140, 140, 140))
    # broken windows marker
    draw.rectangle([bx + 192, by + 80, bx + 252, by + 96], fill=(40, 40, 40))
    draw.text((bx + 196, by + 82), "7-8 FLRS", font=font(FONT_BOLD, 11), fill=(255, 200, 60))


def art_hayabusa(draw, bx, by, bw, bh):
    # deep space
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(12, 14, 34))
    for sx, sy in [(30, 12), (80, 40), (140, 16), (200, 60), (330, 14), (400, 44), (450, 20)]:
        star(draw, bx + sx, by + sy, 3, (255, 255, 255))
    # asteroid (grey rock, lower right)
    draw.polygon([(bx + 330, by + 60), (bx + 360, by + 44), (bx + 410, by + 48),
                  (bx + 440, by + 70), (bx + 420, by + 96), (bx + 370, by + 104),
                  (bx + 338, by + 88)], fill=(140, 130, 120), outline=(90, 84, 76))
    draw.ellipse([bx + 368, by + 60, bx + 388, by + 74], fill=(110, 102, 92))
    draw.ellipse([bx + 398, by + 76, bx + 414, by + 88], fill=(110, 102, 92))
    # probe: gold body + panels, drifting away with a red X over its path
    draw.rectangle([bx + 120, by + 40, bx + 170, by + 66], fill=(212, 175, 55), outline=(140, 110, 20))
    draw.rectangle([bx + 84, by + 46, bx + 120, by + 60], fill=(40, 90, 160))
    draw.rectangle([bx + 170, by + 46, bx + 206, by + 60], fill=(40, 90, 160))
    draw.ellipse([bx + 132, by + 26, bx + 158, by + 40], fill=(200, 200, 200), outline=(120, 120, 120))
    # dashed planned path to the asteroid, crossed out
    for i in range(8):
        px = bx + 210 + i * 16
        draw.line([px, by + 56, px + 9, by + 56], fill=(255, 255, 255), width=2)
    draw.line([bx + 250, by + 34, bx + 290, by + 74], fill=(220, 60, 40), width=4)
    draw.line([bx + 290, by + 34, bx + 250, by + 74], fill=(220, 60, 40), width=4)
    # engine warning tag
    draw.rectangle([bx + 20, by + 78, bx + 210, by + 102], fill=(150, 40, 40))
    draw.text((bx + 30, by + 83), "ENGINE TROUBLE", font=font(FONT_BOLD, 15), fill=(255, 255, 255))


def art_berlin(draw, bx, by, bw, bh):
    # conference hall
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(228, 234, 244))
    draw.rectangle([bx, by + 78, bx + bw, by + bh], fill=(90, 70, 50))
    # long table
    draw.rectangle([bx + 60, by + 72, bx + bw - 60, by + 92], fill=(120, 90, 60), outline=(70, 50, 30))
    # four flags behind the table: DE, FR, GB, UA
    def flag(px, kind):
        draw.line([px, by + 8, px, by + 72], fill=(60, 60, 60), width=3)
        fx, fy, fw, fh = px + 3, by + 10, 62, 40
        if kind == "de":
            for i, c in enumerate([(0, 0, 0), (221, 0, 0), (255, 206, 0)]):
                draw.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
        elif kind == "fr":
            for i, c in enumerate([(0, 85, 164), (255, 255, 255), (239, 65, 53)]):
                draw.rectangle([fx + i * fw / 3, fy, fx + (i + 1) * fw / 3, fy + fh], fill=c)
        elif kind == "gb":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(1, 33, 105))
            draw.line([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), width=5)
            draw.line([fx + fw, fy, fx, fy + fh], fill=(255, 255, 255), width=5)
            draw.line([fx, fy, fx + fw, fy + fh], fill=(200, 16, 46), width=2)
            draw.line([fx + fw, fy, fx, fy + fh], fill=(200, 16, 46), width=2)
            draw.line([fx + fw / 2, fy, fx + fw / 2, fy + fh], fill=(255, 255, 255), width=8)
            draw.line([fx, fy + fh / 2, fx + fw, fy + fh / 2], fill=(255, 255, 255), width=8)
            draw.line([fx + fw / 2, fy, fx + fw / 2, fy + fh], fill=(200, 16, 46), width=4)
            draw.line([fx, fy + fh / 2, fx + fw, fy + fh / 2], fill=(200, 16, 46), width=4)
        else:  # ua
            draw.rectangle([fx, fy, fx + fw, fy + fh / 2], fill=(0, 91, 187))
            draw.rectangle([fx, fy + fh / 2, fx + fw, fy + fh], fill=(255, 213, 0))
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=(90, 90, 90), width=1)
    flag(bx + 70, "de")
    flag(bx + 170, "fr")
    flag(bx + 270, "gb")
    flag(bx + 370, "ua")
    # handshake over the table: two forearms meeting in a clasp
    draw.line([bx + 150, by + 100, bx + 226, by + 62], fill=(232, 190, 160), width=13)
    draw.line([bx + 330, by + 100, bx + 254, by + 62], fill=(210, 170, 140), width=13)
    draw.ellipse([bx + 224, by + 50, bx + 256, by + 74], fill=(232, 190, 160), outline=(180, 140, 110))


# ------------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header banner
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((32, 16), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=GOLD)
    d.text((32, 46), "FRIDAY 20 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
    d.text((32, 112), "Six stories that defined the day  \u2022  Washington \u00b7 Odisha \u00b7 New York \u00b7 Riyadh \u00b7 Space \u00b7 Berlin",
           font=font(FONT_REG, 19), fill=(200, 210, 230))

    # Grid: 2 cols x 3 rows
    mx, my, gap = 24, 172, 20
    pw = (W - 2 * mx - gap) // 2          # 478
    ph = 262
    panels = [
        ("POLITICS  \u00b7  WASHINGTON", (150, 40, 40), art_iran,
         "TRUMP DEFERS IRAN DECISION",
         "War call pushed to 2027: 'see what happens after Jan 1'"),
        ("WEATHER  \u00b7  INDIA", (20, 90, 130), art_cyclone,
         "CYCLONE AKVAN HITS ODISHA",
         "300,000 evacuated; 423 rescue teams deployed"),
        ("TECH  \u00b7  NEW YORK", (20, 110, 70), art_ipo,
         "ANTHROPIC SOARS ON DEBUT",
         "Shares close 17% higher on first day of trading"),
        ("GULF  \u00b7  RIYADH", (140, 70, 20), art_riyadh,
         "MISSILE HITS RIYADH TOWER",
         "Houthi strike damages wealth fund HQ; no injuries"),
        ("SPACE  \u00b7  JAPAN", (40, 50, 110), art_hayabusa,
         "HAYABUSA2 LANDING SCRAPPED",
         "Engine trouble forces Japan's probe to change plans"),
        ("DIPLOMACY  \u00b7  BERLIN", (0, 120, 110), art_berlin,
         "EUROPE READY FOR RUSSIA TALKS",
         "Peace deal with Ukraine must come first, leaders say"),
    ]
    for i, (tag, color, art, head, sub) in enumerate(panels):
        x = mx + (i % 2) * (pw + gap)
        y = my + (i // 2) * (ph + gap)
        bx, by, bw, bh = panel(d, x, y, pw, ph, tag, color)
        art(d, bx, by, bw, bh)
        panel_text(d, x, y, pw, head, sub)

    # Footer
    d.rectangle([0, H - 26, W, H], fill=NAVY)
    d.text((32, H - 23), "EVENTS OF 20 NOVEMBER 2026, AS REPORTED THAT DAY",
           font=F_FOOT, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
