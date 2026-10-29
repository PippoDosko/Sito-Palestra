"""Genera il sito partendo da src/.
- docs/: il sito online (GitHub Pages). Pagine leggere che usano file separati
  per stile, script e immagini, scaricati una volta sola e tenuti in memoria dal browser.
- dist/ e anteprima-sito.html: versioni autosufficienti (tutto incorporato) per le anteprime.
Uso: python3 build.py   (richiede Pillow per le immagini)"""
import base64, hashlib, pathlib

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
DIST.mkdir(exist_ok=True)
for old in DIST.glob("*.html"):
    old.unlink()  # toglie le pagine eliminate

LOGO = "data:image/png;base64," + base64.b64encode((SRC / "img" / "logo.png").read_bytes()).decode()
CSS = (SRC / "styles.css").read_text()
IMG_OUTDOOR = "data:image/jpeg;base64," + base64.b64encode((SRC / "img" / "outdoor.jpg").read_bytes()).decode()
JS = (SRC / "script.js").read_text()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Chivo+Mono:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">')
OUTDOOR_SRCSET = 'srcset="img/outdoor-720.webp 720w, img/outdoor-1179.webp 1179w"'

# Font ospitati sul sito (src/fonts, ridotti ai caratteri latini e ai pesi usati): nessun collegamento a Google
FONT_FACES = """@font-face{font-family:"Big Shoulders Display";src:url(fonts/big-shoulders-display.woff) format("woff");font-weight:700 900;font-display:swap}
@font-face{font-family:"Manrope";src:url(fonts/manrope.woff) format("woff");font-weight:400 800;font-display:swap}
@font-face{font-family:"Chivo Mono";src:url(fonts/chivo-mono.woff) format("woff");font-weight:500 700;font-display:swap}
"""
LEAFLET_VER = "1.9.4"

def version(text):
    """Breve impronta del contenuto: cambia il nome richiesto quando il file cambia, così il browser non usa la copia vecchia."""
    return hashlib.sha1(text.encode()).hexdigest()[:8]

# Risorse per le due modalità: incorporate (anteprime) oppure file separati (sito online)
INLINE = {
    "logo": LOGO, "outdoor": IMG_OUTDOOR, "outdoor_srcset": "",
    "icons": f'<link rel="icon" href="{LOGO}">',
    "css": f"<style>\n{CSS}\n</style>", "js": f"<script>\n{JS}\n</script>", "preload": "", "fonts": FONTS,
    "leaflet_js": f"https://cdnjs.cloudflare.com/ajax/libs/leaflet/{LEAFLET_VER}/leaflet.js",
    "leaflet_css": f"https://cdnjs.cloudflare.com/ajax/libs/leaflet/{LEAFLET_VER}/leaflet.css",
}
FILES = {
    "logo": "img/logo-128.webp", "outdoor": "img/outdoor-1179.webp", "outdoor_srcset": OUTDOOR_SRCSET + ' sizes="100vw"',
    "icons": ('<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png">\n'
              '<link rel="icon" href="img/favicon-192.png" sizes="192x192" type="image/png">\n'
              '<link rel="apple-touch-icon" href="img/apple-touch-icon.png">'),
    "css": f'<link rel="stylesheet" href="assets/styles.css?v={version(FONT_FACES + CSS)}">',
    "fonts": ('<link rel="preload" as="font" type="font/woff" href="assets/fonts/big-shoulders-display.woff" crossorigin>\n'
              '<link rel="preload" as="font" type="font/woff" href="assets/fonts/manrope.woff" crossorigin>'),
    "leaflet_js": f"assets/leaflet/leaflet.js?v={LEAFLET_VER}",
    "leaflet_css": f"assets/leaflet/leaflet.css?v={LEAFLET_VER}",
    "js": f'<script src="assets/script.js?v={version(JS)}"></script>',
    "preload": ('<link rel="preload" as="image" href="img/outdoor-1179.webp" fetchpriority="high" '
                'imagesrcset="img/outdoor-720.webp 720w, img/outdoor-1179.webp 1179w" imagesizes="100vw">'),
}

# file, voce di menu, icona, titolo della scheda, descrizione per Google
PAGES = [
    ("index.html",         "Home",           "var(--orange)", "Sport's Center 2 · Palestra a Roveleto di Cadeo (PC)",
     "ASD Sport's Center 2: sala pesi, zona cardio, sala corsi e area outdoor a Roveleto di Cadeo (Piacenza)."),
    ("spazi.html",         "I nostri spazi", "var(--magenta)", "I nostri spazi · Sport's Center 2",
     "Sala pesi, zona cardio, sala corsi e area outdoor dello Sport's Center 2 a Roveleto di Cadeo."),
    ("corsi.html",         "I corsi",        "var(--teal)", "I corsi · Sport's Center 2",
     "Pump, Pilates, Triform e Step: i corsi dello Sport's Center 2 con giorni e orari."),
    ("personale.html",     "Il personale",   "var(--purple)", "Il personale · Sport's Center 2",
     "Istruttori e staff dello Sport's Center 2 a Roveleto di Cadeo."),
    ("prezzi.html",        "Listino prezzi", "var(--green)", "Listino prezzi · Sport's Center 2",
     "Abbonamenti dal mensile all'annuale, ingresso giornaliero e tariffe ragazzi, per soci e non soci."),
    ("dove-trovarci.html", "Dove trovarci",  "var(--orange)", "Dove trovarci · Sport's Center 2",
     "Orari di apertura, indirizzo, telefono e mappa dello Sport's Center 2 a Roveleto di Cadeo."),
    ("privacy.html",       "Privacy e cookie", "var(--chalk)", "Privacy e cookie · Sport's Center 2",
     "Informativa sulla privacy e sui cookie del sito dello Sport's Center 2."),
]
NOT_IN_MENU = {"index.html", "privacy.html"}  # la home si raggiunge dal logo, la privacy dal piè di pagina
STRIPE = '<div class="stripe"><span></span><span></span><span></span><span></span><span></span></div>'

def nav(current):
    items = []
    for f, label, color, *_ in PAGES:
        if f in NOT_IN_MENU:
            continue
        cls = ' active" aria-current="page' if f == current else ""
        items.append(f'<li><a class="nav-link{cls}" href="{f}" style="--c:{color}">{label}</a></li>')
    items.append('<li class="menu-extra"><a class="btn" data-tel href="#">Chiama lo 0523 500928</a>'
                 '<p>Via Cavour 3 · Roveleto di Cadeo (PC)</p></li>')
    return "\n      ".join(items)

def band():
    return f"""<div class="wrap"><div class="band">
    <div><h2 class="display">Vieni a trovarci</h2><p>Per informazioni chiamaci o passa direttamente in palestra.</p></div>
    <div class="btns"><a class="btn" data-tel href="#">Chiama</a><a class="btn ghost" href="dove-trovarci.html">Come raggiungerci</a></div>
    {STRIPE}</div></div>"""

def fill(text, a):
    return (text.replace("{{LOGO}}", a["logo"]).replace("{{IMG_OUTDOOR}}", a["outdoor"])
                .replace("{{OUTDOOR_SRCSET}}", a["outdoor_srcset"])
                .replace("{{LEAFLET_JS}}", a["leaflet_js"]).replace("{{LEAFLET_CSS}}", a["leaflet_css"]))

def page(f, title, desc, a=INLINE):
    body = fill((SRC / "pages" / f).read_text(), a)
    foot_links = " ".join(f'<a href="{p[0]}">{p[1]}</a>' for p in PAGES if p[0] != "privacy.html")
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0F0F0E">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{desc}">
{a["icons"]}
{a["preload"] if f == "index.html" else ""}
{a["fonts"]}
{a["css"]}
</head>
<body>
<header>
  {STRIPE}
  <nav class="wrap nav" aria-label="Menu principale">
    <a class="brand" href="index.html">
      <img src="{a["logo"]}" alt="Logo ASD Sport's Center 2" width="42" height="42">
      <b>Sport's Center 2</b>
    </a>
    <ul class="links">
      {nav(f)}
    </ul>
    <a class="btn nav-call" data-tel href="#">Chiama</a>
    <button class="menu-btn" aria-label="Apri il menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </nav>
</header>
<main style="--sec:{dict((p[0],p[2]) for p in PAGES)[f]}">
{body}
{band() if f not in ("dove-trovarci.html", "privacy.html") else ""}
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <a class="brand" href="index.html"><img src="{a["logo"]}" alt="" width="42" height="42" loading="lazy"><div><b>Sport's Center 2</b><small>ASD · Roveleto di Cadeo (PC)</small></div></a>
      <nav aria-label="Menu secondario">{foot_links}</nav>
    </div>
    <p class="legal">ASD Sport's Center Due Cadeo · C.F. 90010090331 · P.IVA 01650500331 · <a href="privacy.html">Privacy e cookie</a></p>
  </div>
</footer>
{a["js"]}
</body>
</html>
"""

# Sito pubblicato su GitHub Pages (cartella docs/). Finché è una bozza chiede a Google di non indicizzarlo.
NOINDEX = True
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
for old in DOCS.glob("*.html"):
    old.unlink()
(DOCS / ".nojekyll").write_text("")
(DOCS / "assets").mkdir(exist_ok=True)
(DOCS / "assets" / "styles.css").write_text(FONT_FACES + CSS)
(DOCS / "assets" / "script.js").write_text(JS)
import shutil
for sub_dir in ("fonts", "leaflet"):
    shutil.rmtree(DOCS / "assets" / sub_dir, ignore_errors=True)
shutil.copytree(SRC / "fonts", DOCS / "assets" / "fonts")
shutil.copytree(SRC / "vendor" / "leaflet", DOCS / "assets" / "leaflet")

def build_images():
    """Logo, icone e foto ottimizzati per il sito online, ricavati dai file in src/img/."""
    from PIL import Image
    out = DOCS / "img"
    out.mkdir(exist_ok=True)
    logo = Image.open(SRC / "img" / "logo.png").convert("RGBA")
    small = lambda im: im.quantize(colors=128, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    logo.resize((128, 128), Image.LANCZOS).save(out / "logo-128.webp", quality=88, method=6)
    logo.resize((32, 32), Image.LANCZOS).save(out / "favicon-32.png", optimize=True)
    small(logo.resize((192, 192), Image.LANCZOS)).save(out / "favicon-192.png", optimize=True)
    tile = Image.new("RGBA", (180, 180), (15, 15, 14, 255))  # icona per la schermata Home dell'iPhone
    tile.alpha_composite(logo.resize((156, 156), Image.LANCZOS), (12, 12))
    small(tile).save(out / "apple-touch-icon.png", optimize=True)
    photo = Image.open(SRC / "img" / "outdoor.jpg").convert("RGB")
    photo.save(out / "outdoor-1179.webp", quality=72, method=6)
    photo.resize((720, round(720 * photo.height / photo.width)), Image.LANCZOS).save(out / "outdoor-720.webp", quality=72, method=6)

build_images()

for f, _, _, title, desc in PAGES:
    (DIST / f).write_text(page(f, title, desc))
    html = page(f, title, desc, FILES)
    if NOINDEX:
        html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
    (DOCS / f).write_text(html)
    print("ok", f)

# ---------------------------------------------------------------
# Anteprima unica: tutte le pagine in un solo file, il menu cambia
# pagina senza ricaricare (utile per mostrare il sito al cliente).
# ---------------------------------------------------------------
import re

def to_hash(html):
    # "corsi.html#triform" -> "#corsi:triform", "spazi.html" -> "#spazi", "index.html" -> "#index"
    def rep(m):
        page, anchor = m.group(1), m.group(2)
        return f'href="#{page}' + (f'.{anchor}' if anchor else "") + '"'
    return re.sub(r'href="([a-z-]+)\.html(?:#([a-z-]+))?"', rep, html)

def preview():
    sections = []
    for f, label, ico, title, desc in PAGES:
        key = f[:-5]
        body = fill((SRC / "pages" / f).read_text(), INLINE)
        extra = band() if f not in ("dove-trovarci.html", "privacy.html") else ""
        sections.append(f'<div class="pv-page" data-page="{key}" data-title="{title}" style="--sec:{ico}" hidden>\n{body}\n{extra}\n</div>')
    full = page("index.html", PAGES[0][3], PAGES[0][4])
    main_open = full.index("<main")
    main_start, main_end = full.index(">", main_open) + 1, full.index("</main>")
    full = full[:main_open] + "<main>" + full[main_start:]
    main_start, main_end = full.index("<main>") + len("<main>"), full.index("</main>")
    full = full[:main_start] + "\n" + "\n".join(sections) + "\n" + full[main_end:]
    full = full.replace(' active" aria-current="page', "")
    full = to_hash(full)
    router = """
// Navigazione dell'anteprima unica
function showPage(){
  const [key, anchor] = (location.hash.slice(1) || "index").split(".");
  let found = false;
  document.querySelectorAll(".pv-page").forEach(p => {
    const on = p.dataset.page === key; p.hidden = !on;
    if (on) {
      found = true; document.title = p.dataset.title;
      if (!matchMedia("(prefers-reduced-motion: reduce)").matches)
        p.animate([{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }],
                  { duration: 260, easing: "cubic-bezier(0.23, 1, 0.32, 1)" });
    }
  });
  if (!found) { location.hash = "#index"; return; }
  document.querySelectorAll(".nav-link").forEach(a => {
    const on = a.getAttribute("href") === "#" + key;
    a.classList.toggle("active", on);
    on ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current");
  });
  document.querySelector("header").classList.remove("open");
  document.documentElement.classList.remove("menu-open");
  if (key === "dove-trovarci" && window.refreshMap) requestAnimationFrame(window.refreshMap);
  const target = anchor && document.querySelector(`.pv-page[data-page="${key}"] #${anchor}`);
  if (target) target.scrollIntoView(); else window.scrollTo(0, 0);
}
window.addEventListener("hashchange", showPage);
showPage();
"""
    full = full.replace("</script>\n</body>", router + "</script>\n</body>")
    (ROOT / "anteprima-sito.html").write_text(full)
    print("ok anteprima-sito.html")

def artifact():
    import re
    full = (ROOT / "anteprima-sito.html").read_text()
    title = "<title>Sport's Center 2</title>"
    style = re.search(r"<style>.*?</style>", full, re.S).group(0)
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Chivo+Mono:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap">'
    body = full[full.index("<body>") + 6 : full.index("</body>")]
    # nella pagina pubblicata su Claude la cartografia è bloccata: niente pulsante della mappa, resta la cartolina
    body = re.sub(r'data-leaflet-js="[^"]*"', 'data-leaflet-js=""', body)
    out = "\n".join([title, '<meta name="claude:viewport-fit-sides" content="cover">', fonts, style, body])
    dest = pathlib.Path("/tmp/claude-0/-home-claude/09079919-c381-5bfc-ad5e-cabd613b0d76/scratchpad/sportcenter2-pubblicato.html")
    dest.write_text(out)
    print("ok", dest.name, len(out)//1024, "KB")

preview()
# Copia per la pagina pubblicata su Claude: solo dentro la sessione di lavoro
if pathlib.Path("/tmp/claude-0").exists():
    artifact()
