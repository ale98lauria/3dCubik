<a href="https://ailligence.it" target="_blank">
  <img src="https://ailligence.it/og-image.png" alt="ailligence.it" width="100%">
</a>

<h1 align="center">3D Cubik — Catalogo Prodotti</h1>

<p align="center">
  Catalogo statico per prodotti 3D, hostabile su GitHub Pages o Netlify.<br>
  Pannello admin locale per gestire prodotti e categorie senza backend.
</p>

---

## Indice

- [Struttura del progetto](#struttura-del-progetto)
- [Setup](#setup)
- [Tutorial: aggiungere nuove immagini](#tutorial-aggiungere-nuove-immagini)
- [Tutorial: pannello admin](#tutorial-pannello-admin)
- [Comando di rigenerazione](#comando-di-rigenerazione)
- [Deploy](#deploy)

---

## Struttura del progetto

```
3dcubik/
├── index.html          # Catalogo pubblico (generato)
├── products.json       # Dati prodotti (generato + editabile via admin)
├── sw.js               # Service Worker per cache offline
├── admin.html          # Pannello admin locale
├── build_catalog.py    # Script di generazione
├── imgs/
│   ├── webp/           # Immagini originali (aggiungi qui le nuove)
│   └── thumb/          # Anteprime 320×320 (generate automaticamente)
└── README.md
```

---

## Setup

**Requisiti:** Python 3.10+ e Pillow

```bash
pip install Pillow
```

---

## Tutorial: aggiungere nuove immagini

### Convenzione nomi file

| Formato | Significato |
|---|---|
| `Aereo.webp` | Prodotto con una sola immagine |
| `Aereo__2.webp` | Seconda immagine dello stesso prodotto |
| `Aereo__3.webp` | Terza immagine, ecc. |

I file con lo stesso prefisso vengono raggruppati in un unico prodotto con carosello.

### Passaggi

1. **Copia** i nuovi file `.webp` nella cartella `imgs/webp/`

2. **Esegui** il comando di rigenerazione:
   ```bash
   python3 build_catalog.py
   ```
   Lo script in modalità predefinita:
   - Conserva **tutte** le modifiche fatte tramite il pannello admin (categorie, nomi)
   - Aggiunge i nuovi prodotti trovati su disco con auto-classificazione
   - Genera le anteprime solo per le immagini nuove (le esistenti vengono saltate)
   - Aggiorna `products.json` e `index.html`

3. **Push** i file aggiornati su GitHub (o rideploy su Netlify)

---

## Tutorial: pannello admin

Il pannello admin è un file HTML che gira **interamente in locale**, senza server.  
Le modifiche vengono esportate come `products.json` e poi pushate su GitHub.

### Aprire il pannello

Fai doppio clic su `admin.html` — si apre nel browser.

### Caricare i dati

Clicca **📂 Carica JSON** e seleziona il file `products.json` dalla cartella del progetto.

![Caricamento](https://placehold.co/600x80/111827/ffffff?text=Carica+products.json)

### Modificare un prodotto

1. Clicca l'icona ✏️ sulla riga del prodotto
2. Modifica il **nome** (usa underscore al posto degli spazi: `Hello_Kitty`)
3. Seleziona le **categorie** tramite checkbox
4. Usa **✨ Auto-classifica** per suggerire le categorie dal nome
5. Gestisci le **immagini**: riordina (▲▼), aggiungi percorso, rimuovi
6. Clicca **Salva modifiche**

### Aggiungere un prodotto manuale

1. Clicca **+ Nuovo prodotto**
2. Inserisci nome e categorie
3. Aggiungi il percorso dell'immagine (es. `imgs/webp/NomeProdotto.webp`)
4. Salva

### Eliminare un prodotto

Clicca l'icona 🗑 → conferma nella finestra di dialogo.

### Esportare e aggiornare il sito

1. Clicca **⬇ Esporta JSON**
2. Il browser scarica `products.json`
3. Sostituisci il file nella cartella del progetto
4. Push su GitHub / rideploy su Netlify

> **Importante:** le modifiche fatte nel pannello admin vengono salvate **solo** nel JSON esportato. Dopo l'export, se esegui `python3 build_catalog.py` le modifiche vengono **preservate** automaticamente — lo script legge il JSON esistente e non sovrascrive i prodotti già presenti.

---

## Comando di rigenerazione

### Modalità normale (merge) — **consigliata**

```bash
python3 build_catalog.py
```

Cosa fa:
- Legge `products.json` esistente
- **Preserva** nome, categorie e ordine immagini dei prodotti già presenti
- Aggiunge nuovi prodotti trovati in `imgs/webp/` con auto-classificazione
- Genera anteprime solo per le immagini che non le hanno ancora
- Rigenera `index.html`

### Modalità reset — **attenzione, perde le modifiche admin**

```bash
python3 build_catalog.py --reset
```

Cosa fa:
- Ignora `products.json` esistente
- Ricostruisce tutto da zero leggendo solo i file su disco
- Riclassifica automaticamente tutti i prodotti

Usa `--reset` solo se vuoi ripartire da capo (es. dopo una pulizia massiva dei file).

### Solo anteprime

Per rigenerare le anteprime senza toccare JSON o HTML, basta eseguire lo script e interrompere dopo la fase thumbnail, oppure aggiungere nuovi file e lanciare il comando normale — le anteprime esistenti vengono saltate automaticamente.

---

## Deploy

### GitHub Pages

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TUO_USERNAME/3dcubik.git
git branch -M main
git push -u origin main
```

Poi su GitHub: **Settings → Pages → Branch: main → Save**

Il sito sarà disponibile su: `https://TUO_USERNAME.github.io/3dcubik/`

### Netlify

1. Vai su [netlify.com](https://netlify.com)
2. Trascina la cartella del progetto nell'interfaccia web
3. Il sito viene pubblicato istantaneamente

> **Nota:** la cartella `imgs/webp/` pesa ~150MB. Per Netlify usa il deploy via drag & drop o collega il repository GitHub. Il limite del piano gratuito è 100MB per deploy — valuta di usare GitHub Pages che non ha questo limite.

---

## Workflow completo consigliato

```
Nuove immagini in imgs/webp/
        ↓
python3 build_catalog.py      ← merge automatico, preserva admin edits
        ↓
Verifica in admin.html        ← aggiusta categorie se serve
        ↓
Esporta products.json         ← sovrascrive il file nella cartella
        ↓
git add . && git commit && git push   ← aggiorna il sito live
```

---

<p align="center">
  Realizzato con ❤️ da <a href="https://ailligence.it">ailligence.it</a>
</p>
