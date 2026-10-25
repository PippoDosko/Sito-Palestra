"""Genera le pagine del sito in dist/ partendo da src/.
Ogni pagina esce autonoma (CSS, JS e logo incorporati), così si apre anche in anteprima.
Uso: python3 build.py"""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
DIST.mkdir(exist_ok=True)
for old in DIST.glob("*.html"):
    old.unlink()  # toglie le pagine eliminate

LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo.png").read_bytes()).decode()
CSS = (SRC / "styles.css").read_text()
IMG_OUTDOOR = "data:image/jpeg;base64," + base64.b64encode((SRC / "img" / "outdoor.jpg").read_bytes()).decode()
JS = (SRC / "script.js").read_text()

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
     "Abbonamenti trimestrali, semestrali e annuali, ingressi singoli e pacchetti."),
    ("dove-trovarci.html", "Dove trovarci",  "var(--orange)", "Dove trovarci · Sport's Center 2",
     "Orari di apertura, indirizzo, telefono e mappa dello Sport's Center 2 a Roveleto di Cadeo."),
]
LEAFLET = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">\n'
           '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>\n')
PREVIEW_MODE = False
STRIPE = '<div class="stripe"><span></span><span></span><span></span><span></span><span></span></div>'

def nav(current):
    items = []
    for f, label, color, *_ in PAGES:
        if f == "index.html":
            continue  # la home si raggiunge dal logo
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

def page(f, title, desc):
    body = (SRC / "pages" / f).read_text().replace("{{LOGO}}", LOGO).replace("{{IMG_OUTDOOR}}", IMG_OUTDOOR)
    foot_links = " ".join(f'<a href="{p[0]}">{p[1]}</a>' for p in PAGES)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0F0F0E">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Chivo+Mono:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<header>
  {STRIPE}
  <nav class="wrap nav" aria-label="Menu principale">
    <a class="brand" href="index.html">
      <img src="{LOGO}" alt="Logo ASD Sport's Center 2">
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
{band() if f != "dove-trovarci.html" else ""}
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <a class="brand" href="index.html"><img src="{LOGO}" alt=""><div><b>Sport's Center 2</b><small>ASD · Roveleto di Cadeo (PC)</small></div></a>
      <nav aria-label="Menu secondario">{foot_links}</nav>
    </div>
    <p class="legal">ASD Sport's Center Due Cadeo · C.F. 90010090331 · P.IVA 01650500331 · <a href="#"><span class="ph">Privacy &amp; cookie policy</span></a></p>
  </div>
</footer>
{LEAFLET if f == "dove-trovarci.html" and not PREVIEW_MODE else ""}<script>
{JS}
</script>
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

for f, _, _, title, desc in PAGES:
    html = page(f, title, desc)
    (DIST / f).write_text(html)
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
        body = (SRC / "pages" / f).read_text().replace("{{LOGO}}", LOGO).replace("{{IMG_OUTDOOR}}", IMG_OUTDOOR)
        extra = band() if f != "dove-trovarci.html" else ""
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
    full = full.replace("<script>\n", LEAFLET + "<script>\n", 1)  # mappa vera quando si apre il file nel browser
    (ROOT / "anteprima-sito.html").write_text(full)
    print("ok anteprima-sito.html")

def artifact():
    import re
    full = (ROOT / "anteprima-sito.html").read_text()
    title = "<title>Sport's Center 2</title>"
    style = re.search(r"<style>.*?</style>", full, re.S).group(0)
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Chivo+Mono:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap">'
    body = full[full.index("<body>") + 6 : full.index("</body>")]
    body = body.replace(LEAFLET, "")  # nella pagina pubblicata la cartografia è bloccata: resta la cartolina
    out = "\n".join([title, '<meta name="claude:viewport-fit-sides" content="cover">', fonts, style, body])
    dest = pathlib.Path("/tmp/claude-0/-home-claude/09079919-c381-5bfc-ad5e-cabd613b0d76/scratchpad/sportcenter2-pubblicato.html")
    dest.write_text(out)
    print("ok", dest.name, len(out)//1024, "KB")

preview()
# Copia per la pagina pubblicata su Claude: solo dentro la sessione di lavoro
if pathlib.Path("/tmp/claude-0").exists():
    artifact()
