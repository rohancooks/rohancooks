"""Builds assets/*.svg for the GitHub profile README. Run: python _gen/build.py"""
import base64, io, re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

ROOT = Path(__file__).resolve().parent.parent
KIT = Path.home() / "RohanThakur-Brand-Kit"
FONTS = KIT / "05-Fonts" / "install-ttf"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
ORANGE, RED, BG = "#F16B0D", "#E61416", "#070707"

_fonts = {w: TTFont(FONTS / f"Satoshi-{w}.ttf") for w in (500, 700)}


def width(text, size, w=500, track=0.0):
    f = _fonts[w]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    adv = sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in text)
    return adv * size / upm + track * size * max(len(text) - 1, 0)


def font_face(chars, mono=False):
    css = []
    faces = (("M", 400, "GeistMono-Variable.ttf"),) if mono else (("S", 500, "Satoshi-500.ttf"), ("S", 700, "Satoshi-700.ttf"))
    for fam, w, path in faces:
        f = TTFont(FONTS / path)
        opts = Options(); opts.flavor = "woff2"; opts.layout_features = ["kern"]
        s = Subsetter(opts); s.populate(text=chars); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(css)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, chars, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{font_face(chars)}
text{{font-family:S,'Segoe UI',Helvetica,Arial,sans-serif}}{extra_css}
.up{{animation:up 1s cubic-bezier(.2,.7,.2,1) both}}
@keyframes up{{from{{opacity:0;transform:translateY(16px)}}}}
@keyframes d1{{to{{transform:translate(-140px,70px) scale(1.15)}}}}
@keyframes d2{{to{{transform:translate(120px,-60px) scale(.9)}}}}
@keyframes pulse{{50%{{opacity:.25}}}}
@keyframes sweep{{from{{transform:translateX(-400px)}}to{{transform:translateX({w}px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<radialGradient id="o"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".55"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
<radialGradient id="r"><stop offset="0" stop-color="{RED}" stop-opacity=".5"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".07"/></pattern>
<clipPath id="clip"><rect width="{w}" height="{h}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="{BG}"/>{body}</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="19.5" fill="none" stroke="#fff" stroke-opacity=".08"/>
</svg>'''


# ---------------------------------------------------------------- banner
def banner():
    W, H = 1200, 460
    logo = (KIT / "01-Logo/svg/rohanthakur-logo-white.svg").read_text(encoding="utf8")
    logo = re.search(r"<svg[^>]*>(.*)</svg>", logo, re.S).group(1)
    l1, l2 = "Your next best hire might not be a person.", "Let’s build what’s missing."
    tag = "AVAILABLE FOR NEW PROJECTS"
    foot = "AI ENGINEER  ·  CLAUDE CERTIFIED  ·  ORACLE GENAI PRO  ·  IEEE PUBLISHED"
    site = "rohanthakur.in ↗"
    body = f'''
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<circle cx="1010" cy="70" r="440" fill="url(#o)" style="animation:d1 13s ease-in-out infinite alternate"/>
<circle cx="1180" cy="470" r="380" fill="url(#r)" style="animation:d2 17s ease-in-out infinite alternate"/>
<g class="up" style="animation-delay:.1s">
  <circle cx="72" cy="62" r="5" fill="url(#g)" style="animation:pulse 2s ease-in-out infinite"/>
  <text x="88" y="67" font-size="13" font-weight="500" fill="#fff" fill-opacity=".6" letter-spacing="2.3">{tag}</text>
  <text x="{W-64}" y="67" font-size="15" font-weight="500" fill="#fff" fill-opacity=".75" text-anchor="end">{esc(site)}</text>
</g>
<g class="up" style="animation-delay:.25s"><g transform="translate(64 118) scale(1.1)">{logo}</g></g>
<text class="up" style="animation-delay:.5s" x="66" y="316" font-size="36" font-weight="500" fill="#fff" fill-opacity=".88" letter-spacing="-.5">{esc(l1)}</text>
<text class="up" style="animation-delay:.7s" x="66" y="364" font-size="36" font-weight="700" fill="url(#g)" letter-spacing="-.5">{esc(l2)}</text>
<text class="up" style="animation-delay:.9s" x="66" y="420" font-size="12.5" font-weight="500" fill="#fff" fill-opacity=".45" letter-spacing="2">{esc(foot)}</text>
<rect y="{H-3}" width="{W}" height="3" fill="url(#g)" fill-opacity=".9"/>
<rect y="{H-3}" width="400" height="3" fill="url(#shine)" style="animation:sweep 4.5s linear infinite"/>'''
    (OUT / "banner.svg").write_text(svg(W, H, body, l1 + l2 + tag + foot + site), encoding="utf8")


# ---------------------------------------------------------------- chips
def chips(x, y, items, size=14, gap=10, max_w=None, fill_first=False, accent="url(#g)"):
    out, cx, cy = [], x, y
    for i, t in enumerate(items):
        w = width(t, size) + 26
        if max_w and cx + w > x + max_w:
            cx, cy = x, cy + size + 26
        hot = fill_first and i == 0
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{size+16}" rx="{(size+16)/2}" '
                   + (f'fill="{accent}" fill-opacity=".16" stroke="{accent}"' if hot else 'fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".14"')
                   + f'/><text x="{cx+13:.1f}" y="{cy+size+3.5}" font-size="{size}" font-weight="500" fill="#fff" fill-opacity="{.95 if hot else .75}">{esc(t)}</text>')
        cx += w + gap
    return "".join(out), cy + size + 16


# ---------------------------------------------------------------- shipped-work terminal
CYAN, VIOLET, GREEN, YELLOW, PINK, AMBER = "#22d3ee", "#a78bfa", "#4ade80", "#facc15", "#f472b6", "#fb923c"
PROJECTS = [  # (repo-style name, tag, colour, what it does, stack)
    ("revenue-occupancy", "growth", CYAN, "real-time revenue + occupancy dashboard for leadership", "next.js · apps script · power bi"),
    ("ezstays-mis", "finance", VIOLET, "3 spreadsheets in → linked, drill-down P&L out", "next.js 16 · postgres · exceljs"),
    ("staff-attendance", "ops", GREEN, "selfie + GPS check-ins for on-ground staff · live", "next.js · drizzle · postgres · vercel"),
    ("lead-management", "sales", YELLOW, "enquiry → booking pipeline with DigiLocker KYC", "next.js · digilocker api"),
    ("receipt-digitiser", "ai", PINK, "WhatsApp receipt photos → validated Excel ledger", "python · gemini vision · openpyxl"),
    ("uav-wheat-ai", "research", AMBER, "drone imagery + deep learning · IEEE STCR 2025", "python · deep learning · cv"),
]
CYCLE = 16.0  # seconds; the whole session replays on a loop


def terminal():
    W, size, lh = 1200, 17, 28
    mono = TTFont(FONTS / "GeistMono-Variable.ttf")
    cw = mono["hmtx"][mono.getBestCmap()[ord("a")]][0] * size / mono["head"].unitsPerEm
    css, body, chars, n = [], [], "", [0]

    def show(at):  # keyframes: hidden until `at` s, visible until the loop resets
        n[0] += 1
        p = at / CYCLE * 100
        css.append(f"@keyframes v{n[0]}{{0%,{p:.2f}%{{opacity:0}}{p + 1.2:.2f}%,96%{{opacity:1}}100%{{opacity:0}}}}"
                   f".v{n[0]}{{animation:v{n[0]} {CYCLE}s linear infinite}}")
        return f"v{n[0]}"

    def type_on(x, y, text, start, dur):  # bg-coloured cover slides right in character steps
        n[0] += 1
        a, b, k = start / CYCLE * 100, (start + dur) / CYCLE * 100, len(text)
        css.append(f"@keyframes t{n[0]}{{0%,{a:.2f}%{{transform:translateX(0);animation-timing-function:steps({k},end)}}"
                   f"{b:.2f}%,100%{{transform:translateX({k * cw + 4:.1f}px)}}}}"
                   f".t{n[0]}{{animation:t{n[0]} {CYCLE}s infinite}}")
        return (f'<text class="m" x="{x}" y="{y}" fill="#fff">{esc(text)}</text>'
                f'<rect class="t{n[0]}" x="{x - 1}" y="{y - size}" width="{k * cw + 8:.1f}" height="{size + 8}" fill="#0b0b10"/>')

    def prompt(y, cls):
        return (f'<g class="{cls}"><text class="m" x="48" y="{y}"><tspan fill="{GREEN}">rohan</tspan>'
                f'<tspan fill="#6b7280">@</tspan><tspan fill="{CYAN}">builds</tspan><tspan fill="#6b7280"> ~ $</tspan></text></g>')

    px = 48 + 17 * cw  # where the typed command starts
    y = 104
    body.append(prompt(y, show(0.1)))
    body.append(type_on(px, y, "rohan ls --shipped", 0.6, 1.2))
    chars += "rohan@builds ~ $ ls--shipped"
    y += lh + 14
    t = 2.2
    name_x, tag_x, desc_x = 76, 76 + 19 * cw, 76 + 31 * cw
    for name, tag, col, desc, stk in PROJECTS:
        cls = show(t)
        body.append(
            f'<g class="{cls}"><circle cx="56" cy="{y - 6}" r="5" fill="{col}"/>'
            f'<text class="m" x="{name_x}" y="{y}" fill="#fff">{esc(name)}</text>'
            f'<text class="m" x="{tag_x:.1f}" y="{y}" fill="{col}">[{esc(tag)}]</text>'
            f'<text class="m" x="{desc_x:.1f}" y="{y}" fill="#d1d5db">{esc(desc)}</text>'
            f'<text class="m" x="{desc_x:.1f}" y="{y + 24}" fill="#6b7280" font-size="14">└ {esc(stk)}</text></g>')
        chars += name + tag + desc + stk + "[]└"
        y += 62
        t += 0.55
    y += 6
    body.append(prompt(y, show(t + 0.3)))
    body.append(type_on(px, y, "rohan status", t + 0.7, 0.8))
    chars += "status"
    y += lh + 6
    stats = [(GREEN, "6 systems live"), (VIOLET, "30+ hostels run on them"), (PINK, "0 hand-offs"), (YELLOW, "open to new builds")]
    x, parts = 48, []
    for col, s in stats:
        parts.append(f'<circle cx="{x + 5}" cy="{y - 6}" r="5" fill="{col}"/><text class="m" x="{x + 18}" y="{y}" fill="{col}">{esc(s)}</text>')
        x += 18 + len(s) * cw + 34
        chars += s
    body.append(f'<g class="{show(t + 1.9)}">{"".join(parts)}</g>')
    y += lh + 14
    body.append(prompt(y, show(t + 2.4)))
    body.append(f'<g class="{show(t + 2.4)}"><rect x="{px:.1f}" y="{y - size + 1}" width="{cw:.1f}" height="{size + 3}" fill="{GREEN}" style="animation:blink 1s steps(1) infinite"/></g>')
    H = y + 40

    rainbow = "".join(f'<stop offset="{i / 5:.2f}" stop-color="{c}"/>' for i, c in enumerate((CYAN, VIOLET, PINK, ORANGE, YELLOW, GREEN)))
    frame = f'''
<defs><linearGradient id="rb" x1="0" x2="1">{rainbow}</linearGradient></defs>
<rect width="{W}" height="{H}" fill="#0b0b10"/>
<rect width="{W}" height="44" fill="#14141c"/>
<rect width="{W}" height="2" fill="url(#rb)"/>
<circle cx="28" cy="23" r="7" fill="#ff5f57"/><circle cx="52" cy="23" r="7" fill="#febc2e"/><circle cx="76" cy="23" r="7" fill="#28c840"/>
<text x="{W / 2}" y="28" font-size="14" font-weight="500" fill="#fff" fill-opacity=".55" text-anchor="middle">rohan@builds — ~/shipped</text>
<circle cx="{W - 60}" cy="{H}" r="380" fill="url(#o)" fill-opacity=".35" style="animation:d2 18s ease-in-out infinite alternate"/>'''
    extra = (font_face(chars, mono=True)
             + f"text.m{{font-family:M,ui-monospace,Consolas,monospace;font-size:{size}px}}"
             + "@keyframes blink{50%{opacity:0}}" + "".join(css))
    (OUT / "work.svg").write_text(svg(W, H, frame + "".join(body), "rohan@builds — ~/shipped", extra), encoding="utf8")


# ---------------------------------------------------------------- stack
STACK = [
    ("AI & AGENTS", ["Claude Code", "Claude API", "MCP", "AI Agents", "Gemini", "Prompt Engineering", "GenAI"]),
    ("BUILD", ["TypeScript", "Next.js", "React", "Node.js", "Python", "Postgres", "Drizzle", "Tailwind", "Vercel"]),
    ("DATA & FINANCE", ["SQL", "Power BI", "Excel", "Tableau", "P&L / MIS", "Financial Modelling"]),
    ("GROWTH & DESIGN", ["GA4", "SEO / GEO", "Meta Business Suite", "Figma", "Canva", "Illustrator", "Premiere Pro"]),
]


def stack():
    W = 1200
    body, y, chars = [], 64, ""
    for (label, items), col in zip(STACK, (PINK, CYAN, VIOLET, YELLOW)):
        body.append(f'<text x="48" y="{y+20}" font-size="12.5" font-weight="700" fill="{col}" letter-spacing="2">{esc(label)}</text>')
        ch, bottom = chips(260, y, items, size=15, max_w=W - 260 - 48, fill_first=True, accent=col)
        body.append(ch)
        y = bottom + 30
        chars += label + "".join(items)
    H = y + 20
    glow = f'<circle cx="1150" cy="{H}" r="360" fill="url(#r)" style="animation:d2 16s ease-in-out infinite alternate"/>'
    (OUT / "stack.svg").write_text(svg(W, H, glow + "".join(body), chars), encoding="utf8")


if __name__ == "__main__":
    banner()
    terminal()
    stack()
    assert width("ab", 10) > 0 and (OUT / "banner.svg").stat().st_size > 1000
    print("built", sorted(p.name for p in OUT.iterdir()))
