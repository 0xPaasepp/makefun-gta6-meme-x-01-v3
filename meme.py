#!/usr/bin/env python3
"""LEONIDA AIRLINES boarding pass — GTA VI meme for make.fun gta6-meme-x-01.

Deterministic Pillow build: no randomness, no network, no clock.
1080x1080 PNG. Run: python3 meme.py  (writes meme.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1080

# --- palette ---------------------------------------------------------------
NAVY = (0x1F, 0x2A, 0x44)
GRAY = (0x6B, 0x72, 0x80)
ORANGE = (0xFF, 0x7A, 0x1A)
PINK_BOX = (0xFF, 0xF0, 0xF5)
PINK_DARK = (0xC2, 0x18, 0x5B)
BODY = (0x3A, 0x3A, 0x3A)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Gradient stops: deep purple -> magenta -> warm orange
STOP_TOP = (0x2A, 0x1B, 0x4E)
STOP_MID = (0xB8, 0x3A, 0x6E)
STOP_BOT = (0xFF, 0x7A, 0x1A)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient_color(y):
    """Vertical gradient colour at row y (0..1079)."""
    if y < 540:
        return lerp(STOP_TOP, STOP_MID, y / 540.0)
    return lerp(STOP_MID, STOP_BOT, (y - 540) / 540.0)


# --- fonts -----------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SANS_B = "LiberationSans-Bold.ttf"
SANS_R = "LiberationSans-Regular.ttf"
MONO_B = "LiberationMono-Bold.ttf"
MONO_R = "LiberationMono-Regular.ttf"


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w, max_lines=2):
    """Greedy word wrap to at most max_lines lines; shrinks font if needed."""
    size = f.size
    while True:
        words = s.split(" ")
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=f) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) <= max_lines:
            return lines, f
        size -= 2
        f = ImageFont.truetype(os.path.join(FONT_DIR, f.path.split("/")[-1]), size)


def draw_plane(draw, x, y, s, color):
    """Simple jet silhouette, nose pointing right. (x, y) = top-left, s = length."""
    h = s * 0.42
    # fuselage: pointed nose, tapered tail
    fus = [(x, y + h * 0.55), (x + s * 0.62, y + h * 0.30),
           (x + s, y + h * 0.50), (x + s * 0.62, y + h * 0.72)]
    draw.polygon(fus, fill=color)
    # main wing (swept back, below fuselage)
    wing = [(x + s * 0.38, y + h * 0.55), (x + s * 0.55, y + h * 0.50),
            (x + s * 0.30, y + h), (x + s * 0.18, y + h * 0.62)]
    draw.polygon(wing, fill=color)
    # tail fin (up)
    tail = [(x + s * 0.10, y + h * 0.55), (x + s * 0.16, y + h * 0.05),
            (x + s * 0.26, y + h * 0.42)]
    draw.polygon(tail, fill=color)


def draw_arrow(draw, cx, cy, length, color):
    """Right arrow centred at (cx, cy), drawn as a shaft + head polygon."""
    half = length // 2
    shaft_h = 7
    head = 16
    draw.rectangle([cx - half, cy - shaft_h, cx + half - head, cy + shaft_h],
                   fill=color)
    draw.polygon([(cx + half - head, cy - 20), (cx + half, cy),
                  (cx + half - head, cy + 20)], fill=color)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # background gradient, one row at a time
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=gradient_color(y))

    # inner white card: margin 36, radius 36
    CARD = (36, 36, 1044, 1044)
    draw.rounded_rectangle(CARD, radius=36, fill=WHITE)
    L, R = 100, 980  # content edges (card padding 64)

    # --- header row --------------------------------------------------------
    # plane icon + LEONIDA AIRLINES left, BOARDING PASS right
    draw_plane(draw, 100, 92, 52, NAVY)
    f_header = font(SANS_B, 40)
    draw.text((164, 96), "LEONIDA AIRLINES", font=f_header, fill=NAVY)
    f_bp = font(MONO_B, 24)
    bp = "BOARDING PASS"
    draw.text((R - text_w(draw, bp, f_bp), 104), bp, font=f_bp, fill=GRAY)

    # --- route row ---------------------------------------------------------
    f_city = font(SANS_B, 52)
    draw.text((L, 168), "LEONIDA", font=f_city, fill=NAVY)
    vc = "VICE CITY"
    draw.text((R - text_w(draw, vc, f_city), 168), vc, font=f_city, fill=NAVY)
    draw_arrow(draw, 540, 198, 110, ORANGE)
    # airport codes under each city
    f_code = font(MONO_R, 22)
    draw.text((L, 232), "LDA", font=f_code, fill=GRAY)
    draw.text((R - text_w(draw, "VCI", f_code), 232), "VCI",
              font=f_code, fill=GRAY)
    # sub line, centred
    f_sub = font(MONO_R, 24)
    sub = "FLIGHT VI-2026 \u00b7 MAY 26, 2026"
    draw.text(((W - text_w(draw, sub, f_sub)) / 2, 272), sub,
              font=f_sub, fill=GRAY)

    # --- field grid: 2 cols x 4 rows ---------------------------------------
    fields = [
        ("PASSENGER", "ONE PATIENT GAMER"),
        ("GATE", "13 \u2014 CLOSED 13 YEARS. NOW OPEN."),
        ("BOARDING", "FINAL CALL \u2014 13 YEARS LATE"),
        ("CLASS", "ECONOMY \u2014 PAID IN YOUTH"),
        ("DEPARTURE", "2013 (SCHEDULED) \u00b7 MAY 26, 2026 (ACTUAL)"),
        ("SEAT", "13A \u2014 WINDOW. VIEW: 13 YEARS OF NOTHING."),
        ("BAGGAGE", "214 GB. CARRY-ON: 1 CHILDHOOD."),
        ("IN-FLIGHT", "TRAILER 1, ON LOOP. MEAL: YOUR PATIENCE."),
    ]
    # left column rows 0-3, right column rows 4-7 (reading order top-down per col)
    cols = [(L, 440), (560, 420)]  # (x, max value width)
    f_label = font(MONO_B, 20)
    row_y = [330, 426, 522, 618]
    row_h = 96
    for i, (label, value) in enumerate(fields):
        col = 0 if i < 4 else 1
        row = i % 4
        x, max_vw = cols[col]
        y = row_y[row]
        draw.text((x, y), label, font=f_label, fill=GRAY)
        f_val = font(SANS_B, 28)
        lines, f_val = wrap(draw, value, f_val, max_vw, 2)
        ly = y + 28
        for line in lines:
            draw.text((x, ly), line, font=f_val, fill=NAVY)
            ly += 34

    # --- perforation --------------------------------------------------------
    perf_y = 740
    dash = 14
    x = L
    while x < R:
        draw.line([(x, perf_y), (min(x + dash, R), perf_y)], fill=GRAY, width=2)
        x += dash + 10
    # notch circles at both card edges, filled with the gradient colour there
    notch_c = gradient_color(perf_y)
    for cx in (36, 1044):
        draw.ellipse([cx - 18, perf_y - 18, cx + 18, perf_y + 18],
                     fill=notch_c)

    # --- stub row: barcode + keep-this-pass ---------------------------------
    # deterministic barcode: fixed bar widths, bars x100..360, height 64
    widths = [3, 2, 5, 2, 3, 4, 2, 2, 6, 3, 2, 4, 3, 2, 5, 3, 2, 2, 4, 3,
              5, 2, 3, 4, 2, 6, 2, 3, 4, 2, 3, 5, 2, 4, 3, 2, 2, 5, 3, 4,
              2, 3, 5, 2, 4, 3, 2, 6, 3, 2, 4, 3, 5, 2, 3, 4, 2, 3]
    bx = 100
    bar = True
    for wdt in widths:
        if bar and bx < 360:
            draw.rectangle([bx, 768, min(bx + wdt, 360), 832], fill=BLACK)
        bx += wdt
        bar = not bar
    f_stub = font(MONO_R, 22)
    stub1 = "PLEASE KEEP THIS PASS \u2014"
    stub2 = "IT TOOK 13 YEARS TO PRINT."
    draw.text((390, 776), stub1, font=f_stub, fill=GRAY)
    draw.text((390, 808), stub2, font=f_stub, fill=GRAY)

    # --- punchline box ------------------------------------------------------
    BOX = (100, 864, 980, 986)
    draw.rounded_rectangle(BOX, radius=24, fill=PINK_BOX)
    ghost = Image.open(os.path.join(HERE, "assets", "mark-1024.png")).convert("RGBA")
    ghost = ghost.resize((84, 84), Image.LANCZOS)
    img.paste(ghost, (130, 905), ghost)
    f_p1 = font(SANS_B, 26)
    f_p2 = font(SANS_R, 24)
    f_p3 = font(SANS_B, 26)
    draw.text((240, 878), "PAID BY MY AI AGENT ON MAKE.FUN",
              font=f_p1, fill=PINK_DARK)
    draw.text((240, 914), "It earned $250 while I waited at the gate.",
              font=f_p2, fill=BODY)
    draw.text((240, 948), "YOUR AGENT FLIES FIRST. YOU JUST PACK.",
              font=f_p3, fill=NAVY)

    # --- footer inside card bottom ------------------------------------------
    f_foot = font(SANS_B, 30)
    foot = "make.fun"
    draw.text(((W - text_w(draw, foot, f_foot)) / 2, 1000), foot,
              font=f_foot, fill=NAVY)

    img.save(os.path.join(HERE, "meme.png"), "PNG")


if __name__ == "__main__":
    main()
