"""Static site builder for J.P. Fernando & Sons.

    python src/build.py

Writes the finished pages to the repository root (assets in ./assets are kept).
Pages keep the original WordPress URLs (e.g. /ropes/pp/).
"""
import html
import json
import urllib.parse
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa: E402,F401,F403

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_BY_SLUG = {c["slug"]: c for c in CATEGORIES}

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
ICON = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    "chev": '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m2 4 4 4 4-4"/></svg>',
    "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" width="16" height="16"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>',
    "knot": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 12h6m8 0h6M8 12a4 4 0 1 0 8 0 4 4 0 1 0-8 0"/><path d="M10 9.5 14 14.5M14 9.5l-4 5"/></svg>',
    "anchor": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="24" cy="9" r="4"/><path d="M24 13v29M14 20h20M6 28c0 8 8 14 18 14s18-6 18-14M6 28l4 3M42 28l-4 3"/></svg>',
    "mesh": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 4h40M4 4l10 12L24 4l10 12L44 4M14 16 4 28l10 12 10-12-10-12Zm20 0L24 28l10 12 10-12-10-12ZM24 28 14 40M24 28l10 12"/></svg>',
    "island": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M22 4c6 2 12 9 14 17s-1 17-8 21c-4 2-9 1-12-3-4-5-6-12-5-20 1-6 5-13 11-15Z"/><circle cx="20" cy="30" r="2"/><path d="M4 44h40"/></svg>',
}

SOCIAL_ICON = {
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.3a22 22 0 0 0-2.5-.1c-2.5 0-4.2 1.5-4.2 4.3v2.3H7.4V14h2.7v8z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.5 9h3.3v10.5H4.5zM6.1 3.8a1.9 1.9 0 1 1 0 3.8 1.9 1.9 0 0 1 0-3.8M10 9h3.2v1.4h.1c.4-.8 1.5-1.7 3.1-1.7 3.3 0 3.9 2.2 3.9 5v5.8h-3.3v-5.1c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7v5.2H10z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.2 3.5h3l-6.6 7.6 7.8 9.4h-6.1l-4.8-5.9-5.5 5.9h-3l7-7.9-7.5-9.1h6.3l4.3 5.4zm-1 15.2h1.6L7.9 5.2H6.1z"/></svg>',
    "pinterest": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.8 9.8 0 0 0-3.6 18.9c-.1-.8-.1-2 0-2.8l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.5 1.8-2.5.9 0 1.3.7 1.3 1.4 0 .9-.6 2.2-.8 3.4-.3 1 .5 1.9 1.5 1.9 1.8 0 3.2-1.9 3.2-4.7 0-2.4-1.8-4.1-4.3-4.1-2.9 0-4.6 2.2-4.6 4.4 0 .9.3 1.8.8 2.3l.1.4-.3 1.1c0 .2-.2.3-.4.2-1.3-.6-2.1-2.5-2.1-4 0-3.3 2.4-6.3 6.9-6.3 3.6 0 6.4 2.6 6.4 6 0 3.6-2.3 6.5-5.4 6.5-1.1 0-2.1-.6-2.4-1.2l-.7 2.5c-.2.9-.9 2.1-1.3 2.8A9.8 9.8 0 1 0 12 2.2"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.6 2.6 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.6 2.6 0 0 0 2.4 7.2 27 27 0 0 0 2 12a27 27 0 0 0 .4 4.8 2.6 2.6 0 0 0 1.8 1.8c1.6.4 7.8.4 7.8.4s6.2 0 7.8-.4a2.6 2.6 0 0 0 1.8-1.8A27 27 0 0 0 22 12a27 27 0 0 0-.4-4.8M10 15V9l5.2 3z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5a9.4 9.4 0 0 0-8.1 14.2L2.6 21.4l4.8-1.3A9.4 9.4 0 1 0 12 2.5m0 17.1c-1.4 0-2.8-.4-4-1.1l-.3-.2-2.8.8.8-2.8-.2-.3A7.7 7.7 0 1 1 12 19.6m4.2-5.8c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.3 6.3 0 0 1-3.1-2.7c-.2-.4.2-.4.7-1.3.1-.1 0-.3 0-.4l-.7-1.7c-.2-.4-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11 11 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1-.1-.2-.2-.2-.5-.4"/></svg>',
}
SOCIAL_LABEL = {"facebook": "Facebook", "instagram": "Instagram", "linkedin": "LinkedIn", "x": "X", "pinterest": "Pinterest", "youtube": "YouTube", "whatsapp": "WhatsApp"}


def social_profiles():
    """(key, label, href) for every social network. href is None while the
    profile URL in content.SOCIAL is still empty (icon shows, link pending)."""
    out = []
    for key, val in SOCIAL.items():
        if not val:
            out.append((key, SOCIAL_LABEL[key], None))
            continue
        href = f"https://wa.me/{val}" if key == "whatsapp" else val
        out.append((key, SOCIAL_LABEL[key], href))
    return out


def link_attrs(href, label):
    """Anchor attributes: a real external link, or an inert placeholder until the URL is added."""
    if href:
        return f'href="{e(href)}" target="_blank" rel="noopener" aria-label="{e(label)}"'
    return f'role="link" aria-disabled="true" aria-label="{e(label)} (link coming soon)" title="{e(label)} — link coming soon"'


def social_row(cls=""):
    links = "".join(
        f'<a class="srow__a srow__a--{k}" {link_attrs(h, l)}>{SOCIAL_ICON[k]}</a>'
        for k, l, h in social_profiles())
    return f'<div class="srow {cls}">{links}</div>' if links else ""


e = html.escape


def rel(page, target):
    """Relative URL from page path (e.g. 'ropes/pp/') to target path."""
    depth = len([p for p in page.split("/") if p])
    prefix = "../" * depth
    if target == "":
        return prefix or "./"
    return prefix + target


def img_size(name):
    """Read pixel size of a JPEG/PNG/WebP in assets/img (stdlib only)."""
    import struct
    path = os.path.join(ROOT, "assets", "img", name)
    with open(path, "rb") as f:
        b = f.read()
    if b[:8] == bytes.fromhex("89504e470d0a1a0a"):
        return struct.unpack(">II", b[16:24])
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        if b[12:16] == b"VP8X":
            return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
        if b[12:16] == b"VP8L":
            v = int.from_bytes(b[21:25], "little")
            return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
        return struct.unpack("<HH", b[26:30])
    i = 2
    while i < len(b):
        if b[i] != 0xFF:
            i += 1
            continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


def img(page, name, alt, cls="", loading="lazy", w=None, h=None, extra=""):
    if not (w and h):
        wh = img_size(name)
        if wh:
            w, h = wh
    size = f' width="{w}" height="{h}"' if w and h else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{rel(page, "assets/img/" + name)}" alt="{e(alt)}"{c} loading="{loading}" decoding="async"{size}{extra}>'


def tag(rows, brand=None, dark=False, cls=""):
    out = [f'<div class="tag{" tag--dark" if dark else ""} {cls}" aria-hidden="true">']
    if brand:
        out.append(f'<div class="tag__brand">{brand}</div>')
    for k, v in rows:
        out.append(f'<span class="tag__k label">{e(k)}</span><span class="tag__v">{e(v)}</span>')
    out.append("</div>")
    return "".join(out)


def add_btn(page, pid, name, lg=False):
    return (f'<button type="button" class="add-btn{" add-btn--lg" if lg else ""}" data-id="{pid}" data-name="{e(name)}" '
            f'data-contact="{rel(page, "contact-us/")}#enquiry" aria-pressed="false">{ICON["plus"]}<span class="add-btn__t">Add to enquiry</span></button>')


def all_items():
    """Every product item (categories + product pages) for selects / hub."""
    items = []
    for c in CATEGORIES:
        items.append((c["slug"], c["name"]))
        for ch in c["children"]:
            p = PRODUCTS[ch]
            items.append((p["slug"], f'{c["name"]} — {p["name"]}'))
    return items


def years():
    return date.today().year - FOUNDED


# --------------------------------------------------------------------------
# layout
# --------------------------------------------------------------------------
def head(page, title, desc, og_img="banner.jpg", schema=None):
    canonical = SITE + page
    full_title = title if title.startswith(NAME) else f"{title} | {NAME}"
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b1a2b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}assets/img/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel(page, 'assets/img/favicon.png')}" type="image/png">
<link rel="apple-touch-icon" href="{rel(page, 'assets/img/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=Instrument+Serif:ital@0;1&family=Noto+Sans+Sinhala:wght@400;600&family=Noto+Sans+Tamil:wght@400;600&display=swap">
<link rel="stylesheet" href="{rel(page, 'assets/css/main.css')}">
{ld}
</head>
"""


def header(page, dark=False):
    def cur(target):
        if target == page or (target != "" and page.startswith(target)):
            return ' aria-current="page"'
        return ""

    products_current = any(page.startswith(c["slug"]) for c in CATEGORIES) or page == "products/"
    mega_items = "".join(
        f'<li><a href="{rel(page, c["slug"])}">{img(page, c["img"], "", w=52, h=52)}'
        f'<div><strong>{e(c["name"])}</strong><span>{e(c["blurb"][:58].rsplit(" ", 1)[0])}…</span></div></a></li>'
        for c in CATEGORIES)
    drawer_sub = "".join(f'<a href="{rel(page, c["slug"])}">{e(c["name"])}</a>' for c in CATEGORIES)
    phone = PHONES[0]
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr{' hdr--dark' if dark else ''}">
  <div class="wrap hdr__in">
    <a class="brand" href="{rel(page, '')}" aria-label="{e(NAME)} — home">
      {img(page, 'logo.webp', '', loading='eager')}
      <span class="brand__name">J.P. Fernando <em>&amp;</em> Sons<small>Colombo · Since 1953</small></span>
    </a>
    <nav class="nav" aria-label="Main">
      <a class="nav__link" href="{rel(page, '')}"{' aria-current="page"' if page == '' else ''}>Home</a>
      <div class="nav__item">
        <button class="nav__link" type="button" aria-expanded="false" aria-controls="mega"{' aria-current="page"' if products_current else ''}>Products {ICON['chev']}</button>
        <div class="mega" id="mega">
          <ul class="mega__list">{mega_items}</ul>
          <a class="mega__feature" href="{rel(page, 'products/')}">
            {img(page, 'ropes.jpg', '')}
            <span class="label">Full range</span>
            <span class="h3">Browse every product</span>
            <span class="link-arrow">All products {ICON['arrow']}</span>
          </a>
        </div>
      </div>
      <a class="nav__link" href="{rel(page, 'brands/')}"{cur('brands/')}>Brands</a>
      <a class="nav__link" href="{rel(page, 'about-us/')}"{cur('about-us/')}>About</a>
      <a class="nav__link" href="{rel(page, 'contact-us/')}"{cur('contact-us/')}>Contact</a>
    </nav>
    <div class="hdr__actions">
      <a class="hdr__call" href="tel:{phone[1]}">{ICON['phone']}<span>{phone[0]}</span></a>
      <a class="qbtn" href="{rel(page, 'contact-us/')}#enquiry">{ICON['list']}<span class="qbtn__label">Enquiry list</span><span class="qbtn__count" data-count="0">0</span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <nav class="drawer__main" aria-label="Mobile">
    <a href="{rel(page, '')}">Home</a>
    <a href="{rel(page, 'products/')}">Products</a>
    <a href="{rel(page, 'brands/')}">Brands</a>
    <a href="{rel(page, 'about-us/')}">About us</a>
    <a href="{rel(page, 'contact-us/')}">Contact</a>
  </nav>
  <div class="drawer__sub">{drawer_sub}</div>
  <div class="drawer__foot">
    <a href="tel:{phone[1]}">{phone[0]}</a>
    <a href="https://wa.me/{MOBILE[1].lstrip("+")}" target="_blank" rel="noopener">WhatsApp {MOBILE[0]}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span>{', '.join(ADDRESS)}</span>
    {social_row("srow--drawer")}
  </div>
</div>
<main id="main">
"""


def cta_band(page, title="Tell us what <em>you need.</em>", text="Send us the product, size and quantity — we'll come back with availability and a quotation."):
    return f"""<section class="cta-band">
  <div class="mesh-bg"></div>
  <div class="wrap cta-band__in">
    <h2 class="cta-band__t" data-split>{title}</h2>
    <div class="cta-band__a" data-reveal>
      <p>{text}</p>
      <a class="btn" href="{rel(page, 'contact-us/')}#enquiry">Request a quotation {ICON['arrow']}</a>
      <a class="btn btn--ghost" href="tel:{PHONES[0][1]}">{ICON['phone']} Call {PHONES[0][0]}</a>
    </div>
  </div>
</section>
"""


def quickbar():
    """Floating quick-access bar on the left edge (desktop and tablet)."""
    items = [
        ("call", "Call " + PHONES[0][0], f"tel:{PHONES[0][1]}", ICON["phone"], False),
        ("mail", "Email us", f"mailto:{EMAIL}", ICON["mail"], False),
        ("map", "Find us on the map", MAP_URL, ICON["pin"], True),
    ]
    links = "".join(
        f'<li><a class="qa qa--{k}" href="{h}"{' target="_blank" rel="noopener"' if ext else ''} aria-label="{e(l)}">'
        f'<span class="qa__i">{icon}</span><span class="qa__l">{e(l)}</span></a></li>'
        for k, l, h, icon, ext in items)
    links += "".join(
        f'<li><a class="qa qa--{k}" {link_attrs(h, l)}><span class="qa__i">{SOCIAL_ICON[k]}</span>'
        f'<span class="qa__l">{e(l) if h else e(l) + " — soon"}</span></a></li>'
        for k, l, h in social_profiles())
    return f'<nav class="qbar" aria-label="Quick access"><ul>{links}</ul></nav>'


def footer(page, with_cta=True):
    cats = "".join(f'<li><a href="{rel(page, c["slug"])}">{e(c["name"])}</a></li>' for c in CATEGORIES)
    phones = "".join(f'<li><a href="tel:{t}">{d}</a> <span style="opacity:.6">· {l}</span></li>' for d, t, l in PHONES)
    hours = "".join(f"<li>{d}: {h}</li>" for d, h in HOURS)
    return f"""{cta_band(page) if with_cta else ''}
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div>
        <a class="brand" href="{rel(page, '')}">{img(page, 'logo.webp', '')}<span class="brand__name">J.P. Fernando <em>&amp;</em> Sons</span></a>
        <p>Manufacturers, importers and distributors of nylon and cotton fishing nets, twines, lines and fishing accessories. Colombo, since {FOUNDED}.</p>
        <p class="ftr__si" lang="si">{NAME_SI}</p>
        <p class="ftr__si ftr__ta" lang="ta">{NAME_TA}</p>
        {social_row("srow--footer")}
      </div>
      <div>
        <h3 class="label">Products</h3>
        <ul>{cats}</ul>
      </div>
      <div>
        <h3 class="label">Company</h3>
        <ul>
          <li><a href="{rel(page, 'about-us/')}">About us</a></li>
          <li><a href="{rel(page, 'brands/')}">Brands</a></li>
          <li><a href="{rel(page, 'products/')}">All products</a></li>
          <li><a href="{rel(page, 'contact-us/')}">Contact &amp; enquiries</a></li>
        </ul>
        <h3 class="label" style="margin-top:28px">Opening hours</h3>
        <ul>{hours}</ul>
      </div>
      <div>
        <h3 class="label">Visit &amp; call</h3>
        <address style="font-style:normal">{'<br>'.join(ADDRESS)}</address>
        <ul style="margin-top:14px">{phones}<li><a href="tel:{MOBILE[1]}">{MOBILE[0]}</a> <span style="opacity:.6">· Mobile</span></li><li><a href="https://wa.me/{MOBILE[1].lstrip("+")}" target="_blank" rel="noopener">WhatsApp {MOBILE[0]}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
      </div>
    </div>
    <div class="ftr__big" aria-hidden="true">Since {FOUNDED}</div>
    <div class="ftr__bot">
      <span>© {date.today().year} {e(NAME)}. All rights reserved.</span>
      <span>287/1 Sea Street, Colombo 11 · Sri Lanka</span>
    </div>
  </div>
</footer>
{quickbar()}
<div class="mbar" aria-label="Quick contact">
  <a href="tel:{PHONES[0][1]}">{ICON['phone']} Call</a>
  <a class="mbar__wa" href="https://wa.me/{MOBILE[1].lstrip("+")}" target="_blank" rel="noopener" aria-label="WhatsApp {MOBILE[0]}">{SOCIAL_ICON['whatsapp']} WhatsApp</a>
  <a href="{rel(page, 'contact-us/')}#enquiry">Get a quote</a>
</div>
<div class="toast" role="status" aria-live="polite"><span></span><a href="#" hidden>View list</a></div>
<script src="{rel(page, 'assets/js/main.js')}" defer></script>
</body>
</html>
"""


def enquiry_form(page, compact=False, dark=False):
    opts = "".join(f'<option value="{e(n)}">{e(n)}</option>' for _, n in all_items())
    buyer = "".join(
        f'<input type="radio" name="buyer" id="b-{i}-{"c" if compact else "f"}" value="{v}"{" checked" if i == 0 else ""}><label for="b-{i}-{"c" if compact else "f"}">{v}</label>'
        for i, v in enumerate(["Trade / wholesale buyer", "Fisherman or angler", "Government / tender", "Other"]))
    full = "" if compact else f"""
      <div class="field"><label for="f-email">Email <span class="opt">(optional)</span></label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="f-company">Company / organisation <span class="opt">(optional)</span></label><input id="f-company" name="company" autocomplete="organization"></div>
      <div class="field field--full"><label for="f-qty">Quantity and sizes <span class="opt">(optional)</span></label><input id="f-qty" name="quantity" placeholder="e.g. 20 bundles, 2 mm twine, 1.5 inch mesh"></div>"""
    sfx = "c" if compact else "f"
    endpoint = FORM_ENDPOINT or ("https://api.web3forms.com/submit" if FORM_ACCESS_KEY else "")
    note = ("We reply during business hours, Monday to Saturday." if endpoint
            else f"Pressing send opens your email app with this enquiry ready to go to {EMAIL}.")
    return f"""<form class="form{' on-dark' if dark else ''}" data-enquiry data-endpoint="{e(endpoint)}" data-access-key="{e(FORM_ACCESS_KEY)}" novalidate>
      <div aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden"><label>Leave this empty<input name="botcheck" tabindex="-1" autocomplete="off"></label></div>
      <fieldset class="field field--full" style="border:0;padding:0;margin:0">
        <legend class="label" style="margin-bottom:12px">I am a</legend>
        <div class="seg">{buyer}</div>
      </fieldset>
      <div class="field"><label for="{sfx}-name">Your name</label><input id="{sfx}-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="{sfx}-phone">Phone</label><input id="{sfx}-phone" name="phone" type="tel" required autocomplete="tel" inputmode="tel"></div>{full}
      <div class="field field--full"><label for="{sfx}-interest">Product of interest <span class="opt">(optional)</span></label>
        <select id="{sfx}-interest" name="interest"><option value="">Choose a product…</option>{opts}<option value="Something else">Something else</option></select></div>
      <div class="form__list"><span class="label">Your enquiry list</span><ul></ul></div>
      <div class="field field--full"><label for="{sfx}-msg">What do you need?</label><textarea id="{sfx}-msg" name="message" required rows="4" placeholder="Tell us the product, size and quantity you're looking for."></textarea></div>
      <div class="form__actions">
        <button class="btn{' btn--buoy' if dark else ''}" type="submit">Send enquiry {ICON['arrow']}</button>
        <p class="form__note">{note} Prefer to talk? Call <a href="tel:{PHONES[0][1]}" style="text-decoration:underline">{PHONES[0][0]}</a>.</p>
      </div>
      <div class="form__status" role="status" aria-live="polite"></div>
    </form>"""


def crumbs(page, trail):
    items = [f'<li><a href="{rel(page, "")}">Home</a></li>']
    for name, target in trail:
        items.append(f'<li><a href="{rel(page, target)}">{e(name)}</a></li>' if target is not None else f'<li aria-current="page">{e(name)}</li>')
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs" style="list-style:none;padding:0;margin:0 0 26px">{"".join(items)}</ol></nav>'


def write(page, content):
    path = os.path.join(ROOT, *[p for p in page.split("/") if p], "index.html") if page != "404" else os.path.join(ROOT, "404.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def render_body(page, blocks):
    out = []
    for kind, val in blocks:
        if kind == "p":
            out.append(f"<p>{val}</p>")
        elif kind == "p.big":
            out.append(f'<p class="big">{val}</p>')
        elif kind == "h2":
            out.append(f"<h2>{val}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{val}</h3>")
        elif kind == "ul":
            out.append('<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in val) + "</ul>")
    return "\n".join(out)


def gallery(page, items):
    cells = "".join(
        f'<figure class="gallery__item" tabindex="0" role="button" aria-label="Enlarge: {e(alt)}" data-reveal style="--d:{i*0.06:.2f}s;margin:0">'
        f'{img(page, f, alt)}<figcaption>{e(alt)}</figcaption></figure>'
        for i, (f, alt) in enumerate(items))
    return f"""<div class="gallery-wrap"><div class="gallery" tabindex="0" aria-label="Image gallery — scroll sideways">{cells}</div>
<div class="gallery-nav"><button type="button" class="gnav" data-dir="-1" aria-label="Previous images">&larr;</button><button type="button" class="gnav" data-dir="1" aria-label="Next images">&rarr;</button></div></div>
<dialog class="lightbox"><button class="lightbox__close" type="button" aria-label="Close">×</button><img src="" alt=""><p></p></dialog>"""


def side_card(page, name, pid, ask):
    asks = "".join(f"<li>{e(a)}</li>" for a in ask)
    return f"""<aside class="side-card on-dark" data-reveal>
  <span class="label" style="color:#7fc8bd">Enquire about this range</span>
  <h2 class="h3">Ask for availability &amp; price</h2>
  <p>Add this product to your enquiry list, or contact us directly. We sell wholesale and retail, so trade, tender and individual buyers are all welcome.</p>
  {add_btn(page, pid, name, lg=True).replace('class="add-btn add-btn--lg"', 'class="add-btn add-btn--lg" style="width:100%;justify-content:center;color:var(--paper)"')}
  <a class="btn btn--buoy" href="{rel(page, 'contact-us/')}?product={e(name)}#enquiry">Request a quote {ICON['arrow']}</a>
  <a class="btn btn--ghost" href="tel:{PHONES[0][1]}">{ICON['phone']} {PHONES[0][0]}</a>
  <div class="side-card__ask"><span class="label">Helpful to include</span><ul style="margin-top:10px">{asks}</ul></div>
</aside>"""


def related(page, exclude_slug):
    others = [c for c in CATEGORIES if c["slug"] != exclude_slug][:4]
    cards = "".join(
        f'<a class="rel" href="{rel(page, c["slug"])}" data-reveal style="--d:{i*0.08:.2f}s">{img(page, c["img"], "")}'
        f'<span class="rel__t"><span class="label">0{CATEGORIES.index(c)+1}</span>{e(c["name"])}</span></a>'
        for i, c in enumerate(others))
    return f"""<section class="sec sec--tight">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow label">Keep exploring</span><h2 class="h2">More from the <em>range</em></h2></div>
    <div><a class="link-arrow" href="{rel(page, 'products/')}">All products {ICON['arrow']}</a></div></div>
    <div class="related">{cards}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def schema_org():
    return {
        "@context": "https://schema.org", "@type": "Store", "name": NAME, "url": SITE,
        "logo": SITE + "assets/img/logo.png", "image": SITE + "assets/img/banner.jpg",
        "foundingDate": str(FOUNDED), "email": EMAIL,
        "telephone": [p[0] for p in PHONES] + [MOBILE[0]],
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS[0], "addressLocality": "Colombo 11", "addressCountry": "LK"},
        "openingHours": ["Mo-Fr 09:00-17:00", "Sa 09:00-13:00"],
        "description": "Manufacturers, importers and distributors of nylon and cotton fishing nets, twines, lines and fishing accessories in Sri Lanka since 1953.",
    }


def page_home():
    p = ""
    ticker_items = "".join(f'<a class="ticker__item" href="{rel(p, c["slug"])}">{e(c["name"])}</a>' for c in CATEGORIES) + \
        '<span class="ticker__item">TORAY Japan yarn</span><span class="ticker__item">Island-wide distribution</span>'
    explorer_items = ""
    explorer_imgs = ""
    for i, c in enumerate(CATEGORIES):
        k = c["slug"].strip("/")
        explorer_items += f"""<li class="explorer__item" data-key="{k}">
      <a href="{rel(p, c['slug'])}">
        <span class="explorer__idx num">0{i+1}</span>
        <span class="explorer__name">{e(c['name'])}</span>
        <span class="explorer__go">{ICON['arrow']}</span>
        <span class="explorer__desc">{e(c['blurb'])}</span>
        <span class="explorer__thumb">{img(p, c['img'], '')}</span>
      </a></li>"""
        explorer_imgs += f'<div class="explorer__img{" cover" if c["fit"] == "cover" else ""}" data-key="{k}">{img(p, c["img"], c["name"])}</div>'

    brand_cells = "".join(
        f'<a class="brand-cell" href="{rel(p, "brands/")}" data-reveal style="--d:{i*0.06:.2f}s">{img(p, b["img"], b["name"] + " logo")}<span class="brand-cell__name label">{e(b["where"])}</span></a>'
        for i, b in enumerate(BRANDS))

    body = f"""{head(p, NAME + " — Fishing nets, ropes & lines since 1953", f"Sri Lanka's pioneer importer and distributor of nylon fishing nets since {FOUNDED}. SuperCatch nets made from TORAY Japan yarn, HDPE nets, ropes, lines, twine and fishing accessories. Colombo 11.", schema=schema_org())}
{header(p)}
<section class="hero">
  <div class="hero__net"></div>
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <span class="eyebrow label" data-reveal>Sea Street, Colombo · Est. {FOUNDED}</span>
      <h1 class="h1 hero__title" data-split>Nets, ropes &amp; lines for Sri Lanka's <em>fishing fleet.</em></h1>
      <p class="lede hero__lede" data-reveal style="--d:.5s">The country's pioneer importer and distributor of nylon fishing nets — now making our own SuperCatch nets from TORAY Japan yarn, and supplying fishing communities across the island.</p>
      <div class="hero__ctas" data-reveal style="--d:.65s">
        <a class="btn" href="{rel(p, 'products/')}">Explore the range {ICON['arrow']}</a>
        <a class="btn btn--ghost" href="{rel(p, 'contact-us/')}#enquiry">Request a quote</a>
      </div>
      <p class="hero__si" data-reveal style="--d:.8s"><span lang="si">{NAME_SI}</span> · <span lang="ta" class="ta">{NAME_TA}</span></p>
    </div>
    <div class="hero__visual" data-reveal="scale" style="--d:.3s">
      {img(p, 'ropes-cut.webp', 'Coils of SuperCatch fishing rope in blue, green, red, yellow and white', 'hero__ropes', loading='eager', w=938, h=402, extra=' fetchpriority="high"')}
      <div class="hero__tag">{tag([("Agent for", "TORAY Japan"), ("In Sri Lanka", "Sole distributor")], brand="J.P.F &amp; S", dark=True)}</div>
    </div>
  </div>
  <div class="ticker" aria-label="Product categories"><div class="ticker__track">{ticker_items}{ticker_items.replace('class="ticker__item"', 'class="ticker__item" aria-hidden="true" tabindex="-1"')}</div></div>
</section>

<section class="sec sec--ink heritage on-dark">
  <div class="mesh-bg"></div>
  <div class="wrap" style="position:relative">
    <div class="heritage__grid">
      <div class="heritage__year" data-reveal="left">
        <div class="heritage__big" aria-hidden="true">1953</div>
        <div class="heritage__seal">
          <svg class="heritage__seal-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ring" d="M100 100m-86 0a86 86 0 1 1 172 0a86 86 0 1 1-172 0"/></defs><text><textPath href="#ring">Pioneers in fishing nets · Colombo · Since 1953 ·</textPath></text></svg>
          {img(p, 'logo.webp', 'J.P. Fernando & Sons seal, since 1953')}
        </div>
      </div>
      <div class="heritage__copy">
        <span class="eyebrow label" data-reveal>Our story</span>
        <h2 class="h2" data-split>Sri Lanka's first distributor of imported <em>fishing nets.</em></h2>
        <p class="lede" data-reveal>J.P. Fernando &amp; Sons was founded in {FOUNDED} to bring imported fishing nets and accessories to Sri Lankan fishermen. Through decades as agent for Japanese and Korean brands, and later as a manufacturer in our own right, one principle has stayed the same: <strong style="color:var(--paper);font-weight:500">Quality First.</strong></p>
        <a class="btn btn--paper" href="{rel(p, 'about-us/')}" data-reveal>Read our history {ICON['arrow']}</a>
      </div>
    </div>
    <div class="facts">
      <div class="fact" data-reveal><span class="fact__n num"><span data-years data-count="{years()}">{years()}</span><sup>yrs</sup></span><span class="fact__t">serving Sri Lanka's fishing community, from Sea Street, Colombo.</span></div>
      <div class="fact" data-reveal style="--d:.1s"><span class="fact__n num">Sole</span><span class="fact__t">agent and single distributor of TORAY Japan products in Sri Lanka.</span></div>
      <div class="fact" data-reveal style="--d:.2s"><span class="fact__n num">Island<sup>wide</sup></span><span class="fact__t">distribution network, proven on Ministry of Fisheries government tenders.</span></div>
    </div>
  </div>
</section>

<section class="sec" id="range">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow label" data-reveal>The range</span><h2 class="h2" data-split>Everything a <em>fishing boat</em> needs, from net to hook.</h2></div>
      <p class="lede" data-reveal>Seven product families, sold wholesale and retail — to trade buyers, government tenders and individual fishermen alike.</p>
    </div>
    <div class="explorer">
      <ul class="explorer__list">{explorer_items}</ul>
      <div class="explorer__stage" aria-hidden="true">{explorer_imgs}
        <div class="explorer__cap"><span class="label">Hover a category</span></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight" style="padding-top:0">
  <div class="wrap">
    <div class="paths">
      <article class="path path--trade on-dark" data-reveal>
        <span class="label">For trade &amp; tender buyers</span>
        <h2 class="h2">Supplying at <em>scale.</em></h2>
        <p>Dealers, net-makers, cooperatives and government buyers work with us for dependable supply and an established distribution network that reaches the whole island.</p>
        <ul class="path__list">
          <li>Sole distributor of TORAY Japan yarn in Sri Lanka</li>
          <li>Locally manufactured SuperCatch nets — made to your mesh and size</li>
          <li>Experience delivering Ministry of Fisheries government tenders</li>
        </ul>
        <div class="path__foot">
          <a class="btn btn--buoy" href="{rel(p, 'contact-us/')}#enquiry">Request a trade quote {ICON['arrow']}</a>
          <a class="link-arrow" href="{rel(p, 'brands/')}">Our brands {ICON['arrow']}</a>
        </div>
        {img(p, 'toray-yarn.jpg', '', 'path__img')}
      </article>
      <article class="path path--fisher" data-reveal style="--d:.12s">
        <span class="label">For fishermen &amp; anglers</span>
        <h2 class="h2">Gear you can <em>trust.</em></h2>
        <p>Whether you need a single net, a coil of rope or a box of hooks, visit our Sea Street store or call ahead and we'll tell you what's in stock.</p>
        <ul class="path__list">
          <li>Nets, lines and ropes in many sizes and colours</li>
          <li>Hooks, swivels, lures, floats, reels and rods</li>
          <li>Wholesale and retail — buy one item or a full order</li>
          <li>Open Monday to Saturday in Colombo 11</li>
        </ul>
        <div class="path__foot">
          <a class="btn" href="{rel(p, 'products/')}">Browse products {ICON['arrow']}</a>
          <a class="link-arrow" href="tel:{PHONES[0][1]}">Call the store {ICON['arrow']}</a>
        </div>
        {img(p, 'lures-cut.webp', '', 'path__img')}
      </article>
    </div>
  </div>
</section>

<section class="sec sec--ink on-dark">
  <div class="wrap">
    <div class="toray">
      <div class="toray__media">
        <div class="toray__img" data-clip>{img(p, 'toray-yarn.jpg', 'TORAY nylon yarn on bobbins', w=800, h=500)}</div>
        <div class="toray__badge">{tag([("Origin", "Japan"), ("Since", "Nylon pioneers, 1951")], brand="TORAY")}</div>
      </div>
      <div class="toray__copy">
        <span class="eyebrow label" data-reveal>What goes into our nets</span>
        <blockquote data-split>Every net we make starts with <em>TORAY Japan</em> yarn.</blockquote>
        <p class="lede" data-reveal>Our Quality First principle led us to use TORAY Japan nylon yarn in all of our own fishing-net brands — and J.P. Fernando &amp; Sons became sole agent and single distributor of TORAY products in Sri Lanka.</p>
        <a class="btn btn--paper" href="{rel(p, 'nylon-yarn-twine/toray/')}" data-reveal>About TORAY yarn {ICON['arrow']}</a>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow label" data-reveal>Brands</span><h2 class="h2" data-split>Names fishermen have trusted <em>for decades.</em></h2></div>
      <p class="lede" data-reveal>Our own SuperCatch and J.P. Fernando &amp; Sons nets, alongside respected brands from Japan and beyond.</p>
    </div>
    <div class="brands">{brand_cells}</div>
    <p class="history-agents" data-reveal><strong>Agent over the decades for</strong> {' · '.join(HISTORIC_AGENCIES)}</p>
  </div>
</section>

<section class="sec sec--paper2 sec--tight">
  <div class="wrap trust">
    <div class="trust__card" data-reveal><span class="trust__icon">{ICON['anchor']}</span><h3 class="h3">The first, since {FOUNDED}</h3><p>The pioneer in distributing imported fishing nets and accessories in Sri Lanka, and a leading name in the market today.</p></div>
    <div class="trust__card" data-reveal style="--d:.1s"><span class="trust__icon">{ICON['mesh']}</span><h3 class="h3">Made on Japanese machines</h3><p>Our own brands are manufactured locally using the latest Japanese net-making machines and TORAY Japan yarn.</p></div>
    <div class="trust__card" data-reveal style="--d:.2s"><span class="trust__icon">{ICON['island']}</span><h3 class="h3">Proven on government tenders</h3><p>Successful government tenders for the Ministry of Fisheries and Aquatic Resources showed the reach of our island-wide network.</p></div>
  </div>
</section>

<section class="sec sec--ink on-dark" id="quote">
  <div class="mesh-bg"></div>
  <div class="wrap quote" style="position:relative">
    <div class="quote__intro">
      <span class="eyebrow label" data-reveal>Request a quote</span>
      <h2 class="h2" data-split>Tell us what you're <em>fishing for.</em></h2>
      <p class="lede" data-reveal>Send us the product, size and quantity. We reply during business hours, Monday to Saturday.</p>
      <div class="quote__contacts" data-reveal>
        <a href="tel:{PHONES[0][1]}"><span class="label">Call</span><span>{PHONES[0][0]}</span></a>
        <a href="https://wa.me/{MOBILE[1].lstrip("+")}" target="_blank" rel="noopener"><span class="label">WhatsApp</span><span>{MOBILE[0]}</span></a>
        <a href="mailto:{EMAIL}"><span class="label">Email</span><span>{EMAIL}</span></a>
      </div>
    </div>
    <div class="quote__form" data-reveal style="--d:.15s">{enquiry_form(p, compact=True, dark=True)}</div>
  </div>
</section>
{footer(p, with_cta=False)}"""
    write(p, body)


def page_category(c):
    p = c["slug"]
    pid = p.strip("/")
    range_rows = ""
    if c["children"]:
        rows = ""
        for ch in c["children"]:
            pr = PRODUCTS[ch]
            rows += f"""<div class="range__row" data-reveal>
        <a class="range__img" href="{rel(p, pr['slug'])}" tabindex="-1" aria-hidden="true">{img(p, pr['img'], '')}</a>
        <div><span class="label" style="color:var(--muted)">{e(pr['kind'])}</span><h3 class="h3"><a href="{rel(p, pr['slug'])}">{pr['title_html']}</a></h3><p>{e(pr['blurb'])}</p></div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">{add_btn(p, pr['slug'].strip('/'), pr['name'])}<a class="btn btn--sm btn--ghost" href="{rel(p, pr['slug'])}">View {ICON['arrow']}</a></div>
      </div>"""
        range_rows = f"""<section class="sec sec--tight sec--paper2">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow label" data-reveal>In this range</span><h2 class="h2" data-split>Choose your <em>{e(c['name'].split()[-1].lower())}</em></h2></div></div>
    <div class="range">{rows}</div>
  </div>
</section>"""
    gal = ""
    if len(c["gallery"]) > 1:
        gal = f"""<section class="sec sec--tight">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow label" data-reveal>Gallery</span><h2 class="h2" data-split>A closer <em>look</em></h2></div><p class="lede" data-reveal>Select any image to enlarge it.</p></div>
    {gallery(p, c['gallery'])}
  </div>
</section>"""
    idx = CATEGORIES.index(c) + 1
    body = f"""{head(p, c['name'], c['blurb'] + ' ' + c['intro'], og_img=c['img'])}
{header(p)}
<section class="cat-hero">
  <div class="mesh-bg mesh-bg--ink"></div>
  <div class="wrap cat-hero__grid" style="position:relative">
    <div class="cat-hero__copy">
      {crumbs(p, [("Products", "products/"), (c['name'], None)])}
      <span class="eyebrow label" data-reveal>Category 0{idx} / 0{len(CATEGORIES)}</span>
      <h1 class="h1" data-split>{c['title_html']}</h1>
      <p class="lede" data-reveal style="--d:.3s">{e(c['intro'])}</p>
      <div class="cat-hero__actions" data-reveal style="--d:.45s">
        <a class="btn" href="{rel(p, 'contact-us/')}?product={e(c['name'])}#enquiry">Request a quote {ICON['arrow']}</a>
        {add_btn(p, pid, c['name'], lg=True)}
      </div>
    </div>
    <div class="cat-hero__media">
      <div class="cat-hero__frame{' contain' if c['fit'] == 'contain' else ''}" data-clip>{img(p, c['img'], c['name'], loading='eager')}</div>
      <div class="cat-hero__tag">{tag(c['tag'], brand=f"0{idx}")}</div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap cat-body">
    <div class="cat-body__main prose" data-reveal>{render_body(p, c['body'])}</div>
    <div class="cat-body__side">{side_card(p, c['name'], pid, c['ask'])}</div>
  </div>
</section>
{range_rows}
{gal}
{related(p, p)}
{footer(p)}"""
    write(p, body)


def page_product(key):
    pr = PRODUCTS[key]
    p = pr["slug"]
    parent = CAT_BY_SLUG[pr["parent"]]
    spec = "".join(f'<div class="spec__row"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in pr["spec"])
    siblings = [PRODUCTS[s] for s in parent["children"] if s != key]
    sib_cards = "".join(
        f'<article class="card" data-reveal><div class="card__media{" contain" if s["fit"] == "contain" else ""}">{img(p, s["img"], s["name"])}<span class="card__tag label">{e(parent["name"])}</span></div>'
        f'<div class="card__body"><h3 class="card__title"><a class="card__link" href="{rel(p, s["slug"])}">{e(s["name"])}</a></h3><p class="card__text">{e(s["blurb"])}</p>'
        f'<div class="card__foot">{add_btn(p, s["slug"].strip("/"), s["name"])}<span class="link-arrow">View {ICON["arrow"]}</span></div></div></article>'
        for s in siblings)
    sib = f"""<section class="sec sec--tight sec--paper2">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow label" data-reveal>Also in {e(parent['name'])}</span><h2 class="h2" data-split>Related <em>products</em></h2></div>
    <div><a class="link-arrow" href="{rel(p, parent['slug'])}">All {e(parent['name'].lower())} {ICON['arrow']}</a></div></div>
    <div class="cards">{sib_cards}</div>
  </div>
</section>""" if siblings else ""
    gal = f"""<section class="sec sec--tight" style="padding-top:0"><div class="wrap">{gallery(p, pr['gallery'])}</div></section>""" if len(pr["gallery"]) > 1 else ""
    body = f"""{head(p, f"{pr['name']} — {parent['name']}", pr['blurb'], og_img=pr['img'])}
{header(p)}
<section class="cat-hero">
  <div class="mesh-bg mesh-bg--ink"></div>
  <div class="wrap cat-hero__grid" style="position:relative">
    <div class="cat-hero__copy">
      {crumbs(p, [("Products", "products/"), (parent['name'], parent['slug']), (pr['name'], None)])}
      <span class="eyebrow label" data-reveal>{e(pr['kind'])}</span>
      <h1 class="h1" data-split>{pr['title_html']}</h1>
      <p class="lede" data-reveal style="--d:.3s">{e(pr['blurb'])}</p>
      <div class="cat-hero__actions" data-reveal style="--d:.45s">
        <a class="btn" href="{rel(p, 'contact-us/')}?product={e(parent['name'] + ' — ' + pr['name'])}#enquiry">Request a quote {ICON['arrow']}</a>
        {add_btn(p, p.strip('/'), pr['name'], lg=True)}
      </div>
    </div>
    <div class="cat-hero__media">
      <div class="cat-hero__frame{' contain' if pr['fit'] == 'contain' else ''}" data-clip>{img(p, pr['img'], pr['name'], loading='eager')}</div>
      <div class="cat-hero__tag">{tag(pr['tag'])}</div>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap cat-body">
    <div class="cat-body__main prose" data-reveal>
      {render_body(p, pr['body'])}
      <h2 style="margin-top:48px">Product details</h2>
      <dl class="spec">{spec}</dl>
    </div>
    <div class="cat-body__side">{side_card(p, pr['name'], p.strip('/'), parent['ask'])}</div>
  </div>
</section>
{gal}
{sib}
{related(p, parent['slug'])}
{footer(p)}"""
    write(p, body)


def page_products():
    p = "products/"
    cards = []
    groups = {"nets": "Nets", "lines": "Ropes & lines", "yarn": "Yarn & twine", "tackle": "Tackle & accessories"}
    for i, c in enumerate(CATEGORIES):
        wide = " is-wide" if i in (0, 3) else ""
        cards.append(
            f'<article class="card{wide}" data-group="{c["group"]}" data-reveal><div class="card__media{" contain" if c["fit"] == "contain" else ""}">{img(p, c["img"], c["name"])}<span class="card__tag label">{e(groups[c["group"]])}</span></div>'
            f'<div class="card__body"><span class="label" style="color:var(--muted);margin-bottom:10px">Category 0{i+1}</span><h2 class="card__title"><a class="card__link" href="{rel(p, c["slug"])}">{e(c["name"])}</a></h2><p class="card__text">{e(c["blurb"])}</p>'
            f'<div class="card__foot">{add_btn(p, c["slug"].strip("/"), c["name"])}<span class="link-arrow">Explore {ICON["arrow"]}</span></div></div></article>')
        for ch in c["children"]:
            pr = PRODUCTS[ch]
            cards.append(
                f'<article class="card" data-group="{c["group"]}" data-reveal><div class="card__media{" contain" if pr["fit"] == "contain" else ""}">{img(p, pr["img"], pr["name"])}<span class="card__tag label">{e(c["name"])}</span></div>'
                f'<div class="card__body"><h2 class="card__title"><a class="card__link" href="{rel(p, pr["slug"])}">{e(pr["name"])}</a></h2><p class="card__text">{e(pr["blurb"])}</p>'
                f'<div class="card__foot">{add_btn(p, pr["slug"].strip("/"), pr["name"])}<span class="link-arrow">View {ICON["arrow"]}</span></div></div></article>')
    filt = '<button class="filter" type="button" data-filter="all" aria-pressed="true">All products</button>' + "".join(
        f'<button class="filter" type="button" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in groups.items())
    body = f"""{head(p, 'Products', 'Nylon and HDPE fishing nets, monofilament lines, HDPE, PP and Vinylon ropes, TORAY nylon yarn and twine, tackle and fishing accessories from J.P. Fernando & Sons, Colombo.')}
{header(p)}
<section class="phero">
  <div class="mesh-bg mesh-bg--ink"></div>
  <div class="wrap phero__grid" style="position:relative">
    <div class="phero__title">{crumbs(p, [("Products", None)])}<span class="eyebrow label" data-reveal>The full range</span><h1 class="h1" data-split style="margin-top:20px">From the net <em>to the hook.</em></h1></div>
    <div class="phero__aside"><p class="lede" data-reveal>Browse every category, add products to your enquiry list, then send one request for availability and pricing.</p></div>
  </div>
</section>
<section class="sec" style="padding-top:20px">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter products">{filt}</div>
    <div class="hub">{''.join(cards)}</div>
  </div>
</section>
{footer(p)}"""
    write(p, body)


def page_brands():
    p = "brands/"
    rows = ""
    for i, b in enumerate(BRANDS):
        link = f'<a class="link-arrow" href="{rel(p, b["link"])}">See products {ICON["arrow"]}</a>' if b["link"] else ""
        rows += f"""<div class="range__row" data-reveal>
      <div class="range__img" style="display:grid;place-items:center;padding:10px">{img(p, b['img'], b['name'] + ' logo')}</div>
      <div><span class="label" style="color:var(--muted)">{e(b['where'])}</span><h2 class="h3" style="margin:6px 0 8px">{e(b['name'])}</h2><p>{e(b['note'])}</p></div>
      <div>{link}</div>
    </div>"""
    body = f"""{head(p, 'Brands', 'TORAY Japan (sole agent in Sri Lanka), SuperCatch, Nitto and other fishing-net brands supplied by J.P. Fernando & Sons, Colombo.')}
{header(p, dark=True)}
<section class="phero phero--ink on-dark">
  <div class="mesh-bg"></div>
  <div class="wrap phero__grid" style="position:relative">
    <div class="phero__title">{crumbs(p, [("Brands", None)])}<span class="eyebrow label" data-reveal>Brands &amp; agencies</span><h1 class="h1" data-split style="margin-top:20px">Trusted names, <em>one supplier.</em></h1></div>
    <div class="phero__aside"><p class="lede" data-reveal>From our own SuperCatch nets to TORAY Japan yarn — the brands behind the J.P. Fernando &amp; Sons range.</p></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="range">{rows}</div>
  </div>
</section>
<section class="sec sec--paper2 sec--tight">
  <div class="wrap cat-body">
    <div class="cat-body__main prose" data-reveal>
      <span class="eyebrow label">A history of agencies</span>
      <h2 style="margin-top:18px">Agent for <em>world-renowned</em> brands</h2>
      <p class="big">Over the decades J.P. Fernando &amp; Sons became importing and distributing agent for {', '.join(HISTORIC_AGENCIES[:-1])} and {HISTORIC_AGENCIES[-1]} — for many years among the most popular and leading brands in the island.</p>
      <p>Since the mid-1990s, as customers became more price-sensitive and production costs rose in Japan and Korea, we have also distributed many leading Indian fishing-net brands, while manufacturing our own brands locally.</p>
    </div>
    <div class="cat-body__side" data-reveal>{tag([("Sole agent", "TORAY Japan"), ("Own brands", "SuperCatch · J.P.F & S")], brand="Since 1953")}</div>
  </div>
</section>
{footer(p)}"""
    write(p, body)


def page_about():
    p = "about-us/"
    eras = [
        (str(FOUNDED), "The pioneer", f"J.P. Fernando &amp; Sons was founded in {FOUNDED} and became the pioneer in distributing imported fishing nets and accessories in Sri Lanka."),
        ("Agency years", "Agent for world-renowned brands", f"The company grew into importing and distributing agent for {', '.join(HISTORIC_AGENCIES[:-1])} and {HISTORIC_AGENCIES[-1]} — among the most popular and leading brands in the island for decades."),
        ("70s – 90s", "Quality First", "Guided by its &ldquo;Quality First&rdquo; principle, the company became the leading and most reputed fishing-gear distributor in Sri Lanka through the 1970s, 80s and early 90s, when most customers wanted premium-quality products only."),
        ("Mid-90s", "Making our own", "As local economic conditions changed and production costs rose in Japan and Korea, we began distributing leading Indian fishing-net brands — and manufacturing our own brands locally, using the latest Japanese machines."),
        ("TORAY", "Sole agent for TORAY Japan", "Our Quality First principle led us to use TORAY Japan yarn in all our net brands. J.P. Fernando &amp; Sons was then appointed sole agent and single distributor of TORAY products in Sri Lanka."),
        ("Today", "A leader in Sri Lankan fishing nets", "Today J.P. Fernando &amp; Sons is a leader in Sri Lanka's fishing-net market, and SuperCatch and J.P. Fernando &amp; Sons are among the most popular quality brands in the country."),
    ]
    era_html = "".join(f"""<div class="era">
      <span class="era__knot" aria-hidden="true"></span>
      <div class="era__when">{w}</div>
      <div class="era__body"><h3 class="h3">{t}</h3><p>{d}</p></div>
    </div>""" for w, t, d in eras)
    body = f"""{head(p, 'About us', f'Founded in {FOUNDED}, J.P. Fernando & Sons pioneered the distribution of imported fishing nets in Sri Lanka and is sole agent for TORAY Japan. Our history, principles and people.')}
{header(p, dark=True)}
<section class="about-hero on-dark">
  <div class="mesh-bg"></div>
  <div class="wrap" style="position:relative">
    {crumbs(p, [("About us", None)])}
    <span class="eyebrow label" data-reveal>About J.P. Fernando &amp; Sons</span>
    <h1 class="display about-hero__title" data-split style="margin-top:24px">Seven decades <br>on <em>Sea Street.</em></h1>
    <div class="about-hero__row">
      <p class="lede" data-reveal>Manufacturers, importers and distributors of all kinds of nylon and cotton fishing nets, twines, lines and fishing accessories — and the pioneers of imported fishing nets in Sri Lanka since {FOUNDED}.</p>
      <p class="about-hero__si" data-reveal style="--d:.15s"><span lang="si">{NAME_SI}</span><br><span lang="ta" class="ta">{NAME_TA}</span></p>
    </div>
  </div>
  <figure class="banner-band" style="margin:0" data-reveal="fade">
    {img(p, 'banner.jpg', 'J.P. Fernando & Sons banner showing the brands and products the company carries', w=1280, h=540)}
    <figcaption>Our brands and range, as shown on the J.P. Fernando &amp; Sons shop banner.</figcaption>
  </figure>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow label" data-reveal>Company profile</span><h2 class="h2" data-split>A story told in <em>knots.</em></h2></div>
    <p class="lede" data-reveal>From the first imported nets to our own SuperCatch brand — the milestones that made us.</p></div>
    <div class="timeline">
      <div class="timeline__rope" aria-hidden="true"><svg preserveAspectRatio="none"><path class="rope-a"/></svg></div>
      {era_html}
    </div>
  </div>
</section>

<section class="sec sec--ink on-dark">
  <div class="mesh-bg"></div>
  <div class="wrap principle" style="position:relative">
    <span class="eyebrow label" data-reveal>Our principle</span>
    <p class="principle__q" data-split>Quality <em>first.</em> Then everything else.</p>
    <p class="lede" data-reveal style="margin:0 auto">It is why we chose the finest fishing-net yarn we know for our own brands, and why fishermen across the island have relied on our nets for generations.</p>
  </div>
</section>

<section class="sec sec--tight sec--paper2">
  <div class="wrap trust">
    <div class="trust__card" data-reveal><span class="trust__icon">{ICON['island']}</span><h3 class="h3">Island-wide network</h3><p>Successful participation in and completion of government tenders for the Ministry of Fisheries and Aquatic Resources highlighted the standard and capacity of our distribution network across the entire island.</p></div>
    <div class="trust__card" data-reveal style="--d:.1s"><span class="trust__icon">{ICON['mesh']}</span><h3 class="h3">Local manufacturing</h3><p>Our own net brands are manufactured in Sri Lanka on the latest Japanese machines, using TORAY Japan nylon yarn.</p></div>
    <div class="trust__card" data-reveal style="--d:.2s"><span class="trust__icon">{ICON['anchor']}</span><h3 class="h3">Nets, lines &amp; more</h3><p>From nylon nets we expanded into manufacturing and distributing fishing lines, HDPE nets, nylon yarn, twine and fishing accessories.</p></div>
  </div>
</section>

<section class="sec">
  <div class="wrap signoff">
    <div class="signoff__card" data-reveal>
      <span class="label" style="color:var(--muted)">From the partners</span>
      <p class="signoff__name">Dinesh Fernando</p>
      <span class="label">Partner</span>
      <address style="font-style:normal;margin-top:22px;color:var(--muted)">{'<br>'.join(ADDRESS)}</address>
    </div>
    <div class="signoff__copy prose" data-reveal style="--d:.1s">
      <p class="big">&ldquo;We are delighted to present our company to you, and we look forward to serving you in the near future.&rdquo;</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px">
        <a class="btn" href="{rel(p, 'contact-us/')}">Get in touch {ICON['arrow']}</a>
        <a class="btn btn--ghost" href="{rel(p, 'products/')}">See our products</a>
      </div>
    </div>
  </div>
</section>
{footer(p)}"""
    write(p, body)


def page_contact():
    p = "contact-us/"
    phones = "".join(f'<a href="tel:{t}">{d}<small>{l}</small></a>' for d, t, l in PHONES)
    hours = "".join(f'<div{" class=closed" if h == "Closed" else ""}><span>{d}</span><span>{h}</span></div>' for d, h in HOURS)
    mapq = urllib.parse.quote_plus(MAP_Q, safe="/,")
    body = f"""{head(p, 'Contact us & request a quote', f'Call {PHONES[0][0]}, WhatsApp {MOBILE[0]}, email {EMAIL}, or visit us at 287/1 Sea Street, Colombo 11. Request availability and quotations for fishing nets, ropes, lines and accessories.')}
{header(p)}
<section class="phero">
  <div class="mesh-bg mesh-bg--ink"></div>
  <div class="wrap phero__grid" style="position:relative">
    <div class="phero__title">{crumbs(p, [("Contact", None)])}<span class="eyebrow label" data-reveal>Contact &amp; quotations</span><h1 class="h1" data-split style="margin-top:20px">Let's talk <em>nets.</em></h1></div>
    <div class="phero__aside"><p class="lede" data-reveal>Trade buyers, tender offices and individual fishermen — tell us what you need and we'll come back with availability and pricing.</p></div>
  </div>
</section>
<section class="sec" style="padding-top:10px" id="enquiry">
  <div class="wrap contact-grid">
    <div class="contact-grid__form" data-reveal>
      <h2 class="h3" style="margin-bottom:28px">Send an enquiry</h2>
      {enquiry_form(p)}
    </div>
    <div class="contact-grid__info" data-reveal style="--d:.1s">
      <div class="info-block"><span class="label">Call</span>{phones}<a href="tel:{MOBILE[1]}">{MOBILE[0]}<small>Mobile</small></a></div>
      <div class="info-block"><span class="label">WhatsApp</span><a href="https://wa.me/{MOBILE[1].lstrip("+")}" target="_blank" rel="noopener">{MOBILE[0]}</a></div>
      <div class="info-block"><span class="label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="info-block"><span class="label">Visit</span><address style="font-style:normal;font-size:20px;line-height:1.5">{'<br>'.join(ADDRESS)}</address>
        <a class="link-arrow" style="font-size:15px;margin-top:10px;display:inline-flex" href="{MAP_URL}" target="_blank" rel="noopener">Open in Google Maps {ICON['arrow']}</a></div>
      <div class="info-block"><span class="label">Opening hours</span><div class="hours">{hours}</div><span class="open-now"></span></div>
    </div>
  </div>
</section>
<section class="sec sec--tight" style="padding-top:0">
  <div class="wrap">
    <div class="map" data-reveal>
      <iframe title="Map showing 287/1 Sea Street, Colombo 11" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps/embed?origin=mfe&amp;pb=!1m3!2m1!1s{mapq}!6i16"></iframe>
      <div class="map__pin">{tag([("Find us", "287/1 Sea Street"), ("City", "Colombo 11, Sri Lanka")], dark=True)}</div>
    </div>
  </div>
</section>
{footer(p, with_cta=False)}"""
    write(p, body)


def page_404():
    p = "404"
    # 404 is served from any depth, so use root-absolute asset paths
    body = f"""{head('', 'Page not found', 'The page you were looking for could not be found.')}
{header('')}
<section class="lost">
  <div>
    <span class="eyebrow label">Error 404</span>
    <h1 class="h1">This one <em>got away.</em></h1>
    <p class="lede" style="margin:0 auto 30px">The page you were looking for isn't here. Try one of these instead.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
      <a class="btn" href="./">Back to home {ICON['arrow']}</a>
      <a class="btn btn--ghost" href="products/">Browse products</a>
    </div>
  </div>
</section>
{footer('', with_cta=False)}"""
    body = body.replace('href="./', 'href="/').replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    for c in ["products/", "brands/", "about-us/", "contact-us/"] + [x["slug"] for x in CATEGORIES]:
        body = body.replace(f'href="{c}', f'href="/{c}')
    write(p, body)


def sitemap():
    pages = ["", "products/", "brands/", "about-us/", "contact-us/"] + [c["slug"] for c in CATEGORIES] + [v["slug"] for v in PRODUCTS.values()]
    urls = "".join(f"<url><loc>{SITE}{x}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for x in pages)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    return pages


if __name__ == "__main__":
    page_home()
    page_products()
    page_brands()
    page_about()
    page_contact()
    for c in CATEGORIES:
        page_category(c)
    for k in PRODUCTS:
        page_product(k)
    page_404()
    n = sitemap()
    print(f"Built {len(n) + 1} pages into {ROOT}")
