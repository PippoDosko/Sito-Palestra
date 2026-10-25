# Sito Sport's Center 2

Sito della palestra ASD Sport's Center Due Cadeo (Roveleto di Cadeo, PC).

- `src/` contiene le pagine, lo stile (`styles.css`) e lo script (`script.js`). Orari di apertura, orari dei corsi e telefono si modificano in cima a `src/script.js`.
- `python3 build.py` genera il sito nella cartella `docs/`, che è quella pubblicata da GitHub Pages.
- Finché il sito è una bozza, `NOINDEX = True` in `build.py` chiede a Google di non indicizzarlo.
