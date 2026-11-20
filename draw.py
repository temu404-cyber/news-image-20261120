#!/usr/bin/env python3
"""Render entry.png: one picture summing up world news on Friday 20 November 2026.

The picture is a newspaper-style front page: a navy banner naming the day,
then six illustrated panels, one per story, each checked against reporting
dated 20 November 2026:

  * Washington: Trump defers the Iran war decision to 2027.
  * Odisha: Cyclone Akvan makes landfall; 300,000 people evacuated.
  * New York: Anthropic closes 17% higher on its Nasdaq debut.
  * Riyadh: a Houthi missile damages the PIF Tower; nobody hurt.
  * Space: engine trouble scraps Hayabusa2's asteroid landing.
  * Berlin: Europe offers to negotiate with Russia, peace deal first.

Everything is drawn with PIL primitives and DejaVu text; there are no
photographs and no network access. The script writes entry.png (1024x1024,
under 1 MiB). Run it with: python3 draw.py
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

IMG_W, IMG_H = 1024, 1024

# --- palette ---------------------------------------------------------------
SHEET = (246, 241, 231)
MIDNIGHT = (18, 32, 62)
STEEL = (28, 49, 94)
BRASS = (201, 162, 39)
SOOT = (22, 24, 32)
SLATE = (74, 78, 88)
CARD_WHITE = (255, 255, 255)
EDGE = (18, 32, 62)
SHADOW = (210, 204, 190)
RED = (150, 40, 40)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


TITLE_FONT = load_font(BOLD_PATH, 52)
KICKER_FONT = load_font(BOLD_PATH, 20)
TAG_FONT = load_font(BOLD_PATH, 17)
HEAD_FONT = load_font(BOLD_PATH, 25)
SUB_FONT = load_font(REG_PATH, 18)
FOOT_FONT = load_font(BOLD_PATH, 17)


def wrap_text(pen, text, fnt, max_w):
    """Split text into lines that fit max_w, breaking greedily on words."""
    out = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if pen.textlength(candidate, font=fnt) <= max_w:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_star(pen, cx, cy, radius, color, tilt=0):
    corners = []
    for step in range(10):
        angle = math.radians(tilt - 90 + step * 36)
        reach = radius if step % 2 == 0 else radius * 0.42
        corners.append((cx + reach * math.cos(angle), cy + reach * math.sin(angle)))
    pen.polygon(corners, fill=color)


def draw_burst(pen, cx, cy, radius, color):
    """Sixteen-point jagged blast, seeded so it is identical every run."""
    random.seed(7)
    corners = []
    for step in range(16):
        angle = math.radians(step * 22.5)
        reach = radius * random.uniform(0.55, 1.0)
        corners.append((cx + reach * math.cos(angle), cy + reach * math.sin(angle)))
    pen.polygon(corners, fill=color)


# --- cards -----------------------------------------------------------------
def card(pen, x, y, w, h, tag, accent):
    pen.rectangle([x + 3, y + 4, x + w + 3, y + h + 4], fill=SHADOW)
    pen.rectangle([x, y, x + w, y + h], fill=CARD_WHITE, outline=EDGE, width=2)
    pen.rectangle([x, y, x + w, y + 32], fill=accent)
    pen.text((x + 12, y + 6), tag, font=TAG_FONT, fill=CARD_WHITE)
    return x, y + 32, w, 110  # the art box below the tag band


def card_text(pen, x, y, w, headline, deck):
    left = x + 14
    width = w - 28
    line_y = y + 150
    for line in wrap_text(pen, headline, HEAD_FONT, width)[:2]:
        pen.text((left, line_y), line, font=HEAD_FONT, fill=SOOT)
        line_y += 30
    sub_y = y + 212
    for line in wrap_text(pen, deck, SUB_FONT, width)[:2]:
        pen.text((left, sub_y), line, font=SUB_FONT, fill=SLATE)
        sub_y += 22


# --- scenes, one per story -------------------------------------------------
def scene_washington(pen, ax, ay, aw, ah):
    # Dusk sky above the White House lawn.
    pen.rectangle([ax, ay, ax + aw, ay + ah], fill=(226, 232, 244))
    pen.rectangle([ax, ay + 76, ax + aw, ay + ah], fill=(120, 145, 120))
    # The White House: main block, portico base, triangular pediment.
    pen.rectangle([ax + 150, ay + 52, ax + 328, ay + 100], fill=(245, 245, 240), outline=STEEL)
    pen.rectangle([ax + 138, ay + 96, ax + 340, ay + 104], fill=(230, 230, 225), outline=STEEL)
    for col in range(5):
        px = ax + 164 + col * 32
        pen.rectangle([px, ay + 62, px + 12, ay + 96], fill=(200, 205, 215), outline=STEEL)
    pen.polygon([(ax + 200, ay + 52), (ax + 278, ay + 52), (ax + 239, ay + 34)], fill=(245, 245, 240), outline=STEEL)
    pen.ellipse([ax + 232, ay + 38, ax + 246, ay + 52], fill=STEEL)
    # Stars and stripes on a pole.
    pen.line([ax + 392, ay + 18, ax + 392, ay + 96], fill=(60, 60, 60), width=3)
    for stripe in range(5):
        pen.rectangle([ax + 395, ay + 18 + stripe * 6, ax + 435, ay + 24 + stripe * 6],
                      fill=(178, 34, 52) if stripe % 2 == 0 else CARD_WHITE)
    pen.rectangle([ax + 395, ay + 18, ax + 415, ay + 30], fill=(60, 59, 110))
    # A calendar page stamped with the deferred year.
    pen.rectangle([ax + 26, ay + 22, ax + 116, ay + 96], fill=CARD_WHITE, outline=RED, width=3)
    pen.rectangle([ax + 26, ay + 22, ax + 116, ay + 44], fill=RED)
    pen.text((ax + 38, ay + 50), "2027", font=load_font(BOLD_PATH, 26), fill=RED)
    pen.text((ax + 38, ay + 80), "JAN 1+", font=load_font(BOLD_PATH, 14), fill=SLATE)


def scene_cyclone(pen, ax, ay, aw, ah):
    # A dark storm sky above a rough sea.
    pen.rectangle([ax, ay, ax + aw, ay + 62], fill=(70, 80, 100))
    pen.rectangle([ax, ay + 62, ax + aw, ay + ah], fill=(30, 70, 110))
    for wy in (72, 86, 100):
        for wx in range(0, aw, 46):
            pen.arc([ax + wx, ay + wy, ax + wx + 30, ay + wy + 12], 180, 360,
                    fill=(140, 200, 235), width=2)
    # The cyclone itself: concentric arcs around a white eye.
    cx, cy = ax + 250, ay + 52
    for radius, shade in [(44, CARD_WHITE), (34, (200, 220, 240)), (24, (160, 190, 220)), (14, (120, 160, 200))]:
        pen.arc([cx - radius, cy - radius, cx + radius, cy + radius], 200, 470, fill=shade, width=5)
    pen.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=CARD_WHITE)
    # Slanted rain.
    for rx, ry in [(60, 10), (90, 26), (120, 8), (380, 12), (410, 28), (440, 10)]:
        pen.line([ax + rx, ay + ry, ax + rx - 6, ay + ry + 16], fill=(180, 200, 225), width=3)
    # The evacuation count on a shelter sign.
    pen.rectangle([ax + 330, ay + 62, ax + 452, ay + 104], fill=CARD_WHITE, outline=RED, width=2)
    pen.text((ax + 340, ay + 66), "300,000", font=load_font(BOLD_PATH, 18), fill=RED)
    pen.text((ax + 340, ay + 88), "EVACUATED", font=load_font(BOLD_PATH, 11), fill=SLATE)


def scene_ipo(pen, ax, ay, aw, ah):
    pen.rectangle([ax, ay, ax + aw, ay + ah], fill=(232, 244, 232))
    # A rising row of bars.
    for x0, height in [(30, 30), (80, 42), (130, 38), (180, 58), (230, 74), (280, 96)]:
        pen.rectangle([ax + x0, ay + ah - 12 - height, ax + x0 + 34, ay + ah - 12],
                      fill=(34, 139, 34))
    # The trend line climbing to the top right.
    pen.line([(ax + 30, ay + 78), (ax + 110, ay + 62), (ax + 190, ay + 44),
              (ax + 290, ay + 14)], fill=(0, 100, 0), width=4)
    pen.polygon([(ax + 290, ay + 14), (ax + 272, ay + 16), (ax + 286, ay + 30)], fill=(0, 100, 0))
    # The ticker tag and the day-one gain.
    pen.rectangle([ax + 330, ay + 18, ax + 452, ay + 62], fill=MIDNIGHT)
    pen.text((ax + 344, ay + 26), "ANT", font=load_font(BOLD_PATH, 28), fill=CARD_WHITE)
    pen.text((ax + 330, ay + 68), "+17% DAY 1", font=load_font(BOLD_PATH, 18), fill=(0, 100, 0))


def scene_riyadh(pen, ax, ay, aw, ah):
    # Night over Riyadh's financial district.
    pen.rectangle([ax, ay, ax + aw, ay + ah], fill=(30, 34, 52))
    for sx, sy in [(40, 14), (90, 30), (150, 10), (330, 18), (420, 28), (455, 12)]:
        draw_star(pen, ax + sx, ay + sy, 3, CARD_WHITE)
    # Lit windows in the shorter towers.
    for tx, tw, th in [(30, 40, 44), (80, 34, 60), (380, 44, 52), (432, 36, 66)]:
        pen.rectangle([ax + tx, ay + ah - th, ax + tx + tw, ay + ah], fill=(60, 66, 90))
        for wy in range(ay + ah - th + 8, ay + ah - 6, 12):
            pen.rectangle([ax + tx + 8, wy, ax + tx + 16, wy + 6], fill=(255, 220, 120))
    # The PIF Tower, tallest in the frame, tapering towards the top.
    pen.polygon([(ax + 190, ay + 6), (ax + 250, ay + 6), (ax + 262, ay + ah), (ax + 178, ay + ah)],
                fill=(150, 170, 200), outline=(220, 230, 240))
    for wy in range(ay + 16, ay + ah - 8, 14):
        pen.line([ax + 196, wy, ax + 248, wy], fill=(90, 110, 140), width=1)
    # The blast and the smoke drifting off the tower.
    draw_burst(pen, ax + 292, ay + 28, 26, (255, 140, 0))
    draw_burst(pen, ax + 292, ay + 28, 14, (255, 220, 60))
    pen.ellipse([ax + 304, ay + 0, ax + 330, ay + 22], fill=(110, 110, 110))
    pen.ellipse([ax + 322, ay + 0, ax + 346, ay + 16], fill=(140, 140, 140))
    # The damaged floors, marked on the facade.
    pen.rectangle([ax + 192, ay + 80, ax + 252, ay + 96], fill=(40, 40, 40))
    pen.text((ax + 196, ay + 82), "7-8 FLRS", font=load_font(BOLD_PATH, 11), fill=(255, 200, 60))


def scene_hayabusa(pen, ax, ay, aw, ah):
    # Deep space.
    pen.rectangle([ax, ay, ax + aw, ay + ah], fill=(12, 14, 34))
    for sx, sy in [(30, 12), (80, 40), (140, 16), (200, 60), (330, 14), (400, 44), (450, 20)]:
        draw_star(pen, ax + sx, ay + sy, 3, CARD_WHITE)
    # The asteroid, lower right, pitted with craters.
    pen.polygon([(ax + 330, ay + 60), (ax + 360, ay + 44), (ax + 410, ay + 48),
                 (ax + 440, ay + 70), (ax + 420, ay + 96), (ax + 370, ay + 104),
                 (ax + 338, ay + 88)], fill=(140, 130, 120), outline=(90, 84, 76))
    pen.ellipse([ax + 368, ay + 60, ax + 388, ay + 74], fill=(110, 102, 92))
    pen.ellipse([ax + 398, ay + 76, ax + 414, ay + 88], fill=(110, 102, 92))
    # The probe: a gold body, blue panels, a dish on top, drifting away.
    pen.rectangle([ax + 120, ay + 40, ax + 170, ay + 66], fill=(212, 175, 55), outline=(140, 110, 20))
    pen.rectangle([ax + 84, ay + 46, ax + 120, ay + 60], fill=(40, 90, 160))
    pen.rectangle([ax + 170, ay + 46, ax + 206, ay + 60], fill=(40, 90, 160))
    pen.ellipse([ax + 132, ay + 26, ax + 158, ay + 40], fill=(200, 200, 200), outline=(120, 120, 120))
    # The planned approach, dashed, and crossed out in red.
    for step in range(8):
        px = ax + 210 + step * 16
        pen.line([px, ay + 56, px + 9, ay + 56], fill=CARD_WHITE, width=2)
    pen.line([ax + 250, ay + 34, ax + 290, ay + 74], fill=(220, 60, 40), width=4)
    pen.line([ax + 290, ay + 34, ax + 250, ay + 74], fill=(220, 60, 40), width=4)
    # The engine warning.
    pen.rectangle([ax + 20, ay + 78, ax + 210, ay + 102], fill=RED)
    pen.text((ax + 30, ay + 83), "ENGINE TROUBLE", font=load_font(BOLD_PATH, 15), fill=CARD_WHITE)


def draw_flag(pen, px, top, kind):
    """One small flag on a pole: DE, FR, GB or UA."""
    pen.line([px, top + 8, px, top + 72], fill=(60, 60, 60), width=3)
    qx, qy, qw, qh = px + 3, top + 10, 62, 40
    if kind == "de":
        for i, shade in enumerate([(0, 0, 0), (221, 0, 0), (255, 206, 0)]):
            pen.rectangle([qx, qy + i * qh / 3, qx + qw, qy + (i + 1) * qh / 3], fill=shade)
    elif kind == "fr":
        for i, shade in enumerate([(0, 85, 164), CARD_WHITE, (239, 65, 53)]):
            pen.rectangle([qx + i * qw / 3, qy, qx + (i + 1) * qw / 3, qy + qh], fill=shade)
    elif kind == "gb":
        pen.rectangle([qx, qy, qx + qw, qy + qh], fill=(1, 33, 105))
        pen.line([qx, qy, qx + qw, qy + qh], fill=CARD_WHITE, width=5)
        pen.line([qx + qw, qy, qx, qy + qh], fill=CARD_WHITE, width=5)
        pen.line([qx, qy, qx + qw, qy + qh], fill=(200, 16, 46), width=2)
        pen.line([qx + qw, qy, qx, qy + qh], fill=(200, 16, 46), width=2)
        pen.line([qx + qw / 2, qy, qx + qw / 2, qy + qh], fill=CARD_WHITE, width=8)
        pen.line([qx, qy + qh / 2, qx + qw, qy + qh / 2], fill=CARD_WHITE, width=8)
        pen.line([qx + qw / 2, qy, qx + qw / 2, qy + qh], fill=(200, 16, 46), width=4)
        pen.line([qx, qy + qh / 2, qx + qw, qy + qh / 2], fill=(200, 16, 46), width=4)
    else:  # ua
        pen.rectangle([qx, qy, qx + qw, qy + qh / 2], fill=(0, 91, 187))
        pen.rectangle([qx, qy + qh / 2, qx + qw, qy + qh], fill=(255, 213, 0))
    pen.rectangle([qx, qy, qx + qw, qy + qh], outline=(90, 90, 90), width=1)


def scene_berlin(pen, ax, ay, aw, ah):
    # A conference hall: pale wall above a wooden floor.
    pen.rectangle([ax, ay, ax + aw, ay + ah], fill=(228, 234, 244))
    pen.rectangle([ax, ay + 78, ax + aw, ay + ah], fill=(90, 70, 50))
    # The long negotiating table.
    pen.rectangle([ax + 60, ay + 72, ax + aw - 60, ay + 92], fill=(120, 90, 60), outline=(70, 50, 30))
    # Four flags behind the table.
    for offset, kind in [(70, "de"), (170, "fr"), (270, "gb"), (370, "ua")]:
        draw_flag(pen, ax + offset, ay, kind)
    # A handshake above the table: two forearms meeting in a clasp.
    pen.line([ax + 150, ay + 100, ax + 226, ay + 62], fill=(232, 190, 160), width=13)
    pen.line([ax + 330, ay + 100, ax + 254, ay + 62], fill=(210, 170, 140), width=13)
    pen.ellipse([ax + 224, ay + 50, ax + 256, ay + 74], fill=(232, 190, 160), outline=(180, 140, 110))


# --- the six stories -------------------------------------------------------
PANELS = [
    {
        "kicker": "POLITICS  \u00b7  WASHINGTON",
        "accent": (150, 40, 40),
        "scene": scene_washington,
        "headline": "TRUMP DEFERS IRAN DECISION",
        "deck": "War call pushed to 2027: 'see what happens after Jan 1'",
    },
    {
        "kicker": "WEATHER  \u00b7  INDIA",
        "accent": (20, 90, 130),
        "scene": scene_cyclone,
        "headline": "CYCLONE AKVAN HITS ODISHA",
        "deck": "300,000 evacuated; 423 rescue teams deployed",
    },
    {
        "kicker": "TECH  \u00b7  NEW YORK",
        "accent": (20, 110, 70),
        "scene": scene_ipo,
        "headline": "ANTHROPIC SOARS ON DEBUT",
        "deck": "Shares close 17% higher on first day of trading",
    },
    {
        "kicker": "GULF  \u00b7  RIYADH",
        "accent": (140, 70, 20),
        "scene": scene_riyadh,
        "headline": "MISSILE HITS RIYADH TOWER",
        "deck": "Houthi strike damages wealth fund HQ; no injuries",
    },
    {
        "kicker": "SPACE  \u00b7  JAPAN",
        "accent": (40, 50, 110),
        "scene": scene_hayabusa,
        "headline": "HAYABUSA2 LANDING SCRAPPED",
        "deck": "Engine trouble forces Japan's probe to change plans",
    },
    {
        "kicker": "DIPLOMACY  \u00b7  BERLIN",
        "accent": (0, 120, 110),
        "scene": scene_berlin,
        "headline": "EUROPE READY FOR RUSSIA TALKS",
        "deck": "Peace deal with Ukraine must come first, leaders say",
    },
]


# --- build -----------------------------------------------------------------
def build():
    sheet = Image.new("RGB", (IMG_W, IMG_H), SHEET)
    pen = ImageDraw.Draw(sheet)

    # The banner naming the day.
    pen.rectangle([0, 0, IMG_W, 148], fill=MIDNIGHT)
    pen.rectangle([0, 148, IMG_W, 154], fill=BRASS)
    pen.text((32, 16), "THE WORLD IN ONE IMAGE", font=KICKER_FONT, fill=BRASS)
    pen.text((32, 46), "FRIDAY 20 NOVEMBER 2026", font=TITLE_FONT, fill=CARD_WHITE)
    pen.text((32, 112), "Six stories that defined the day  \u2022  Washington \u00b7 Odisha \u00b7 New York \u00b7 Riyadh \u00b7 Space \u00b7 Berlin",
           font=load_font(REG_PATH, 19), fill=(200, 210, 230))

    # A two-by-three grid of story cards.
    margin_x, margin_y, gap = 24, 172, 20
    card_w = (IMG_W - 2 * margin_x - gap) // 2          # 478
    card_h = 262
    for index, panel in enumerate(PANELS):
        x = margin_x + (index % 2) * (card_w + gap)
        y = margin_y + (index // 2) * (card_h + gap)
        ax, ay, aw, ah = card(pen, x, y, card_w, card_h, panel["kicker"], panel["accent"])
        panel["scene"](pen, ax, ay, aw, ah)
        card_text(pen, x, y, card_w, panel["headline"], panel["deck"])

    # The footer line.
    pen.rectangle([0, IMG_H - 26, IMG_W, IMG_H], fill=MIDNIGHT)
    pen.text((32, IMG_H - 23), "EVENTS OF 20 NOVEMBER 2026, AS REPORTED THAT DAY",
           font=FOOT_FONT, fill=CARD_WHITE)

    sheet.save("entry.png", optimize=True)
    print(f"wrote entry.png {sheet.size}")


if __name__ == "__main__":
    build()
