/* =========================================================
   DATI DELLA PALESTRA: si modificano solo qui
   ========================================================= */

// Orari di apertura (dal post Instagram dell'11 ottobre). Indice 0 = domenica.
const HOURS = {
  1: ["Lunedì", "09:30", "21:30"],
  2: ["Martedì", "10:00", "21:30"],
  3: ["Mercoledì", "09:30", "21:30"],
  4: ["Giovedì", "10:00", "21:30"],
  5: ["Venerdì", "09:30", "21:30"],
  6: ["Sabato", "10:30", "14:30"],
  0: ["Domenica", null, null],
};

// Orari dei corsi: giorno (1 = lunedì … 6 = sabato), inizio, fine.
// (dal post Instagram del 6 ottobre)
const COURSE_SLOTS = {
  pump:    [[1, "19:00", "20:00"]],
  pilates: [[2, "19:00", "20:00"], [3, "19:00", "20:00"], [5, "19:00", "20:00"]],
  triform: [[2, "19:00", "20:00"], [5, "19:00", "20:00"]],
  step:    [[4, "19:00", "20:00"]],
};
const COURSE_NAMES = { pump: "Pump", pilates: "Pilates", triform: "Triform", step: "Step" };
const COURSE_COLORS = { pump: "var(--orange)", pilates: "var(--purple)", triform: "var(--green)", step: "var(--magenta)" };

// Telefono della palestra, come va mostrato (es. "0523 123456"). DA INSERIRE.
const PHONE = "0523 500928";
// Link d'invito al gruppo WhatsApp dei corsi (es. "https://chat.whatsapp.com/XXXX"). DA INSERIRE.
const WHATSAPP_GROUP = "";

/* ========================================================= */

const fmt = t => t.replace(/^0/, "");
const toMin = t => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
const DAY_SHORT = ["Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab"];

// Giorno e ora attuali a Roma, qualunque sia il fuso del visitatore
const parts = Object.fromEntries(
  new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false })
    .formatToParts(new Date()).map(p => [p.type, p.value])
);
const today = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(parts.weekday);
const now = (+parts.hour % 24) * 60 + (+parts.minute);

// Indicatore "Aperto ora / Chiuso"
function statusText() {
  const [, o, c] = HOURS[today];
  if (o && now >= toMin(o) && now < toMin(c)) return [true, "Aperto ora · chiudiamo alle " + fmt(c)];
  if (o && now < toMin(o)) return [false, "Chiuso · apriamo oggi alle " + fmt(o)];
  for (let k = 1; k <= 7; k++) {
    const h = HOURS[(today + k) % 7];
    if (h[1]) return [false, "Chiuso · riapriamo " + (k === 1 ? "domani" : h[0].toLowerCase()) + " alle " + fmt(h[1])];
  }
}
document.querySelectorAll("[data-status]").forEach(el => {
  const [open, text] = statusText();
  el.classList.add(open ? "open" : "closed");
  el.querySelector(".txt").textContent = text;
});

// Tabella orari settimanale
const hoursList = document.getElementById("hours");
if (hoursList) {
  [1, 2, 3, 4, 5, 6, 0].forEach(i => {
    const [name, o, c] = HOURS[i];
    const li = document.createElement("li");
    if (!o) li.classList.add("closed");
    if (i === today) li.classList.add("today");
    li.innerHTML = `<span class="d">${name}</span><span class="t">${o ? fmt(o) + " – " + fmt(c) : "Chiuso"}</span>`;
    hoursList.appendChild(li);
  });
}

// Orari dei corsi dentro ogni scheda
document.querySelectorAll("[data-slots]").forEach(ul => {
  const slots = (COURSE_SLOTS[ul.dataset.slots] || []).slice().sort((a, b) => a[0] - b[0] || toMin(a[1]) - toMin(b[1]));
  ul.innerHTML = slots.length
    ? slots.map(([d, s, e]) => `<li><b>${DAY_SHORT[d]}</b> ${fmt(s)}–${fmt(e)}</li>`).join("")
    : `<li><span class="ph">DA INSERIRE: giorni e orari</span></li>`;
});

// Settimana dei corsi, giorno per giorno (da lunedì a venerdì)
const week = document.getElementById("week");
if (week) {
  week.innerHTML = [1, 2, 3, 4, 5].map(d => {
    const items = Object.entries(COURSE_SLOTS)
      .flatMap(([k, slots]) => slots.filter(s => s[0] === d).map(s => [k, s[1], s[2]]))
      .sort((a, b) => toMin(a[1]) - toMin(b[1]));
    const body = items.length
      ? items.map(([k, s, e]) => `<a href="#${k}" class="wk-item" style="--c:${COURSE_COLORS[k]}"><b>${COURSE_NAMES[k]}</b><span>${fmt(s)}–${fmt(e)}</span></a>`).join("")
      : `<span class="wk-none">Nessun corso</span>`;
    return `<div class="wk-day${d === today ? " today" : ""}"><div class="wk-name">${HOURS[d][0]}</div>${body}</div>`;
  }).join("");
  week.addEventListener("click", e => {
    const a = e.target.closest(".wk-item");
    if (!a) return;
    const card = document.getElementById(a.getAttribute("href").slice(1));
    if (!card) return;
    e.preventDefault();
    const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
    card.scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "center" });
    card.classList.remove("flash"); void card.offsetWidth; card.classList.add("flash");
  });
}

// Telefono: link "chiama" sul cellulare
document.querySelectorAll("[data-tel]").forEach(a => {
  if (PHONE) {
    a.href = "tel:" + PHONE.replace(/[^\d+]/g, "");
    if (a.hasAttribute("data-tel-text")) a.textContent = PHONE;
  } else a.addEventListener("click", e => { e.preventDefault(); alert("Numero di telefono ancora da inserire"); });
});

// Pallino del gruppo WhatsApp dei corsi
document.querySelectorAll("[data-wa-group]").forEach(a => {
  if (WHATSAPP_GROUP) { a.href = WHATSAPP_GROUP; a.target = "_blank"; a.rel = "noopener"; }
  else a.addEventListener("click", e => { e.preventDefault(); alert("Link del gruppo WhatsApp ancora da inserire"); });
});

// Menu da telefono
const header = document.querySelector("header");
document.querySelector(".menu-btn").addEventListener("click", () => {
  const open = header.classList.toggle("open");
  document.querySelector(".menu-btn").setAttribute("aria-expanded", open);
  document.documentElement.classList.toggle("menu-open", open);
});

// Sezioni che compaiono scorrendo: solo ciò che all'apertura è fuori dallo schermo,
// così la prima schermata è sempre completa anche senza scorrere.
const REVEAL = ".space-row,.course,.price-group,.person,.wk-day,.outdoor,.band,.hours,.contacts,.req,.rules,#orari > div";
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(entries => {
    let i = 0;
    entries.filter(e => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top || a.boundingClientRect.left - b.boundingClientRect.left)
      .forEach(e => {
        e.target.style.setProperty("--d", Math.min(i++, 5) * 70 + "ms"); // piccola cascata tra elementi vicini
        e.target.classList.add("in");
        io.unobserve(e.target);
      });
  }, { rootMargin: "0px", threshold: 0 });
  document.querySelectorAll(REVEAL).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.top < innerHeight && r.bottom > 0) return; // già visibile: resta com'è
    el.classList.add("reveal");
    io.observe(el);
  });
}

// Mappa interattiva (solo nel sito definitivo, dove viene caricata la libreria Leaflet).
// Se la libreria o la cartografia non arrivano, resta la "cartolina" con il link a Google Maps.
const mapEl = document.getElementById("map");
if (mapEl && window.L) {
  try {
    const lat = +mapEl.dataset.lat, lng = +mapEl.dataset.lng;
    const logo = mapEl.querySelector(".map-pin img").src;
    const gmaps = mapEl.querySelector(".map-card").href;
    mapEl.innerHTML = "";
    mapEl.classList.add("live");
    const map = L.map(mapEl, { scrollWheelZoom: false, dragging: !L.Browser.mobile, tap: false }).setView([lat, lng], 17);
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
      maxZoom: 19,
      attribution: "Immagini &copy; Esri, Maxar, Earthstar Geographics"
    }).addTo(map);
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}", {
      maxZoom: 19
    }).addTo(map);
    const icon = L.divIcon({ className: "logo-pin", html: `<span class="map-pin"><img src="${logo}" alt=""></span>`,
                             iconSize: [64, 78], iconAnchor: [32, 78], popupAnchor: [0, -74] });
    L.marker([lat, lng], { icon, title: "Sport's Center 2", alt: "Sport's Center 2" }).addTo(map)
      .bindPopup(`<b>Sport's Center 2</b><br>Via Cavour 3, Roveleto di Cadeo<br><a href="${gmaps}" target="_blank" rel="noopener">Apri in Google Maps</a>`);
    // se la mappa era nascosta quando è stata creata, la ridisegna quando torna visibile
    window.refreshMap = () => { map.invalidateSize(); map.setView([lat, lng], 17); };
  } catch (e) { /* in caso di errore resta la cartolina */ }
}

// Menu da telefono: si chiude con Esc
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && header.classList.contains("open")) document.querySelector(".menu-btn").click();
});

// Striscia della home: orario di oggi
document.querySelectorAll("[data-today]").forEach(el => {
  const [, o, c] = HOURS[today];
  el.textContent = o ? fmt(o) + " – " + fmt(c) : "Chiuso oggi";
});
