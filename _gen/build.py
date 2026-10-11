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


def font_face(chars):
    css = []
    for w, path in ((500, "Satoshi-500.ttf"), (700, "Satoshi-700.ttf")):
        f = TTFont(FONTS / path)
        opts = Options(); opts.flavor = "woff2"; opts.layout_features = ["kern"]
        s = Subsetter(opts); s.populate(text=chars); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:S;font-weight:{w};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(css)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, chars):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{font_face(chars)}
text{{font-family:S,'Segoe UI',Helvetica,Arial,sans-serif}}
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
def chips(x, y, items, size=14, gap=10, max_w=None, fill_first=False):
    out, cx, cy = [], x, y
    for i, t in enumerate(items):
        w = width(t, size) + 26
        if max_w and cx + w > x + max_w:
            cx, cy = x, cy + size + 26
        hot = fill_first and i == 0
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{size+16}" rx="{(size+16)/2}" '
                   + ('fill="url(#g)" fill-opacity=".14" stroke="url(#g)"' if hot else 'fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".14"')
                   + f'/><text x="{cx+13:.1f}" y="{cy+size+3.5}" font-size="{size}" font-weight="500" fill="#fff" fill-opacity="{.95 if hot else .75}">{esc(t)}</text>')
        cx += w + gap
    return "".join(out), cy + size + 16


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("Revenue & Occupancy", "GROWTH · BUSINESS INTELLIGENCE",
     ["Live revenue and occupancy intelligence across", "30+ student hostels and ~6,700 beds."],
     ["SQL", "Python", "Power BI", "Forecasting"]),
    ("EzStays MIS", "FINANCE · BUSINESS SYSTEMS",
     ["Monthly P&L engine: three spreadsheets in, a linked,", "drill-down management income statement out."],
     ["Next.js 16", "TypeScript", "Postgres", "ExcelJS"]),
    ("Staff Attendance App", "OPERATIONS · WEB APP",
     ["Selfie + GPS attendance and daily work tracking", "for on-ground hostel staff. Live in production."],
     ["Next.js", "Drizzle", "Postgres", "Vercel"]),
    ("Lead Management System", "SALES · CRM · KYC",
     ["Enquiry-to-booking pipeline with DigiLocker KYC,", "so no lead or document slips through."],
     ["Next.js", "DigiLocker API", "CRM"]),
    ("AI Receipt Digitiser", "AI · AUTOMATION",
     ["WhatsApp receipt photos in, a validated Excel", "ledger out. Hours of data entry, gone."],
     ["Python", "Gemini", "Vision OCR", "openpyxl"]),
    ("UAV Wheat Disease AI", "AI / ML · IEEE PUBLISHED",
     ["Drone imagery + deep learning to catch wheat", "disease early. Published at IEEE STCR 2025."],
     ["Deep Learning", "Computer Vision", "Python"]),
]


def card(i, title, tag, desc, stack):
    W, H = 600, 300
    glow = "o" if i % 2 == 0 else "r"
    num = f"{i+1:02d}"
    ch, _ = chips(36, 228, stack, size=13)
    body = f'''
<circle cx="{560 if i % 2 == 0 else 600}" cy="0" r="300" fill="url(#{glow})" style="animation:d{1 + i % 2} {12 + i}s ease-in-out infinite alternate"/>
<text x="36" y="54" font-size="15" font-weight="700" fill="url(#g)">{num}</text>
<text x="70" y="54" font-size="12" font-weight="500" fill="#fff" fill-opacity=".5" letter-spacing="1.8">{esc(tag)}</text>
<text x="{W-36}" y="56" font-size="20" font-weight="500" fill="#fff" fill-opacity=".45" text-anchor="end">↗</text>
<text x="34" y="116" font-size="34" font-weight="700" fill="#fff" letter-spacing="-.8">{esc(title)}</text>
<text x="36" y="156" font-size="16.5" font-weight="500" fill="#fff" fill-opacity=".62">{esc(desc[0])}</text>
<text x="36" y="182" font-size="16.5" font-weight="500" fill="#fff" fill-opacity=".62">{esc(desc[1])}</text>
{ch}'''
    chars = title + tag + "".join(desc) + "".join(stack) + num + "↗"
    (OUT / f"work-{num}.svg").write_text(svg(W, H, body, chars), encoding="utf8")


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
    for label, items in STACK:
        body.append(f'<text x="48" y="{y+20}" font-size="12.5" font-weight="700" fill="url(#g)" letter-spacing="2">{esc(label)}</text>')
        ch, bottom = chips(260, y, items, size=15, max_w=W - 260 - 48, fill_first=True)
        body.append(ch)
        y = bottom + 30
        chars += label + "".join(items)
    H = y + 20
    glow = f'<circle cx="1150" cy="{H}" r="360" fill="url(#r)" style="animation:d2 16s ease-in-out infinite alternate"/>'
    (OUT / "stack.svg").write_text(svg(W, H, glow + "".join(body), chars), encoding="utf8")


if __name__ == "__main__":
    banner()
    for i, p in enumerate(PROJECTS):
        card(i, *p)
    stack()
    assert width("ab", 10) > 0 and (OUT / "banner.svg").stat().st_size > 1000
    print("built", sorted(p.name for p in OUT.iterdir()))
