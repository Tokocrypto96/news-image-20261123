#!/usr/bin/env python3
"""Render THE WORLD TODAY — broadsheet front page for Monday 23 November 2026.

Draws the whole newspaper with Pillow: masthead, four main stories with
hand-drawn vector panels, and a black IN BRIEF band. Deterministic output:
no timestamps, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 18)
PAPER = (250, 247, 238)
GREY = (110, 110, 108)
RED = (178, 34, 34)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, leading, color=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, width, text, fnt, leading):
    return para(draw, x, y, width, text, fnt, leading)


def rule(draw, x, y, w, thick=3):
    draw.rectangle([x, y, x + w, y + thick], fill=INK)


def panel_climate(draw, x, y, w, h):
    """Globe over a smoking factory skyline."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 238))
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(96, 96, 96))
    # factory blocks
    draw.rectangle([x + 18, y + h - 96, x + 78, y + h - 46], fill=(70, 70, 70))
    draw.rectangle([x + 88, y + h - 116, x + 138, y + h - 46], fill=(84, 84, 84))
    draw.rectangle([x + 148, y + h - 86, x + 196, y + h - 46], fill=(70, 70, 70))
    # chimneys + smoke
    for cx in (x + 34, x + 104, x + 164):
        draw.rectangle([cx, y + h - 138, cx + 12, y + h - 90], fill=(52, 52, 52))
    for i, (sx, sy, r) in enumerate([(x + 40, y + 26, 9), (x + 62, y + 14, 12),
                                     (x + 110, y + 22, 10), (x + 132, y + 10, 13),
                                     (x + 170, y + 24, 9)]):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 148))
    # globe
    cx, cy, r = x + w - 78, y + 52, 42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(72, 130, 190),
                 outline=(30, 60, 100), width=3)
    # land masses
    draw.ellipse([cx - 30, cy - 26, cx - 2, cy + 2], fill=(46, 125, 70))
    draw.ellipse([cx + 2, cy + 4, cx + 30, cy + 30], fill=(46, 125, 70))
    draw.line([cx - r, cy, cx + r, cy], fill=(30, 60, 100), width=2)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def panel_kyiv(draw, x, y, w, h):
    """Night skyline under drone lights."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    for sx, sy in [(x + 20, y + 18), (x + 70, y + 30), (x + 130, y + 12),
                   (x + 190, y + 26), (x + 240, y + 16), (x + 280, y + 32)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 220))
    # buildings
    for bx, bw, bh in [(x + 8, 44, 66), (x + 60, 36, 92), (x + 104, 52, 78),
                       (x + 164, 40, 104), (x + 212, 48, 70), (x + 268, 34, 88)]:
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(52, 54, 74))
        for wy in range(y + h - bh + 8, y + h - 8, 14):
            for wx in range(bx + 6, bx + bw - 6, 12):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 214, 110))
    # drones: small crosses with red lights
    for dx, dy in [(x + 96, y + 34), (x + 220, y + 22), (x + 178, y + 52)]:
        draw.line([dx - 10, dy, dx + 10, dy], fill=(255, 80, 60), width=2)
        draw.line([dx, dy - 10, dx, dy + 10], fill=(255, 80, 60), width=2)
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 80, 60))
    # fire glow at a rooftop
    for r, c in [(26, (255, 120, 30)), (16, (255, 180, 60)), (8, (255, 230, 120))]:
        draw.ellipse([x + 150 - r, y + h - 104 - r, x + 150 + r, y + h - 104 + r],
                     fill=c)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def panel_hormuz(draw, x, y, w, h):
    """Tanker in a narrow strait, jets above."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 222, 236))
    # strait cliffs
    draw.polygon([(x, y + h), (x, y + 60), (x + 46, y + 78), (x + 30, y + h)],
                 fill=(150, 128, 96))
    draw.polygon([(x + w, y + h), (x + w, y + 54), (x + w - 52, y + 76),
                  (x + w - 30, y + h)], fill=(150, 128, 96))
    # sea
    draw.rectangle([x, y + h - 58, x + w, y + h], fill=(38, 96, 150))
    for wy in range(y + h - 50, y + h - 4, 12):
        draw.line([x + 8, wy, x + w - 8, wy], fill=(120, 180, 220), width=2)
    # tanker
    tx, ty = x + 52, y + h - 96
    draw.rectangle([tx, ty, tx + 190, ty + 38], fill=(150, 40, 30))
    draw.rectangle([tx + 150, ty - 26, tx + 188, ty], fill=(220, 220, 210))
    draw.rectangle([tx + 20, ty - 14, tx + 60, ty], fill=(90, 90, 88))
    draw.line([tx + 20, ty - 14, tx + 20, ty - 30], fill=(60, 60, 60), width=3)
    # jets
    for jx, jy in [(x + 60, y + 26), (x + 150, y + 16)]:
        draw.polygon([(jx, jy), (jx + 34, jy + 6), (jx, jy + 12)],
                     fill=(60, 60, 64))
        draw.line([jx, jy + 6, jx - 22, jy + 6], fill=(200, 200, 200), width=2)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def panel_robot(draw, x, y, w, h):
    """UN-blue hall with a robot silhouette and olive branches."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    # UN emblem circle
    cx, cy, r = x + w // 2, y + h // 2 + 6, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 200),
                 outline=(30, 60, 110), width=3)
    # robot head + body inside the circle
    draw.rectangle([cx - 22, cy - 30, cx + 22, cy + 2], fill=(40, 44, 52))
    draw.ellipse([cx - 18, cy - 22, cx - 6, cy - 10], fill=(255, 80, 60))
    draw.ellipse([cx + 6, cy - 22, cx + 18, cy - 10], fill=(255, 80, 60))
    draw.rectangle([cx - 26, cy + 6, cx + 26, cy + 34], fill=(40, 44, 52))
    draw.line([cx - 26, cy + 12, cx - 40, cy + 26], fill=(40, 44, 52), width=4)
    draw.line([cx + 26, cy + 12, cx + 40, cy + 26], fill=(40, 44, 52), width=4)
    # olive branches
    for s in (-1, 1):
        bx = cx + s * 66
        draw.arc([bx - 18, cy - 30, bx + 18, cy + 30], 270 if s < 0 else 90,
                 90 if s < 0 else 270, fill=(40, 110, 60), width=3)
        for k in range(4):
            ly = cy - 22 + k * 14
            draw.ellipse([bx - 4 + s * 8, ly, bx + 4 + s * 8, ly + 8],
                         fill=(40, 110, 60))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    CW = W - 2 * M  # 968

    # ---- masthead ----
    mast = SERIF_B(66)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 16), title, font=mast, fill=INK)
    rule(d, M, 96, CW, 5)
    rule(d, M, 106, CW, 1)
    sub = SANS(15)
    left = "PRICE: FREE  •  WORLD EDITION"
    right = "No. 327  •  ONE DAY, ONE WORLD"
    d.text((M, 114), left, font=sub, fill=GREY)
    rw = d.textlength(right, font=sub)
    d.text((W - M - rw, 114), right, font=sub, fill=GREY)
    date_f = SANS_B(21)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 138), date, font=date_f, fill=RED)
    rule(d, M, 168, CW, 3)

    # ---- story 1: lead, full width ----
    y = 186
    kicker = SANS_B(15)
    d.text((M, y), "CLIMATE  •  COP31, ANTALYA", font=kicker, fill=RED)
    y += 24
    h1 = SERIF_B(46)
    y = headline(d, M, y, CW, "CLIMATE TALKS COLLAPSE", h1, 52)
    y += 4
    # image panel left, text right
    px, py, pw, ph = M, y, 430, 160
    panel_climate(d, px, py, pw, ph)
    tx = M + pw + 18
    twd = W - M - tx
    body = SANS(15)
    y2 = para(d, tx, py + 2, twd,
              "COP31 climate talks have failed after the European Union and "
              "other nations rejected any deal without language on phasing "
              "out fossil fuels.", body, 22)
    y2 = para(d, tx, y2 + 8, twd,
              "Turkiye's final draft omitted the words \"fossil fuels\" "
              "entirely, leaving negotiators with no agreement to sign.",
              body, 22)
    y = py + ph + 16
    rule(d, M, y, CW, 2)
    y += 14

    # ---- stories 2-4: three columns ----
    col_w = (CW - 2 * 20) // 3
    stories = [
        ("WAR  •  UKRAINE", "DRONES HIT KYIV AS RUSSIAN SHIP BURNS",
         "At least four people were killed and 14 are missing after Russian "
         "drone strikes hit a building in the Kyiv region, President "
         "Zelenskiy said. A Russian cargo ship bound for Kaliningrad, hit "
         "by drones, is still on fire off the coast of Finland.",
         panel_kyiv),
        ("WAR  •  GULF", "GULF WAR WIDENS",
         "The Strait of Hormuz conflict has entered a crucial stage as the "
         "Iran–US war engulfs Saudi Arabia and Bahrain. Iran says it struck "
         "a US F-16; US Central Command denies the claim.",
         panel_hormuz),
        ("UNITED NATIONS", "UN TO KEEP TALKING ON KILLER ROBOTS",
         "Nations have agreed at a United Nations conference to continue "
         "negotiations on lethal autonomous weapons systems, keeping the "
         "talks on so-called killer robots alive.",
         panel_robot),
    ]
    top = y
    max_y = top
    for i, (kick, head, text, panel) in enumerate(stories):
        x = M + i * (col_w + 20)
        cy = top
        d.text((x, cy), kick, font=kicker, fill=RED)
        cy += 22
        cy = headline(d, x, cy, col_w, head, SERIF_B(24), 27)
        cy += 6
        panel(d, x, cy, col_w, 112)
        cy += 112 + 8
        cy = para(d, x, cy, col_w, text, SANS(14), 18)
        max_y = max(max_y, cy)
        if i < 2:
            d.line([x + col_w + 10, top, x + col_w + 10, max_y], fill=GREY, width=1)
    y = max_y + 14
    rule(d, M, y, CW, 2)
    y += 12

    # ---- IN BRIEF band ----
    band_h = H - M - y
    d.rectangle([M, y, W - M, y + band_h], fill=(16, 16, 16))
    bx, by = M + 16, y + 12
    d.text((bx, by), "IN BRIEF", font=SANS_B(19), fill=(255, 255, 255))
    by += 30
    briefs = [
        "Nepal PM Balendra Shah holds bilateral talks with PM Modi in New Delhi.",
        "South Korea's education minister resigns over an AI exam-cheating scandal.",
        "Seven bodies found, 50 missing after a factory fire in Indonesia.",
        "Thousands march in Lisbon as living costs fuel anger.",
        "New York Mayor-elect Mamdani announces a plan to close Rikers Island jail by 2032.",
    ]
    bf = SANS(14)
    col_bw = (CW - 32 - 20) // 2
    for i, item in enumerate(briefs):
        col = i % 2
        row = i // 2
        ix = bx + col * (col_bw + 20)
        iy = by + row * 38
        d.text((ix, iy), "•", font=SANS_B(15), fill=(255, 200, 60))
        para(d, ix + 16, iy, col_bw - 16, item, bf, 18, color=(235, 235, 235))

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
