#!/usr/bin/env python3
"""Generates every SVG in assets/ from data/desktop.json (+ data/activity.json).

Usage:  python3 scripts/build_assets.py
No third-party packages needed.
"""
import json
import os
from datetime import date, datetime
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(ROOT, "data", "desktop.json"), encoding="utf-8") as f:
    D = json.load(f)

USER = D["username"]
W = 880

# palette
BG = "#efe6d0"      # cream wallpaper
DOT = "#cbbd9b"     # wallpaper dots
WIN = "#fbf6e8"     # window body
INK = "#161512"
MUST = "#e2a929"    # mustard accent
MUST_L = "#f3d98b"
MUTED = "#6f6755"

MONO = "'SF Mono','Menlo','Consolas','DejaVu Sans Mono','Courier New',monospace"
SERIF = "Georgia,'Iowan Old Style','Times New Roman','DejaVu Serif',serif"


def e(s):
    return escape(str(s))


def svg(w, h, body, title, desc=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">\n'
        f"<title id=\"t\">{e(title)}</title><desc id=\"d\">{e(desc or title)}</desc>\n"
        f'<defs><pattern id="wall" width="8" height="8" patternUnits="userSpaceOnUse">'
        f'<rect width="8" height="8" fill="{BG}"/><circle cx="1" cy="1" r="0.8" fill="{DOT}"/></pattern>'
        f'<pattern id="stripe" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="4" height="4" fill="{WIN}"/><rect y="1" width="4" height="1" fill="{INK}"/></pattern></defs>\n'
        f'<rect width="{w}" height="{h}" fill="url(#wall)"/>\n{body}\n</svg>\n'
    )


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def text(x, y, s, size=14, fill=INK, family=MONO, weight="normal", style="normal", anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" {extra}>{e(s)}</text>'
    )


def window(x, y, w, h, title, accent=WIN, shadow=True, open_bottom=False):
    """Retro window: hard shadow, 2px border, striped title bar, close box."""
    out = []
    if shadow:
        out.append(f'<rect x="{x+5}" y="{y+5}" width="{w}" height="{h}" fill="{INK}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WIN}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="26" fill="{accent if accent != WIN else "url(#stripe)"}"/>')
    out.append(f'<line x1="{x}" y1="{y+28}" x2="{x+w}" y2="{y+28}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<rect x="{x+10}" y="{y+8}" width="12" height="12" fill="{WIN}" stroke="{INK}" stroke-width="2"/>')
    tw = len(title) * 8.4 + 24
    cx = x + w / 2
    out.append(f'<rect x="{cx-tw/2:.1f}" y="{y+5}" width="{tw:.1f}" height="19" fill="{WIN}"/>')
    out.append(text(cx, y + 19, title, 13, INK, MONO, "bold", anchor="middle"))
    # right-hand little zoom box
    out.append(f'<rect x="{x+w-24}" y="{y+8}" width="12" height="12" fill="{WIN}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<rect x="{x+w-21}" y="{y+11}" width="6" height="6" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    return "\n".join(out)


# ---------- icons (all drawn on a 64x64 grid at origin, crisp) ----------

def icon_folder(x, y, fill=MUST, s=1.0):
    return (
        f'<g transform="translate({x},{y}) scale({s})" shape-rendering="crispEdges">'
        f'<rect x="6" y="10" width="26" height="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        f'<rect x="6" y="18" width="52" height="34" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        f'<rect x="10" y="22" width="44" height="3" fill="{WIN}" opacity="0.55"/>'
        f'<rect x="8" y="54" width="52" height="3" fill="{INK}"/></g>'
    )


def icon_doc(x, y, fill=WIN, s=1.0, lines=True):
    g = (
        f'<g transform="translate({x},{y}) scale({s})" shape-rendering="crispEdges">'
        f'<path d="M12 6 H40 L52 18 V58 H12 Z" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        f'<path d="M40 6 V18 H52" fill="{MUST_L}" stroke="{INK}" stroke-width="2"/>'
    )
    if lines:
        for i, yy in enumerate((28, 35, 42, 49)):
            g += f'<rect x="18" y="{yy}" width="{28 if i < 3 else 16}" height="2" fill="{INK}"/>'
    return g + "</g>"


def icon_trash(x, y, s=1.0):
    return (
        f'<g transform="translate({x},{y}) scale({s})" shape-rendering="crispEdges">'
        f'<rect x="14" y="14" width="36" height="4" fill="{INK}"/><rect x="26" y="9" width="12" height="5" fill="{INK}"/>'
        f'<path d="M17 20 H47 L44 58 H20 Z" fill="{WIN}" stroke="{INK}" stroke-width="2"/>'
        + "".join(f'<rect x="{xx}" y="26" width="2" height="26" fill="{INK}"/>' for xx in (25, 31, 37))
        + "</g>"
    )


def icon_mac(x, y, s=1.0):
    return (
        f'<g transform="translate({x},{y}) scale({s})" shape-rendering="crispEdges">'
        f'<rect x="8" y="4" width="64" height="76" fill="{WIN}" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="16" y="12" width="48" height="40" fill="{MUST_L}" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="28" y="24" width="5" height="9" fill="{INK}"/><rect x="47" y="24" width="5" height="9" fill="{INK}"/>'
        f'<rect x="30" y="40" width="20" height="3" fill="{INK}"/><rect x="26" y="37" width="4" height="3" fill="{INK}"/>'
        f'<rect x="50" y="37" width="4" height="3" fill="{INK}"/>'
        f'<rect x="20" y="62" width="30" height="5" fill="{INK}"/><rect x="56" y="62" width="4" height="5" fill="{MUST}" stroke="{INK}" stroke-width="1.5"/>'
        f'<rect x="4" y="80" width="72" height="8" fill="{WIN}" stroke="{INK}" stroke-width="3"/></g>'
    )


# ---------- 1. menu bar ----------

def menubar():
    h = 40
    b = [f'<rect x="0" y="0" width="{W}" height="32" fill="{WIN}"/><rect y="31" width="{W}" height="2" fill="{INK}"/>']
    b.append(f'<rect x="14" y="9" width="14" height="14" fill="{MUST}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(40, 21, USER, 14, INK, MONO, "bold"))
    x = 40 + len(USER) * 8.6 + 26
    for item in ("File", "Edit", "View", "About"):
        b.append(text(x, 21, item, 14, INK, SERIF))
        x += len(item) * 9 + 24
    b.append(f'<circle cx="{W-150}" cy="16" r="5" fill="{MUST}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(W - 138, 21, D["menu_status"], 13, INK, MONO))
    write("menubar.svg", svg(W, h, "\n".join(b), f"{USER} menu bar", "Decorative retro menu bar: File, Edit, View, About."))


# ---------- 2. hello.txt ----------

def hello():
    H = 352
    x0, y0, w, h = 16, 8, W - 32, 328
    h_ = D["hello"]
    b = [window(x0, y0, w, h, "hello.txt", accent=MUST)]
    b.append(text(48, 98, h_["greeting"], 22, MUTED, SERIF, style="italic"))
    b.append(text(48, 144, h_["name"], 44, INK, SERIF, "bold"))
    for i, line in enumerate(h_["tagline"]):
        b.append(text(48, 188 + i * 30, line, 23, INK, SERIF, style="italic"))
    # dashed divider
    b.append(f'<line x1="48" y1="246" x2="{x0+w-32}" y2="246" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>')
    for i, (k, v) in enumerate(h_["info"]):
        y = 274 + i * 24
        b.append(text(48, y, k.upper().ljust(20, " ").replace(" ", " "), 13, MUTED, MONO, "bold"))
        b.append(text(48 + 22 * 8.1, y, v, 14, INK, MONO))
    b.append(f'<rect x="{48+22*8.1+len(h_["info"][0][1])*8.4+6:.0f}" y="262" width="9" height="15" fill="{INK}"/>')
    # mac + sticky note
    b.append(icon_mac(W - 250, 74, 1.7))
    sx, sy = W - 395, 92
    b.append(f'<g transform="rotate(-7 {sx+60} {sy+40})"><rect x="{sx+4}" y="{sy+4}" width="108" height="76" fill="{INK}"/>'
             f'<rect x="{sx}" y="{sy}" width="108" height="76" fill="{MUST_L}" stroke="{INK}" stroke-width="2"/>'
             + text(sx + 54, sy + 36, h_["sticky"][0], 18, INK, SERIF, "bold", anchor="middle")
             + text(sx + 54, sy + 58, h_["sticky"][1], 14, INK, SERIF, style="italic", anchor="middle") + "</g>")
    write("hello.svg", svg(W, H, "\n".join(b), "hello.txt",
          f"{h_['greeting']} {h_['name']} " + " ".join(h_["tagline"])))


# ---------- 3. desktop shortcuts (5 tiles x 176) ----------

SHORTCUTS = [
    ("about", "About Me", "who is this?", "doc"),
    ("journal", "Journal", "notes to self", "doc"),
    ("reading", "Reading", "books & tabs", "doc"),
    ("experiments", "Experiments", "tinker zone", "folder"),
    ("ideas", "Ideas That", "Didn't Work", "folder"),
]


def shortcuts():
    tw, th = 176, 128
    for key, l1, l2, kind in SHORTCUTS:
        b = []
        cx = tw / 2
        if kind == "folder":
            b.append(icon_folder(cx - 32, 14, MUST if key == "experiments" else MUST_L, 1.0))
        else:
            b.append(icon_doc(cx - 32, 14, WIN, 1.0))
        lw = max(len(l1), len(l2)) * 8 + 16
        b.append(f'<rect x="{cx-lw/2:.0f}" y="84" width="{lw}" height="36" fill="{WIN}" stroke="{INK}" stroke-width="2"/>')
        b.append(text(cx, 99, l1, 13, INK, MONO, "bold", anchor="middle"))
        b.append(text(cx, 113, l2, 11, MUTED, MONO, anchor="middle"))
        write(f"icon-{key}.svg", svg(tw, th, "\n".join(b), f"{l1} {l2}".strip(), f"Desktop shortcut: {l1} {l2}".strip()))


# ---------- 4. projects window (title / 4 tiles / footer) ----------

PROJECTS = [
    ("built", "Built", "things that run", MUST),
    ("progress", "In Progress", "work in motion", MUST_L),
    ("experiments", "Experiments", "might explode", WIN),
    ("archived", "Archived", "retired, with honour", "#d9ceb0"),
]


def projects():
    # header (title bar + path bar). Sides line up with the tiles' side borders.
    hh = 80
    b = [f'<rect x="0" y="12" width="{W}" height="{hh-12}" fill="{WIN}"/>']
    b = [f'<rect x="16" y="12" width="{W-32}" height="{hh-12}" fill="{WIN}"/>']
    b.append(window(16, 8, W - 32, hh - 8 + 40, "projects", shadow=False).replace(
        f'height="{hh-8+40}"', f'height="{hh-8}"'))
    b.append(f'<rect x="{W-15}" y="12" width="5" height="{hh-12}" fill="{INK}"/>')
    b.append(f'<rect x="17" y="37" width="{W-34}" height="{hh-37}" fill="{WIN}"/>')
    b.append(f'<line x1="16" y1="{hh-1}" x2="{W-16}" y2="{hh-1}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3"/>')
    b.append(text(34, 62, f"~/{USER}/projects", 13, MUTED, MONO))
    b.append(text(W - 34, 62, "4 folders", 13, MUTED, MONO, anchor="end"))
    write("projects-top.svg", svg(W, hh, "\n".join(b), "projects window title bar", "Projects window title bar"))

    tw, th = 220, 152
    for i, (key, l1, l2, col) in enumerate(PROJECTS):
        lx = 16 if i == 0 else 0
        rx = 16 if i == len(PROJECTS) - 1 else 0
        b = []
        b.append(f'<rect x="{lx}" y="0" width="{tw-lx-rx}" height="{th}" fill="{WIN}"/>')
        if lx:
            b.append(f'<line x1="{lx}" y1="0" x2="{lx}" y2="{th}" stroke="{INK}" stroke-width="2"/>')
        if rx:
            b.append(f'<line x1="{tw-rx}" y1="0" x2="{tw-rx}" y2="{th}" stroke="{INK}" stroke-width="2"/>')
        # shadow strip on far right tile
        if rx:
            b.append(f'<rect x="{tw-rx+1}" y="5" width="5" height="{th-5}" fill="{INK}"/>')
        cx = lx + (tw - lx - rx) / 2
        b.append(icon_folder(cx - 40, 18, col, 1.25))
        b.append(text(cx, 114, l1, 15, INK, MONO, "bold", anchor="middle"))
        b.append(text(cx, 132, l2, 12, MUTED, SERIF, style="italic", anchor="middle"))
        write(f"folder-{key}.svg", svg(tw, th, "\n".join(b), f"{l1} folder", f"Projects folder: {l1} ({l2})"))

    fh = 48
    b = [f'<rect x="16" y="0" width="{W-32}" height="{fh-8}" fill="{WIN}"/>']
    b.append(f'<rect x="{W-15}" y="0" width="5" height="{fh-3}" fill="{INK}"/>')
    b.append(f'<rect x="21" y="{fh-3}" width="{W-32}" height="5" fill="{INK}" transform="translate(0,-2)"/>')
    b.append(f'<line x1="16" y1="0" x2="16" y2="{fh-10}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<line x1="{W-16}" y1="0" x2="{W-16}" y2="{fh-10}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<line x1="16" y1="{fh-10}" x2="{W-16}" y2="{fh-10}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<line x1="16" y1="1" x2="{W-16}" y2="1" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3"/>')
    b.append(text(34, 24, "tip: tag a repo with the topic  built / in-progress / experiments / archived  to file it here.",
                  11, MUTED, MONO))
    write("projects-bottom.svg", svg(W, fh, "\n".join(b), "projects window footer", "Projects window footer"))


# ---------- 5. now learning ----------

def learning():
    rows = D["learning"]
    stages = D["stages"]
    rh = 56
    H = 8 + 28 + 56 + len(rows) * rh + 56 + 40
    H = (H + 7) // 8 * 8
    x0, y0, w = 16, 8, W - 32
    h = H - 24
    b = [window(x0, y0, w, h, "now learning.app")]
    b.append(text(48, 82, "checkpoints i update by hand. no fake percentages.", 14, MUTED, SERIF, style="italic"))
    # column headings
    b.append(text(48, 112, "TOPIC", 11, MUTED, MONO, "bold"))
    b.append(text(410, 112, "CHECKPOINT", 11, MUTED, MONO, "bold"))
    b.append(text(x0 + w - 32, 112, "STAGE", 11, MUTED, MONO, "bold", anchor="end"))
    b.append(f'<line x1="32" y1="120" x2="{x0+w-16}" y2="120" stroke="{INK}" stroke-width="1"/>')
    for i, r in enumerate(rows):
        y = 128 + i * rh
        b.append(icon_doc(30, y - 4, WIN, 0.55))
        b.append(text(72, y + 18, r["name"], 15, INK, MONO, "bold"))
        b.append(text(72, y + 36, r.get("note", ""), 12, MUTED, SERIF, style="italic"))
        for s in range(len(stages) - 1):          # 4 boxes = 4 checkpoints after "not started"
            bx = 410 + s * 34
            filled = s < r["stage"]
            b.append(f'<rect x="{bx}" y="{y+8}" width="26" height="20" fill="{MUST if filled else WIN}" stroke="{INK}" stroke-width="2"/>')
        b.append(text(x0 + w - 32, y + 24, stages[r["stage"]], 13, INK, MONO, anchor="end"))
        b.append(f'<line x1="32" y1="{y+rh-6}" x2="{x0+w-16}" y2="{y+rh-6}" stroke="{DOT}" stroke-width="1"/>')
    ly = 128 + len(rows) * rh + 8
    b.append(text(48, ly + 14, "legend:", 11, MUTED, MONO, "bold"))
    b.append(text(104, ly + 14, "  ->  ".join(stages[1:]), 11, MUTED, MONO))
    write("learning.svg", svg(W, H, "\n".join(b), "now learning",
          "Learning checkpoints: " + "; ".join(f"{r['name']} - {stages[r['stage']]}" for r in rows)))


# ---------- 6. terminal + system info (two 440px windows) ----------

def terminal_and_sysinfo():
    hw = W // 2
    th = 288
    # terminal
    b = []
    x0, y0, w, h = 16, 8, hw - 24, th - 24
    b.append(window(x0, y0, w, h, "terminal"))
    b.append(f'<rect x="{x0+1}" y="{y0+30}" width="{w-2}" height="{h-31}" fill="{INK}"/>')
    y = y0 + 58
    for kind, s in D["terminal"]:
        if kind == "cmd":
            b.append(text(x0 + 16, y, "$", 13, MUST, MONO, "bold"))
            b.append(text(x0 + 34, y, s[:40], 13, WIN, MONO))
        else:
            b.append(text(x0 + 34, y, s[:42], 13, "#b9b09a", MONO))
        y += 22
    b.append(f'<rect x="{x0+34+ (min(len(D["terminal"][-1][1]),40))*7.8+4:.0f}" y="{y-35}" width="9" height="15" fill="{MUST}"/>')
    write("terminal.svg", svg(hw, th, "\n".join(b), "terminal", "Decorative terminal window with a few playful commands."))

    # system info
    b = []
    x0, y0, w, h = 8, 8, hw - 24, th - 24
    b.append(window(x0, y0, w, h, D["sysinfo_title"]))
    b.append(icon_mac(x0 + 24, y0 + 52, 1.45))
    rx = x0 + 168
    y = y0 + 54
    for k, v in D["sysinfo"]:
        b.append(text(rx, y, k, 12, MUTED, MONO, "bold"))
        b.append(text(rx, y + 16, v[:30], 13, INK, MONO))
        y += 34
    write("sysinfo.svg", svg(hw, th, "\n".join(b), D["sysinfo_title"], "System information window, with playful descriptions."))


# ---------- 7. activity monitor ----------

def activity():
    path = os.path.join(ROOT, "data", "activity.json")
    days, synced = [], None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            j = json.load(f)
        days = j.get("days", [])
        synced = j.get("synced")
    cell, gap = 11, 3
    cols = 53
    gw = cols * (cell + gap) - gap
    H = 264
    x0, y0, w, h = 16, 8, W - 32, H - 24
    b = [window(x0, y0, w, h, "activity monitor.app")]
    gx = x0 + (w - gw) // 2
    gy = y0 + 76
    counts = [d["count"] for d in days]
    mx = max(counts) if counts else 0

    def lvl(c):
        if c <= 0 or mx == 0:
            return 0
        r = c / mx
        return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4
    shades = [WIN, "#f6e3a6", "#efc95c", MUST, "#a87408"]
    if days:
        first = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
        offset = (first.weekday() + 1) % 7      # Sunday-first rows
        for i, d in enumerate(days):
            idx = i + offset
            cx = gx + (idx // 7) * (cell + gap)
            cy = gy + (idx % 7) * (cell + gap)
            b.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" fill="{shades[lvl(d["count"])]}" stroke="{INK}" stroke-width="1"/>')
        total = sum(counts)
        b.append(text(x0 + 24, y0 + 56, f"{total} contributions in the last year", 14, INK, MONO, "bold"))
        b.append(text(x0 + w - 24, y0 + 56, f"synced {synced}", 12, MUTED, MONO, anchor="end"))
    else:
        for c in range(cols):
            for r in range(7):
                b.append(f'<rect x="{gx + c*(cell+gap)}" y="{gy + r*(cell+gap)}" width="{cell}" height="{cell}" fill="{WIN}" stroke="{DOT}" stroke-width="1"/>')
        b.append(text(x0 + 24, y0 + 56, "no data synced yet", 14, INK, MONO, "bold"))
        b.append(text(x0 + w - 24, y0 + 56, "run the 'update desktop' action once", 12, MUTED, MONO, anchor="end"))
    # legend
    lx = x0 + w - 24 - 5 * 15 - 70
    ly = y0 + h - 24
    b.append(text(lx, ly + 9, "less", 11, MUTED, MONO, anchor="end"))
    for i, s in enumerate(shades):
        b.append(f'<rect x="{lx+8+i*15}" y="{ly}" width="11" height="11" fill="{s}" stroke="{INK}" stroke-width="1"/>')
    b.append(text(lx + 8 + 5 * 15 + 4, ly + 9, "more", 11, MUTED, MONO))
    b.append(text(x0 + 24, ly + 9, "source: github contributions · real numbers only", 11, MUTED, MONO))
    write("activity.svg", svg(W, H, "\n".join(b), "activity monitor",
          "GitHub contribution heatmap for the last year" if days else "Activity monitor waiting for its first sync"))


# ---------- 8. recycle bin ----------

def recycle():
    lessons = D["recycle"]
    H = 8 + 28 + 40 + len(lessons) * 30 + 40
    H = (H + 7) // 8 * 8 + 16
    x0, y0, w, h = 16, 8, W - 32, H - 24
    b = [window(x0, y0, w, h, "recycle bin")]
    b.append(icon_trash(x0 + 26, y0 + 44, 1.7))
    b.append(text(x0 + 150, y0 + 64, "lessons salvaged from failed experiments", 15, INK, SERIF, "bold", style="italic"))
    for i, l in enumerate(lessons):
        y = y0 + 98 + i * 30
        b.append(f'<rect x="{x0+150}" y="{y-12}" width="12" height="14" fill="{WIN}" stroke="{INK}" stroke-width="2"/>')
        b.append(text(x0 + 176, y, l.replace("*", ""), 14, INK, MONO))
    write("recycle.svg", svg(W, H, "\n".join(b), "recycle bin", "Lessons: " + " ".join(lessons)))


# ---------- 9. taskbar ----------

def taskbar():
    h = 56
    b = [f'<rect y="8" width="{W}" height="40" fill="{WIN}"/><rect y="8" width="{W}" height="2" fill="{INK}"/>']
    b.append(f'<rect x="12" y="16" width="14" height="24" fill="{MUST}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(38, 33, f"{USER}.os", 14, INK, MONO, "bold"))
    b.append(text(W - 14, 33, "made by hand, with a little help · built to be edited", 12, MUTED, SERIF, style="italic", anchor="end"))
    write("taskbar.svg", svg(W, h, "\n".join(b), "taskbar", "Decorative footer bar."))


if __name__ == "__main__":
    menubar(); hello(); shortcuts(); projects(); learning()
    terminal_and_sysinfo(); activity(); recycle(); taskbar()
    print("assets built:", ", ".join(sorted(os.listdir(OUT))))
