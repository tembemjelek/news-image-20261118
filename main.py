#!/usr/bin/env python3
"""Sum up 18 November 2026 world news in one image.

Deterministic, Python standard library only, no network, no time,
no randomness. Draws a 1024x1024 newspaper front page and writes
it as a PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

News facts (all events of Wed 18 Nov 2026, verified from multiple
news summaries - see NOTES.md):
- Iran said it targeted US sites in Kuwait and Bahrain overnight
  after the US strike on Qeshm Island; Kuwait and Bahrain said
  they intercepted the drones. A UAE ship was hit in Hormuz:
  one sailor missing, 11 hurt.
- Xi Jinping greeted Trump on the tarmac in Shenzhen and met
  Putin, a day before the first Trump-Xi-Putin summit.
- Ukraine hit the Kerch / Crimean Bridge for a second day;
  part of the road span fell into the strait.
- Democrat Mary Peltola won Alaska's Senate seat, giving
  Democrats a 56-44 Senate majority, the AP reported.
- Nvidia beat forecasts: revenue 115.8 billion dollars, up 103
  percent; earnings 2.68 a share; outlook 130 billion dollars.
  The board said it would not reinstate Jensen Huang.
- Also that day: Ebola in DR Congo passed 11,000 cases;
  Cyclone Akvan headed for India's Andhra Pradesh coast;
  the WHO said 950,000 displaced Palestinians in Gaza were
  on flood-prone ground.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
WHITE = (255, 255, 255)
NAVY = (20, 33, 61)
NAVY2 = (31, 52, 92)
RED = (192, 57, 43)
TEAL = (15, 118, 110)
GOLD = (201, 162, 39)
BLUE = (31, 95, 140)
GREEN = (39, 110, 70)
INK = (28, 32, 40)
GREY = (92, 102, 116)
LIGHT = (226, 231, 236)
SKY = (174, 214, 241)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale if text else 0


def wrap_text(text, scale, max_width):
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                i = (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(-(thick // 2), thick // 2 + 1):
                for b in range(-(thick // 2), thick // 2 + 1):
                    self.set(x + a, y + b, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, pts, color):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)), ((x1, y1), (x2, y2)), ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by) or (yy == ymax and yy == max(ay, by)):
                    t = (yy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale, scale, scale, color)
            cx += 6 * scale
        return cx

    def text_center(self, y, s, scale, color):
        self.text((self.w - text_width(s, scale)) // 2, y, s, scale, color)

    def block(self, x, y, s, scale, color, max_width, line_h):
        lines = wrap_text(s, scale, max_width)
        yy = y
        for line in lines:
            self.text(x, yy, line, scale, color)
            yy += line_h
        return yy


def icon_ship(c, x, y, w, h):
    c.rect(x, y, w, h, NAVY2)
    c.circle(x + w - 52, y + 42, 26, GOLD)
    cx, cy = x + 58, y + 62
    for dx, dy in ((0, -34), (24, -24), (34, 0), (24, 24), (0, 34), (-24, 24), (-34, 0), (-24, -24)):
        c.line(cx, cy, cx + dx, cy + dy, RED, 5)
    c.circle(cx, cy, 12, RED)
    c.rect(x + 28, y + h - 78, w - 56, 30, WHITE)
    c.triangle(((x + 28, y + h - 78), (x + 28, y + h - 48), (x + 58, y + h - 48)), WHITE)
    c.rect(x + w // 2 - 4, y + h - 128, 8, 52, WHITE)
    c.triangle(((x + w // 2 + 4, y + h - 128), (x + w // 2 + 4, y + h - 100), (x + w // 2 + 52, y + h - 100)), RED)
    for wy in (y + h - 38, y + h - 22):
        for wx in range(x + 12, x + w - 12, 36):
            c.line(wx, wy, wx + 18, wy - 8, SKY, 3)
            c.line(wx + 18, wy - 8, wx + 36, wy, SKY, 3)


def icon_bridge(c, x, y, w, h):
    c.rect(x, y, w, h, TEAL)
    c.circle(x + w // 2, y + 24, 14, GOLD)
    deck = y + h - 34
    c.rect(x + 10, deck, w - 20, 8, WHITE)
    c.rect(x + 16, deck - 28, 10, 28, WHITE)
    c.rect(x + w - 26, deck - 28, 10, 28, WHITE)
    c.rect(x + w // 2 - 20, deck, 40, 8, RED)
    c.line(x + w // 2 - 14, deck - 16, x + w // 2 + 14, deck + 8, RED, 4)
    c.line(x + w // 2 + 14, deck - 16, x + w // 2 - 14, deck + 8, RED, 4)


def icon_jets(c, x, y, w, h):
    c.rect(x, y, w, h, BLUE)
    c.triangle(((x + 14, y + 22), (x + 14, y + 58), (x + 72, y + 40)), WHITE)
    c.triangle(((x + 62, y + 52), (x + 62, y + 80), (x + 108, y + 66)), GOLD)
    c.circle(x + w - 22, y + 22, 11, WHITE)
    c.rect(x + 12, y + h - 14, w - 24, 5, WHITE)


def icon_aid(c, x, y, w, h):
    c.rect(x, y, w, h, GREEN)
    c.rect(x + 34, y + 18, 60, 52, WHITE)
    c.rect(x + 56, y + 28, 16, 32, RED)
    c.rect(x + 46, y + 38, 36, 12, RED)
    c.rect(x + 14, y + h - 16, 34, 7, GOLD)
    c.rect(x + w - 48, y + h - 16, 34, 7, GOLD)


def icon_chart(c, x, y, w, h):
    c.rect(x, y, w, h, (122, 63, 23))
    c.line(x + 16, y + 18, x + 16, y + h - 16, WHITE, 3)
    c.line(x + 16, y + h - 16, x + w - 12, y + h - 16, WHITE, 3)
    pts = [(x + 24, y + 30), (x + 50, y + 40), (x + 76, y + 36), (x + 100, y + 58), (x + 116, y + 68)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, RED, 5)
    for (px, py) in pts:
        c.circle(px, py, 5, GOLD)


# ---------------------------------------------------------------- layout
def card(c, x, y, w, h, accent):
    c.rect(x, y, w, h, WHITE)
    c.rect(x, y, w, 8, accent)
    c.rect(x, y, w, h, GREY)  # border via thin rects below (overwritten centre)
    c.rect(x + 2, y + 2, w - 4, h - 4, WHITE)
    c.rect(x, y, w, 8, accent)


def story(c, x, y, w, h, accent, icon, kicker, headline, body):
    card(c, x, y, w, h, accent)
    icon(c, x + 14, y + 18, 128, 96)
    c.text(x + 156, y + 22, kicker, 2, accent)
    c.block(x + 156, y + 48, headline, 3, INK, w - 172, 28)
    c.block(x + 14, y + 130, body, 2, INK, w - 28, 19)


def draw():
    c = Canvas(W, H, PAPER)
    # masthead
    c.rect(0, 0, W, 128, NAVY)
    c.text_center(22, "THE WORLD IN ONE DAY", 5, WHITE)
    c.text_center(78, "WEDNESDAY 18 NOVEMBER 2026", 3, GOLD)
    c.rect(0, 128, W, 8, RED)
    # lead story
    c.rect(24, 148, 976, 282, WHITE)
    c.rect(24, 148, 976, 8, RED)
    icon_ship(c, 40, 168, 264, 246)
    c.text(324, 172, "LEAD STORY  |  GULF", 2, RED)
    c.block(324, 200, "IRAN HITS BACK AT KUWAIT AND BAHRAIN AFTER US STRIKE", 4, INK, 660, 38)
    c.block(324, 344, "IRAN SAID IT TARGETED US SITES AT ALI AL SALEM AIR BASE IN KUWAIT. BAHRAIN AND KUWAIT SAID THEY INTERCEPTED DRONES BEFORE DAWN. A UAE SHIP WAS HIT IN HORMUZ. ONE SAILOR MISSING, 11 HURT.", 2, INK, 660, 19)
    # grid, 2 x 2
    story(c, 24, 446, 476, 218, BLUE, icon_jets,
          "ASIA", "XI GREETS TRUMP IN SHENZHEN",
          "XI MET TRUMP AT THE AIRPORT AND PUTIN MET XI A DAY BEFORE THE FIRST TRUMP-XI-PUTIN SUMMIT ON THURSDAY.")
    story(c, 524, 446, 476, 218, TEAL, icon_bridge,
          "UKRAINE", "KERCH BRIDGE HIT SECOND DAY",
          "UKRAINE STRUCK THE BRIDGE AGAIN. PART OF THE ROAD SPAN FELL INTO THE STRAIT, KYIV SAID.")
    story(c, 24, 680, 476, 218, RED, icon_aid,
          "US POLITICS", "PELTOLA WINS ALASKA SENATE SEAT",
          "DEMOCRAT MARY PELTOLA BEAT DAN SULLIVAN. DEMOCRATS TAKE A 56-44 SENATE MAJORITY, AP REPORTED.")
    story(c, 524, 680, 476, 218, GREEN, icon_chart,
          "MARKETS", "NVIDIA BEATS, BOARD SAYS NO TO HUANG",
          "REVENUE 115.8 BILLION DOLLARS, UP 103 PERCENT. EARNINGS 2.68 A SHARE BEAT FORECASTS. OUTLOOK 130 BILLION DOLLARS.")
    # footer
    c.rect(0, 914, W, 110, NAVY)
    c.text_center(924, "ALSO: EBOLA IN DR CONGO PASSES 11,000 CASES", 2, WHITE)
    c.text_center(948, "CYCLONE AKVAN HEADS FOR INDIA  |  GAZA FLOOD RISK FOR 950,000", 2, WHITE)
    c.text_center(972, "SOURCES: REUTERS, BBC, AP, CNBC, UNITED NATIONS", 2, GOLD)
    c.text_center(996, "ALL EVENTS 18 NOVEMBER 2026", 2, WHITE)
    return c


# ---------------------------------------------------------------- PNG
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(c, path):
    raw = bytearray()
    for yy in range(c.h):
        raw.append(0)
        raw.extend(c.px[yy * c.w * 3:(yy + 1) * c.w * 3])
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    c = draw()
    write_png(c, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
