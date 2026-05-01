#!/usr/bin/env python3
"""
build_catalog.py — genera catalog.html da imgs/webp/*.webp
"""

import re
import json
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Configurazione
# ---------------------------------------------------------------------------
IMGS_DIR     = Path("imgs/webp")
THUMB_DIR    = Path("imgs/thumb")
ORIGINALS_DIR = Path("imgs/originals")
WATERMARK_FILE = Path("imgs/watermark.png")
WATERMARK_OPACITY = 0.20
WATERMARK_SCALE = 0.45
BACKGROUND_FILE = Path("imgs/3dcubik_example.png")
THUMB_SIZE   = (320, 320)
THUMB_QUALITY = 80
OUTPUT_HTML  = Path("index.html")
OUTPUT_JSON  = Path("products.json")
PER_PAGE = 48

# ---------------------------------------------------------------------------
# Dizionario keyword → categorie
# ---------------------------------------------------------------------------
KEYWORD_MAP = {
    "alfabeto": ["Alfabeto"],
    "lettera": ["Alfabeto"],
    # Alberi (assorbiti in Piante)
    "abete": ["Piante"],
    "albero": ["Piante"],
    "palma": ["Piante"],
    "bonsai": ["Piante"],
    "quercia": ["Piante"],
    "ulivo": ["Piante"],
    # Fiori
    "fiore": ["Fiori"],
    "girasole": ["Fiori"],
    "orchidea": ["Fiori"],
    "rosa": ["Fiori"],
    "tulipano": ["Fiori"],
    "bouquet": ["Fiori"],
    "margherita": ["Fiori"],
    "giglio": ["Fiori"],
    "lavanda": ["Fiori"],
    "mimosa": ["Fiori"],
    "garofano": ["Fiori"],
    # Piante (foglie e altro materiale vegetale)
    "foglia": ["Piante"],
    "agrifoglio": ["Piante"],
    "edera": ["Piante"],
    "fungo": ["Piante"],
    "cactus": ["Piante"],
    "animale": ["Animali"],
    "animali": ["Animali"],
    "savana": ["Animali"],
    "anatroccolo": ["Animali"],
    "ape": ["Animali"],
    "aquila": ["Animali"],
    "cane": ["Animali"],
    "gatto": ["Animali"],
    "coniglio": ["Animali"],
    "elefante": ["Animali"],
    "tigre": ["Animali"],
    "uccello": ["Animali"],
    "pappagallo": ["Animali"],
    "pecora": ["Animali"],
    "mucca": ["Animali"],
    "cavallo": ["Animali"],
    "maiale": ["Animali"],
    "rana": ["Animali"],
    "farfalla": ["Animali"],
    "coccinella": ["Animali"],
    "tartaruga": ["Animali"],
    "lucertola": ["Animali"],
    "serpente": ["Animali"],
    "panda": ["Animali"],
    "koala": ["Animali"],
    "giraffa": ["Animali"],
    "zebra": ["Animali"],
    "riccio": ["Animali"],
    "volpe": ["Animali"],
    "lupo": ["Animali"],
    "drago": ["Animali"],
    "pinguino": ["Animali"],
    "fenicottero": ["Animali"],
    "tucano": ["Animali"],
    "gorilla": ["Animali"],
    "scimmia": ["Animali"],
    "cervo": ["Animali"],
    "criceto": ["Animali"],
    "coccodrillo": ["Animali"],
    "iguana": ["Animali"],
    "camaleonte": ["Animali"],
    "libellula": ["Animali"],
    "lumaca": ["Animali"],
    "rinoceronte": ["Animali"],
    "ippopotamo": ["Animali"],
    "lama": ["Animali"],
    "alpaca": ["Animali"],
    "cammello": ["Animali"],
    "capra": ["Animali"],
    "asino": ["Animali"],
    "labrador": ["Animali"],
    "balena": ["Animali", "Mare"],
    "delfino": ["Animali", "Mare"],
    "squalo": ["Animali", "Mare"],
    "orca": ["Animali", "Mare"],
    "pulcino": ["Animali", "Pasqua"],
    "aereo": ["Viaggi"],
    "aeroplano": ["Viaggi"],
    "nave": ["Viaggi"],
    "treno": ["Viaggi"],
    "camper": ["Viaggi"],
    "mongolfiera": ["Viaggi"],
    "elicottero": ["Viaggi"],
    "razzo": ["Viaggi"],
    "valigia": ["Viaggi"],
    "passaporto": ["Viaggi"],
    "barca": ["Viaggi", "Mare"],
    "bicicletta": ["Viaggi"],
    "bici": ["Viaggi"],
    "timbro": ["Timbri"],
    "mare": ["Mare"],
    "oceano": ["Mare"],
    "polpo": ["Mare"],
    "medusa": ["Mare"],
    "granchio": ["Mare"],
    "stella_marina": ["Mare"],
    "corallo": ["Mare"],
    "sirena": ["Mare"],
    "conchiglia": ["Mare"],
    "aragosta": ["Mare"],
    "gambero": ["Mare"],
    "spiaggia": ["Mare"],
    "ancora": ["Mare"],
    "faro": ["Mare"],
    "sottomarino": ["Mare"],
    "pesce": ["Mare", "Animali"],
    "battesimo": ["Battesimo"],
    "comunione": ["Comunione"],
    "cresima": ["Cresima"],
    "natale": ["Natale"],
    "babbo": ["Natale"],
    "renna": ["Natale"],
    "elfo": ["Natale"],
    "slitta": ["Natale"],
    "ghirlanda": ["Natale"],
    "presepe": ["Natale"],
    "bambino": ["Bambini"],
    "bambina": ["Bambini"],
    "baby": ["Bambini"],
    "neonato": ["Bambini"],
    "bimbo": ["Bambini"],
    "bimba": ["Bambini"],
    "culla": ["Bambini"],
    "carrozzina": ["Bambini"],
    "ciuccio": ["Bambini"],
    "barbie": ["Barbie"],
    "ken": ["Barbie"],
    "batman": ["Supereroi"],
    "superman": ["Supereroi"],
    "spiderman": ["Supereroi"],
    "capitan_america": ["Supereroi"],
    "iron_man": ["Supereroi"],
    "thor": ["Supereroi"],
    "hulk": ["Supereroi"],
    "wonder_woman": ["Supereroi"],
    "avengers": ["Supereroi"],
    "deadpool": ["Supereroi"],
    "wolverine": ["Supereroi"],
    "groot": ["Supereroi"],
    "pantera_nera": ["Supereroi"],
    "fumetto": ["Supereroi"],
    "fumetti": ["Supereroi"],
    "disney": ["Disney"],
    "paperino": ["Disney"],
    "pluto": ["Disney"],
    "pippo": ["Disney"],
    "cenerentola": ["Disney"],
    "biancaneve": ["Disney"],
    "ariel": ["Disney"],
    "sirenetta": ["Disney"],
    "rapunzel": ["Disney"],
    "mulan": ["Disney"],
    "pocahontas": ["Disney"],
    "bambi": ["Disney"],
    "dumbo": ["Disney"],
    "pinocchio": ["Disney"],
    "winnie": ["Winnie The Pooh", "Disney"],
    "pooh": ["Winnie The Pooh", "Disney"],
    "lilo": ["Disney", "Stitch"],
    "nemo": ["Disney"],
    "dory": ["Disney", "Mare"],
    "buzz": ["Disney"],
    "woody": ["Disney"],
    "toy_story": ["Disney"],
    "coco": ["Disney"],
    "encanto": ["Disney"],
    "alice": ["Disney"],
    "peter_pan": ["Disney"],
    "trilli": ["Disney"],
    "trilly": ["Disney"],
    "aladdin": ["Disney"],
    "tarzan": ["Disney"],
    "aurora": ["Disney"],
    "gaston": ["Disney"],
    "jasmine": ["Disney"],
    "bella_bestia": ["Disney", "Bella e Bestia"],
    "bella_specchio": ["Disney", "Bella e Bestia"],
    "belle_scomponibile": ["Disney", "Bella e Bestia"],
    "bestia": ["Disney", "Bella e Bestia"],
    "cappuccetto": ["Bambini"],
    "inside_out": ["Disney", "Inside Out"],
    "principesse": ["Disney", "Principesse"],
    "carrozza": ["Disney", "Principesse"],
    "aristogatti": ["Disney", "Animali"],
    "carica_101": ["Disney", "Carica 101"],
    "zootropolis": ["Disney", "Zootropolis", "Animali"],
    "zootopia": ["Disney", "Zootropolis", "Animali"],
    "dalmata": ["Disney", "Animali"],
    "bing": ["Bing"],
    "calcio": ["Sport"],
    "basket": ["Sport"],
    "tennis": ["Sport"],
    "pallavolo": ["Sport"],
    "nuoto": ["Sport"],
    "boxe": ["Sport"],
    "karate": ["Sport"],
    "golf": ["Sport"],
    "rugby": ["Sport"],
    "football": ["Sport"],
    "pallone": ["Sport"],
    "pattinaggio": ["Sport"],
    "sci": ["Sport"],
    "snowboard": ["Sport"],
    "surf": ["Sport"],
    "skateboard": ["Sport"],
    "danza": ["Sport"],
    "ginnastica": ["Sport"],
    "baseball": ["Sport"],
    "casa": ["Case"],
    "case": ["Case"],
    "casetta": ["Case"],
    "villetta": ["Case"],
    "castello": ["Case"],
    "pizza": ["Cibo"],
    "bottiglia": ["Cibo"],
    "candy_cane": ["Natale", "Cibo"],
    "biglietto": ["Cinema"],
    "fiocchetto": ["Fiocchi"],
    "cavalli": ["Animali"],
    "osso": ["Animali"],
    "neve": ["Natale"],
    "tiktok": ["Musica"],
    "mappamondo": ["Viaggi"],
    "quadrato": ["Cornici"],
    "cavalluccio_marino": ["Animali", "Mare"],
    "torta": ["Cibo"],
    "gelato": ["Cibo"],
    "dolce": ["Cibo"],
    "biscotto": ["Cibo"],
    "bottiglia":["Cibo"],
    "cioccolato": ["Cibo"],
    "fragola": ["Cibo"],
    "anguria": ["Cibo"],
    "ciliegia": ["Cibo"],
    "mela": ["Cibo"],
    "arancia": ["Cibo"],
    "limone": ["Cibo"],
    "banana": ["Cibo"],
    "ananas": ["Cibo"],
    "cupcake": ["Cibo"],
    "muffin": ["Cibo"],
    "hamburger": ["Cibo"],
    "sushi": ["Cibo"],
    "pane": ["Cibo"],
    "frutta": ["Cibo"],
    "verdura": ["Cibo"],
    "carota": ["Cibo"],
    "pomodoro": ["Cibo"],
    "melone": ["Cibo"],
    "uva": ["Cibo"],
    "kiwi": ["Cibo"],
    "mango": ["Cibo"],
    "caramella": ["Cibo"],
    "lecca_lecca": ["Cibo"],
    "donut": ["Cibo"],
    "macaron": ["Cibo"],
    "waffle": ["Cibo"],
    "pancake": ["Cibo"],
    "popcorn": ["Cibo", "Cinema"],
    "giocattolo": ["Giocattoli"],
    "pupazzo": ["Giocattoli"],
    "palloncino": ["Giocattoli"],
    "peluche": ["Giocattoli"],
    "bambola": ["Giocattoli"],
    "aquilone": ["Giocattoli"],
    "cocomelon": ["Cocomelon"],
    "matrimonio": ["Matrimonio"],
    "sposi": ["Matrimonio"],
    "wedding": ["Matrimonio"],
    "fedi": ["Matrimonio"],
    "sposa": ["Matrimonio"],
    "pasqua": ["Pasqua"],
    "uovo": ["Pasqua"],
    "colomba": ["Pasqua", "Animali"],
    "cornice": ["Cornici"],
    "frame": ["Cornici"],
    "dinosauro": ["Dinosauri"],
    "dino": ["Dinosauri"],
    "t_rex": ["Dinosauri"],
    "triceratopo": ["Dinosauri"],
    "pterodattilo": ["Dinosauri"],
    "velociraptor": ["Dinosauri"],
    "fiocco": ["Fiocchi"],
    "nastro": ["Fiocchi"],
    "archetto": ["Fiocchi"],
    "frozen": ["Frozen"],
    "elsa": ["Frozen"],
    "olaf": ["Frozen"],
    "kristoff": ["Frozen"],
    "halloween": ["Halloween"],
    "zucca": ["Halloween"],
    "fantasma": ["Halloween"],
    "strega": ["Halloween"],
    "scheletro": ["Halloween"],
    "pipistrello": ["Halloween"],
    "ragnatela": ["Halloween"],
    "zombie": ["Halloween"],
    "vampiro": ["Halloween"],
    "harry_potter": ["Harry Potter"],
    "hogwarts": ["Harry Potter"],
    "hermione": ["Harry Potter"],
    "quidditch": ["Harry Potter"],
    "hello_kitty": ["Hello Kitty"],
    "kitty": ["Hello Kitty"],
    "macchina": ["Viaggi"],
    "automobile": ["Viaggi"],
    "ferrari": ["Viaggi"],
    "lamborghini": ["Viaggi"],
    "monster_truck": ["Viaggi"],
    "trattore": ["Viaggi"],
    "camion": ["Viaggi"],
    "autobus": ["Viaggi"],
    "ambulanza": ["Viaggi"],
    "pompieri": ["Viaggi"],
    "polizia": ["Viaggi"],
    "ruspa": ["Viaggi"],
    "escavatore": ["Viaggi"],
    "scooter": ["Viaggi"],
    "moto": ["Viaggi"],
    "laurea": ["Laurea"],
    "diploma": ["Laurea"],
    "dottorato": ["Laurea"],
    "mamma": ["Festa della Mamma"],
    "madre": ["Festa della Mamma"],
    "frida_khalo": ["Festa della Donna"],
    "frida": ["Festa della Donna"],
    "masha": ["Masha e Orso"],
    "nonno": ["Festa dei Nonni"],
    "nonna": ["Festa dei Nonni"],
    "nonni": ["Festa dei Nonni"],
    "numero": ["Numeri"],
    "oceania": ["Oceania", "Disney"],
    "moana": ["Oceania", "Disney"],
    "maui": ["Oceania"],
    "orsetto": ["Orsetti"],
    "orsetti": ["Orsetti"],
    "teddy": ["Orsetti"],
    "orsacchiotto": ["Orsetti"],
    "peppa": ["Peppa Pig"],
    "musica": ["Musica"],
    "chitarra": ["Musica"],
    "violino": ["Musica"],
    "tromba": ["Musica"],
    "sassofono": ["Musica"],
    "microfono": ["Musica"],
    "cuffie": ["Musica"],
    "vinile": ["Musica"],
    "acdc": ["Musica"],
    "beatles": ["Musica"],
    "pentagramma": ["Musica"],
    "nota_musicale": ["Musica"],
    "pjmask": ["PJmask"],
    "pj_mask": ["PJmask"],
    "pigiamini": ["PJmask"],
    "cinema": ["Cinema"],
    "ciak": ["Cinema"],
    "pellicola": ["Cinema"],
    "re_leone": ["Re Leone", "Disney"],
    "simba": ["Re Leone", "Disney"],
    "mufasa": ["Re Leone"],
    "timon": ["Re Leone"],
    "pumba": ["Re Leone"],
    "trucco": ["Trucchi"],
    "makeup": ["Trucchi"],
    "rossetto": ["Trucchi"],
    "smalto": ["Trucchi"],
    "profumo": ["Trucchi"],
    "cipria": ["Trucchi"],
    "sonic": ["Sonic"],
    "knuckles": ["Sonic"],
    "eggman": ["Sonic"],
    "stitch": ["Stitch", "Disney"],
    "stray_kids": ["Stray Kids"],
    "straykids": ["Stray Kids"],
    "mario": ["Super Mario"],
    "luigi": ["Super Mario"],
    "bowser": ["Super Mario"],
    "yoshi": ["Super Mario"],
    "koopa": ["Super Mario"],
    "wario": ["Super Mario"],
    "texture": ["Texture"],
    "pattern": ["Texture"],
    "topolino": ["Topolino", "Disney"],
    "mickey": ["Topolino", "Disney"],
    "minnie": ["Topolino", "Disney"],
    "topper": ["Topper"],
    "unicorno": ["Unicorni"],
    "unicorn": ["Unicorni"],
    "pegaso": ["Unicorni"],
    "vestito": ["Vestiti"],
    "abito": ["Vestiti"],
    "gonna": ["Vestiti"],
    "felpa": ["Vestiti"],
    "maglione": ["Vestiti"],
    "cappotto": ["Vestiti"],
    "costume": ["Vestiti"],
    "tutina": ["Vestiti"],
    "pigiama": ["Vestiti"],
    # --- keywords aggiuntive per ridurre "Altro" ---
    "arcobaleno": ["Bambini", "Unicorni"],
    "baby_body": ["Bambini", "Vestiti"],
    "baby_shark": ["Bambini", "Animali"],
    "ballerina": ["Sport", "Bambini"],
    "ballerine": ["Sport"],
    "coniglietto": ["Animali", "Pasqua"],
    "cigno": ["Animali"],
    "gallina": ["Animali", "Pasqua"],
    "gattino": ["Animali"],
    "elefantino": ["Animali"],
    "elefantini": ["Animali"],
    "cavalluccio": ["Animali"],
    "oca": ["Animali"],
    "leone": ["Animali"],
    "stranger_things": ["Cinema"],
    "squid_game": ["Cinema"],
    "grinch": ["Natale"],
    "schiaccianoci": ["Natale"],
    "natalizio": ["Natale"],
    "pandizenzero": ["Natale"],
    "timbri": ["Timbri"],
    "numeri_bombati": ["Numeri"],
    "numeri_sottili": ["Numeri"],
    "cuore": ["Matrimonio"],
    "cuori": ["Matrimonio"],
    "spumante": ["Matrimonio", "Compleanno"],
    "flute": ["Matrimonio"],
    "fedi": ["Matrimonio"],
    "sposo": ["Matrimonio"],
    "mr&mrs": ["Matrimonio"],
    "champagne": ["Matrimonio", "Compleanno"],
    "wedding": ["Matrimonio"],
    "croce": ["Battesimo", "Comunione", "Cresima"],
    "case_composizione": ["Case"],
    "fattoria": ["Case", "Animali"],
    "fienile": ["Case"],
    "vetrina_negozio": ["Case"],
    "moulin_rouge": ["Cinema"],
    "moulen_rouge": ["Cinema"],
    "joystick": ["Giocattoli"],
    "puzzle": ["Giocattoli"],
    "dondolo": ["Giocattoli"],
    "sonaglino": ["Bambini", "Giocattoli"],
    "bieberon": ["Bambini"],
    "passeggino": ["Bambini"],
    "culla": ["Bambini"],
    "fiocchi": ["Fiocchi"],
    "fragole": ["Cibo"],
    "crostata": ["Cibo"],
    "polpetta": ["Cibo"],
    "marmellata": ["Cibo"],
    "gelatino": ["Cibo"],
    "tamburo": ["Musica"],
    "cassetta": ["Musica"],
    "vespa": ["Viaggi"],
    "jeep": ["Viaggi"],
    "treruote": ["Viaggi"],
    "insegne_stradali": ["Viaggi"],
    "mongolfiera": ["Viaggi"],
    "valigie": ["Viaggi"],
    "kimono": ["Vestiti"],
    "maglia_tshirt": ["Vestiti"],
    "giacca": ["Vestiti"],
    "vestitino": ["Vestiti"],
    "guanto": ["Vestiti"],
    "guanti": ["Vestiti"],
    "cappello": ["Vestiti"],
    "wonderwoman": ["Supereroi"],
    "quadrifoglio": ["Piante"],
    "foglie": ["Piante"],
    "funghetto": ["Piante"],
    "funghi": ["Piante"],
    "fiori": ["Fiori"],
    "corallo": ["Mare"],
    "spirale_acqua": ["Mare"],
    "onde": ["Mare"],
    "palla_neve": ["Natale"],
    "elfo": ["Natale"],
    "renna": ["Natale"],
    "demogorgone": ["Cinema"],
    "stirch": ["Stitch", "Disney"],
    "angel": ["Stitch", "Disney"],
    "knuckles": ["Sonic"],
    "eggman": ["Sonic"],
    # ulteriori
    "orso_viso": ["Orsetti"],
    "orso_nuvola": ["Orsetti"],
    "orso": ["Orsetti"],
    "corona": ["Unicorni"],           # corona è tipica unicorni/principesse
    "zucche": ["Halloween"],
    "palloncini": ["Giocattoli"],
    "pacco_regalo": ["Fiocchi", "Natale"],
    "pacchi_regalo": ["Fiocchi", "Natale"],
    "carote": ["Cibo"],
    "pera": ["Cibo"],
    "prugna": ["Cibo"],
    "farfalle": ["Animali"],
    "circo": ["Bambini"],
    "nuvola": ["Bambini"],
    "nuvoletta": ["Bambini"],
    "happy_birthday": ["Compleanno"],
    "birthday": ["Compleanno"],
    "compleanno": ["Compleanno"],
    "love": ["Matrimonio"],
    "labbra": ["Trucchi"],
    "circo_giostra": ["Bambini"],
    "uno": ["Bambini"],
    "one": ["Bambini"],
    "tazza": ["Cibo"],
    "lanterna": ["Natale"],
    "texrture": ["Texture"],
    "orologio": ["Vestiti"],
    "scarpa": ["Vestiti"],
    "occhiali": ["Vestiti"],
    "corsetto": ["Vestiti"],
    "sciarpa": ["Vestiti"],
    "libro": ["Laurea"],
    "libri": ["Laurea"],
    "matita": ["Bambini"],
    "matite": ["Bambini"],
    # Lusso
    "chanel": ["Lusso"],
    "gucci": ["Lusso"],
    "prada": ["Lusso"],
    "versace": ["Lusso"],
    "dior": ["Lusso"],
    "louis_vuitton": ["Lusso"],
    "vuitton": ["Lusso"],
    "hermes": ["Lusso"],
    "rolex": ["Lusso"],
    "balenciaga": ["Lusso"],
    "fendi": ["Lusso"],
    "armani": ["Lusso"],
    "valentino": ["Lusso"],
    "cartier": ["Lusso"],
    "bulgari": ["Lusso"],
    "tiffany": ["Lusso"],
}

# Ordine delle keyword: le più lunghe prima, per evitare falsi match su
# keyword corte contenute in keyword più lunghe (es. "moto" dentro "mongolfiera").
# Per sicurezza ordiniamo per lunghezza decrescente al momento del match.
SORTED_KEYWORDS = sorted(KEYWORD_MAP.keys(), key=len, reverse=True)


# ---------------------------------------------------------------------------
# Funzione di classificazione
# ---------------------------------------------------------------------------
def normalize(filename: str) -> str:
    """
    Normalizza il filename per il matching:
    - rimuove estensione .webp
    - rimuove suffissi __N (varianti)
    - converte in lowercase
    - sostituisce spazi con _
    """
    stem = Path(filename).stem          # rimuove .webp
    stem = re.sub(r"__\d+$", "", stem)  # rimuove __N finale
    stem = stem.lower()
    stem = stem.replace(" ", "_")
    return stem


def classify(filename: str) -> list[str]:
    """Restituisce lista di categorie per il filename dato."""
    stem = normalize(filename)
    cats: set[str] = set()

    for kw in SORTED_KEYWORDS:
        if kw in stem:
            cats.update(KEYWORD_MAP[kw])

    # "timbro riverso/riversi" è un prodotto diverso dai timbri: se il nome
    # contiene la radice "rivers", rimuovi la categoria Timbri auto-assegnata.
    if "rivers" in stem:
        cats.discard("Timbri")

    # "cane" come keyword (Animali) matcha come substring in candy_cane,
    # biancaneve, ecc. Rimuovi Animali per questi falsi positivi.
    if "candy" in stem or "biancaneve" in stem:
        cats.discard("Animali")

    # "biancaneve" contiene anche "neve" → matcha Natale (falso positivo).
    if "biancaneve" in stem:
        cats.discard("Natale")

    # "cappuccetto_rosso" contiene "osso" → matcha Animali (falso positivo).
    if "rosso" in stem:
        cats.discard("Animali")

    # "papera" contiene "pera" → matcha Cibo (falso positivo).
    if "papera" in stem:
        cats.discard("Cibo")

    # "ingranaggio" contiene "rana" → matcha Animali (falso positivo).
    if "ingranaggio" in stem:
        cats.discard("Animali")

    # Pattern "Animale_con_Decorazione": la decorazione dopo "_con_" non
    # è la categoria primaria, è un dettaglio del prodotto animale.
    if "_con_" in stem and "Animali" in cats:
        after = stem.split("_con_", 1)[1]
        cats.discard("Fiori")  # Cigno_con_Rosa, Coniglietto_con_Fiori
        if "palloncin" in after:
            cats.discard("Giocattoli")  # Elefantino_con_Palloncini
        if "cappello" in after:
            cats.discard("Vestiti")  # Oca/Papera_con_Cappello
        if "fiocco" in after:
            cats.discard("Fiocchi")  # Oca/Papera_con_Fiocco

    # Animali in fattoria: "fattoria" → Case+Animali, ma per i prodotti
    # animali specifici la categoria primaria è solo Animali. Eccezioni:
    # fienile e staccionata che restano sia Animali che Case.
    if "Animali" in cats and "Case" in cats and "fienile" not in stem and "staccionata" not in stem:
        cats.discard("Case")

    # "leone" finisce con "one" (matcha Bambini) — vale per qualsiasi
    # leone, non solo Re Leone. Stesso falso positivo per altri prodotti
    # che finiscono in -one (composizione, demogorgone, pozione) e
    # per "alfabeto_circo" (matcha "circo" → Bambini ma è alfabeto).
    if any(x in stem for x in ("leone", "composizione", "demogorgone", "pozione", "alfabeto", "limone", "maglione")):
        cats.discard("Bambini")

    # I baby body con tema decorativo (es. arcobaleno) sono Vestiti per
    # bambini, non vanno categorizzati come Unicorni.
    if "baby_body" in stem:
        cats.discard("Unicorni")

    # Prodotti che iniziano con "comunione" + croce: la croce è un dettaglio,
    # il prodotto è di Comunione, non di Battesimo né Cresima.
    if stem.startswith("comunione") and "croce" in stem:
        cats.discard("Battesimo")
        cats.discard("Cresima")

    # Prodotti Bing con accessorio cibo (es. carote): primario è Bing.
    if "Bing" in cats:
        cats.discard("Cibo")

    # "_con_fiori"/"_con_fiore"/"_con_fiorellini": il fiore è una decorazione,
    # il prodotto principale non è un fiore.
    if "_con_fior" in stem:
        cats.discard("Fiori")

    # "fiorellini" sono dettagli decorativi (cf. Texture_Fiorellini), non
    # prodotti della cat Fiori.
    if "fiorellini" in stem:
        cats.discard("Fiori")

    # "unicorno_torta" è un prodotto a tema unicorno (template/cutter),
    # non un prodotto generico Cibo.
    if "unicorno_torta" in stem:
        cats.discard("Cibo")

    # "corsetto" contiene "orsetto" → falso positivo Orsetti.
    if "corsetto" in stem:
        cats.discard("Orsetti")

    # I prodotti che iniziano con "targa" sono targhette (Cornici). Per gli
    # altri "X_targa" la categoria primaria è X (es. Mongolfiera_targa).
    if stem.startswith("targa"):
        cats.add("Cornici")

    # "Pupazzo di Neve" è un prodotto natalizio, non un Giocattolo generico.
    if "pupazzo_di_neve" in stem:
        cats.discard("Giocattoli")

    # "Cappello parlante" è il cappello di Harry Potter, non un vestito.
    if "cappello_parlante" in stem:
        cats.discard("Vestiti")

    # "wonder" contiene "onde" → falso positivo Mare.
    if "wonder" in stem:
        cats.discard("Mare")

    # "espositore" contiene "sposi" → falso positivo Matrimonio.
    # Va in Vestiti + Bambini (è un porta-biscotti come appendiabiti).
    if "espositore" in stem:
        cats.discard("Matrimonio")
        cats.add("Vestiti")
        cats.add("Bambini")

    # "Hello Kitty Cuore" non è un prodotto Matrimonio.
    if "hello_kitty_cuore" in stem:
        cats.discard("Matrimonio")

    # "Occhio di bue cuore" va anche in Bambini.
    if "occhio_di_bue" in stem:
        cats.add("Bambini")

    # "sciarpa" contiene "sci" → falso positivo Sport.
    if "sciarpa" in stem:
        cats.discard("Sport")

    # I prodotti che iniziano con "Texture_" appartengono solo a Texture,
    # qualunque sia il soggetto rappresentato (foglie/onde/farfalle/ecc.).
    if stem.startswith("texture") or stem.startswith("texrture"):
        cats.clear()
        cats.add("Texture")

    # Categorie aggiuntive per timbri specifici.
    if "timbro_ramo" in stem:
        cats.add("Piante")
    if "timbro_promessa" in stem:
        cats.add("Matrimonio")
    if "pi_greco" in stem or "one_timbro" in stem:
        cats.add("Numeri")

    # "mongolfiera" contiene "golf" → falso positivo Sport.
    if "mongolfiera" in stem:
        cats.discard("Sport")

    # "Polizia Distintivo" è il distintivo di Judy Hopps in Zootropolis.
    if "polizia_distintivo" in stem:
        cats.discard("Viaggi")
        cats.add("Zootropolis")
        cats.add("Disney")

    # "Barbie_set_Topper": rimuovi cat Topper (resta solo Barbie).
    if "barbie_set_topper" in stem:
        cats.discard("Topper")

    # "Orsetto Aviatore con Aereo" è un orsetto, non un prodotto Viaggi.
    if "orsetto_aviatore" in stem:
        cats.discard("Viaggi")

    # Lettere decorative per matrimonio (con foglia/foglie → no Piante).
    if "lettera_con_foglia" in stem or "lettera__con_foglia" in stem or "lettera_con_foglie" in stem:
        cats.discard("Piante")
        cats.add("Matrimonio")
    if "lettera_busta" in stem or "lettera_mamma" in stem:
        cats.add("Matrimonio")

    # Sub-categorie di Bambini: i prodotti delle sub-cat ricevono anche la
    # categoria "Bambini" parent.
    BAMBINI_CHILDREN = {"Barbie", "Bing", "Cocomelon", "Dinosauri",
                        "Hello Kitty", "Masha e Orso", "Orsetti", "Peppa Pig",
                        "PJmask", "Sonic", "Super Mario", "Supereroi",
                        "Unicorni"}
    if cats & BAMBINI_CHILDREN:
        cats.add("Bambini")
    # Re Leone: i personaggi del franchise non sono animali generici.
    if "Re Leone" in cats:
        cats.discard("Animali")

    # "treruote" è un veicolo (Ape Car a 3 ruote), il match "ape" → Animali
    # è un falso positivo.
    if "treruote" in stem:
        cats.discard("Animali")

    # Topolino: "paperino"/"paperina" contengono "ape" (matcha Animali);
    # accessori del personaggio (guanto/cappello) non sono "Vestiti" generici.
    if "Topolino" in cats:
        cats.discard("Animali")
        cats.discard("Vestiti")

    # "X_con_cornice" non è una cornice ma un prodotto X decorato con
    # cornice (es. Frozen_Logo_con_Cornice). Solo i prodotti che iniziano
    # con "cornice" sono effettivamente nella cat Cornici.
    if "_con_cornice" in stem and not stem.startswith("cornice"):
        cats.discard("Cornici")

    # I personaggi Zootropolis sono Disney/Zootropolis, non Animali generici.
    if "Zootropolis" in cats:
        cats.discard("Animali")

    # "cocomelon" inizia con "coco" (film Disney) → falso positivo.
    if "cocomelon" in stem:
        cats.discard("Disney")

    # Prodotti Comunione: "calice" contiene "alice" (Disney falso positivo)
    # e "comunione" finisce con "one" (Bambini falso positivo).
    if "Comunione" in cats:
        cats.discard("Disney")
        cats.discard("Bambini")

    # Carica 101: i dalmata sono personaggi del franchise, non Animali generici.
    if "Carica 101" in cats:
        cats.discard("Animali")

    # "carrozza_zucca" è la carrozza di Cenerentola (Disney), non Halloween.
    if "carrozza_zucca" in stem:
        cats.discard("Halloween")

    # "_con_targa" è una targhetta decorativa (es. con il nome), non un veicolo.
    if "_con_targa" in stem:
        cats.discard("Viaggi")

    # "Mamma Natale" è un personaggio natalizio, non un prodotto per festa
    # della mamma.
    if "mamma_natale" in stem:
        cats.discard("Festa della Mamma")

    # "_con_fiocco" è una decorazione, il prodotto principale non è un fiocco.
    # Eccezione: i prodotti che iniziano con "cornice" mantengono Fiocchi
    # perché la cornice è proprio a forma di fiocco.
    if "_con_fiocco" in stem and not stem.startswith("cornice"):
        cats.discard("Fiocchi")

    # "Fiocco/Fiocchi di Neve" sono fiocchi di neve (Natale), non decorazioni.
    if "fiocco_di_neve" in stem or "fiocchi_di_neve" in stem:
        cats.discard("Fiocchi")

    return sorted(cats) if cats else ["Altro"]


# ---------------------------------------------------------------------------
# Costruzione catalogo prodotti
# ---------------------------------------------------------------------------
def _group_files() -> dict:
    """Raggruppa i file .webp per chiave prodotto (stem senza __N)."""
    from collections import defaultdict
    files = sorted(IMGS_DIR.glob("*.webp"), key=lambda p: p.name.lower())
    groups: dict[str, list[str]] = defaultdict(list)
    for f in files:
        key = re.sub(r"__\d+$", "", f.stem)
        groups[key].append(f.name)
    return groups


def _sort_imgs(names: list[str]) -> list[str]:
    """Ordina le immagini di un prodotto per suffisso numerico."""
    return sorted(names, key=lambda n: (
        int(re.search(r"__(\d+)$", Path(n).stem).group(1))
        if re.search(r"__(\d+)$", Path(n).stem) else 0
    ))


def load_existing_products() -> dict[str, dict]:
    """Carica products.json esistente come dizionario {name: product}."""
    if not OUTPUT_JSON.exists():
        return {}
    try:
        data = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return {}
        return {p["n"]: p for p in data if "n" in p}
    except Exception as e:
        print(f"Attenzione: impossibile leggere {OUTPUT_JSON}: {e}")
        return {}


def build_products(existing: dict[str, dict] | None = None) -> list[dict]:
    """
    Costruisce la lista prodotti.

    Se `existing` è fornito (modalità merge):
    - Conserva nome, categorie e ordine immagini dei prodotti già presenti
    - Aggiunge le immagini nuove trovate su disco ai prodotti esistenti
    - Crea nuovi prodotti per le chiavi non ancora presenti

    Se `existing` è None (modalità reset):
    - Ricostruisce tutto da zero con auto-classificazione
    """
    groups = _group_files()
    products = []

    for key in sorted(groups.keys(), key=str.lower):
        imgs_sorted = _sort_imgs(groups[key])
        full_paths = [f"imgs/webp/{n}" for n in imgs_sorted]

        if existing is not None and key in existing:
            # ── Prodotto esistente: preserva le modifiche dell'admin ──
            p = dict(existing[key])
            existing_set = set(p["i"])
            new_imgs = [img for img in full_paths if img not in existing_set]
            if new_imgs:
                p["i"] = p["i"] + new_imgs
                print(f"  ↳ {len(new_imgs)} nuova/e immagine/i aggiunta/e a '{key}'")
            products.append(p)
        else:
            # ── Nuovo prodotto: auto-classificazione ──
            categories = classify(key + ".webp")
            products.append({"n": key, "i": full_paths, "c": categories})
            if existing is not None:
                print(f"  ✦ Nuovo prodotto: '{key}' → {categories}")

    return products


# ---------------------------------------------------------------------------
# Generazione thumbnail
# ---------------------------------------------------------------------------
def _apply_watermark_to_image(img, wm):
    """Sovrappone il pattern watermark a tutta l'immagine, semitrasparente.
    Mantiene l'alpha dell'originale per preservare la trasparenza nel WebP."""
    from PIL import Image
    img = img.convert("RGBA")
    w, h = img.size
    wm_resized = wm.resize((w, h), Image.LANCZOS).convert("RGBA")
    alpha = wm_resized.split()[-1].point(lambda p: int(p * WATERMARK_OPACITY))
    wm_resized.putalpha(alpha)
    img.alpha_composite(wm_resized)
    return img


def apply_watermarks() -> None:
    """Applica filigrana ai webp, una sola volta. Backup originali in imgs/originals/."""
    if not BACKGROUND_FILE.exists():
        return
    from PIL import Image
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    wm = Image.open(BACKGROUND_FILE).convert("RGBA")
    files = sorted(IMGS_DIR.glob("*.webp"))
    processed = 0
    for src in files:
        backup = ORIGINALS_DIR / src.name
        if backup.exists():
            continue
        shutil.copy2(src, backup)
        try:
            with Image.open(src) as orig:
                watermarked = _apply_watermark_to_image(orig, wm)
                watermarked.save(src, "WEBP", quality=85, method=4)
        except Exception as e:
            print(f"  Errore watermark {src.name}: {e}")
            shutil.copy2(backup, src)  # ripristina in caso di errore
            continue
        processed += 1
        if processed % 200 == 0:
            print(f"  {processed} watermark applicati...")
    if processed:
        print(f"Watermark applicato a {processed} nuove immagini (backup in {ORIGINALS_DIR})")


def generate_thumbnails() -> None:
    from PIL import Image
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(IMGS_DIR.glob("*.webp"))
    valid_names = {f.name for f in files}
    orphans = 0
    for thumb in THUMB_DIR.glob("*.webp"):
        if thumb.name not in valid_names:
            thumb.unlink()
            orphans += 1
    if orphans:
        print(f"Thumbnail orfane rimosse: {orphans}")
    skipped = 0
    for i, src in enumerate(files, 1):
        dst = THUMB_DIR / src.name
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            continue
        try:
            with Image.open(src) as img:
                img.thumbnail(THUMB_SIZE, Image.LANCZOS)
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode in ("RGBA", "LA", "PA"):
                    bg.paste(img, mask=img.split()[-1])
                else:
                    bg.paste(img.convert("RGB"))
                bg.save(dst, "WEBP", quality=THUMB_QUALITY, method=4)
        except Exception as e:
            print(f"  Errore {src.name}: {e}")
        if i % 200 == 0:
            print(f"  {i}/{len(files)} thumbnail...")
    generated = len(files) - skipped
    print(f"Thumbnail: {generated} generate, {skipped} già aggiornate → {THUMB_DIR}")


# ---------------------------------------------------------------------------
# Statistiche
# ---------------------------------------------------------------------------
def print_stats(products: list[dict]) -> None:
    total = len(products)
    cats_used: set[str] = set()
    no_cat = 0
    for p in products:
        cats_used.update(p["c"])
        if p["c"] == ["Altro"]:
            no_cat += 1

    print(f"Prodotti totali   : {total}")
    print(f"Categorie usate   : {len(cats_used)}")
    print(f"Senza categoria   : {no_cat}")
    if no_cat:
        print("\nProdotti in 'Altro':")
        for p in products:
            if p["c"] == ["Altro"]:
                print(f"  - {p['n']}")


# ---------------------------------------------------------------------------
# Generazione HTML
# ---------------------------------------------------------------------------
ALL_CATEGORIES = [
    "Alfabeto", "Altro", "Animali", "Bambini", "Barbie", "Battesimo",
    "Bella e Bestia", "Bing", "Carica 101", "Case", "Cibo", "Cinema",
    "Cocomelon", "Compleanno", "Comunione", "Cornici", "Cresima", "Dinosauri",
    "Disney",
    "Festa dei Nonni", "Festa della Donna", "Festa della Mamma", "Fiocchi",
    "Fiori", "Frozen", "Giocattoli", "Halloween", "Harry Potter", "Hello Kitty",
    "Inside Out", "Laurea", "Lusso", "Mare", "Masha e Orso", "Matrimonio",
    "Musica", "Natale",
    "Numeri", "Oceania", "Orsetti", "Pasqua", "Peppa Pig", "Piante", "PJmask",
    "Principesse", "Re Leone", "Sonic", "Sport", "Stitch", "Stray Kids",
    "Super Mario", "Supereroi", "Texture", "Timbri", "Topolino", "Topper",
    "Trucchi", "Unicorni", "Vestiti", "Viaggi", "Winnie The Pooh",
    "Zootropolis",
]


def generate_html() -> str:
    categories_json = json.dumps(ALL_CATEGORIES, ensure_ascii=False, separators=(",", ":"))

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>3dCubik — Catalogo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* ===== RESET & VARIABLES ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --dark: #111827;
  --accent: #4f46e5;
  --light: #f9fafb;
  --white: #ffffff;
  --radius: 10px;
  --shadow: 0 2px 8px rgba(0,0,0,0.10);
  --shadow-hover: 0 6px 20px rgba(0,0,0,0.18);
  --sidebar-w: 220px;
  --topbar-h: 56px;
}}

body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--light);
  color: var(--dark);
  min-height: 100vh;
}}

/* ===== SIDEBAR ===== */
.sidebar {{
  position: fixed;
  top: 0; left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  background: var(--dark);
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow: hidden;
  transition: transform .25s ease;
}}
.sidebar.collapsed {{ transform: translateX(-100%); }}
.btn-sidebar-toggle {{
  position: fixed;
  top: 14px;
  left: calc(var(--sidebar-w) - 14px);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--white);
  color: #fff;
  cursor: pointer;
  z-index: 110;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  box-shadow: 0 2px 6px rgba(0,0,0,.25);
  transition: left .25s ease, transform .25s ease;
}}
.btn-sidebar-toggle.collapsed {{ left: 14px; transform: rotate(180deg); }}
.btn-sidebar-toggle svg {{ width: 14px; height: 14px; }}
.sidebar-logo {{
  padding: 18px 16px 14px;
  font-family: 'Montserrat', sans-serif;
  font-size: 1.6rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--white);
  border-bottom: 1px solid rgba(255,255,255,.08);
  flex-shrink: 0;
}}
.sidebar-logo span {{ color: var(--white); }}
.sidebar-search {{
  padding: 10px 12px;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255,255,255,.07);
}}
.sidebar-search input {{
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,.15);
  background: rgba(255,255,255,.07);
  color: var(--white);
  font-size: .82rem;
  outline: none;
}}
.sidebar-search {{ position: relative; }}
.sidebar-search input {{ padding-right: 28px; }}
.sidebar-search input::placeholder {{ color: #9ca3af; }}
.sidebar-search input:focus {{ border-color: var(--accent); }}
.btn-clear {{
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 2px 6px;
  font-size: 1.1rem;
  line-height: 1;
  display: none;
  border-radius: 4px;
}}
.btn-clear:hover {{ color: var(--white); background: rgba(255,255,255,.08); }}
.btn-clear.visible {{ display: block; }}
.sidebar-list {{
  flex: 1;
  overflow-y: auto;
  padding: 6px 0 16px;
  scrollbar-width: thin;
  scrollbar-color: #374151 transparent;
}}
.sidebar-list::-webkit-scrollbar {{ width: 4px; }}
.sidebar-list::-webkit-scrollbar-track {{ background: transparent; }}
.sidebar-list::-webkit-scrollbar-thumb {{ background: #374151; border-radius: 4px; }}
.cat-item {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 16px;
  cursor: pointer;
  font-size: .84rem;
  border-radius: 0;
  transition: background .15s;
  user-select: none;
}}
.cat-item:hover {{ background: rgba(255,255,255,.06); }}
.cat-item.active {{
  background: var(--accent);
  color: var(--white);
  font-weight: 600;
}}
.cat-item .badge {{
  font-size: .72rem;
  background: rgba(255,255,255,.15);
  color: inherit;
  padding: 1px 7px;
  border-radius: 99px;
  min-width: 26px;
  text-align: center;
}}
.cat-item.active .badge {{ background: rgba(255,255,255,.25); }}
.cat-item.parent {{ font-weight: 600; color: #fff; }}
.cat-item.parent .arrow {{
  display: inline-block;
  width: 10px;
  margin-right: 6px;
  padding: 4px;
  margin-left: -4px;
  transition: transform .15s;
  font-size: .65rem;
  opacity: .7;
  cursor: pointer;
}}
.cat-item.parent .arrow:hover {{ opacity: 1; }}
.cat-item.parent.expanded .arrow {{ transform: rotate(90deg); }}
.cat-item.child {{ padding-left: 32px; font-size: .8rem; }}

/* ===== MAIN ===== */
.main {{
  margin-left: var(--sidebar-w);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left .25s ease;
}}
.main.expanded {{ margin-left: 0; }}
.main.expanded .topbar {{ padding-left: 56px; }}

/* ===== TOPBAR ===== */
.topbar {{
  position: sticky;
  top: 0;
  z-index: 90;
  height: var(--topbar-h);
  background: var(--dark);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,.3);
}}
.topbar-search {{
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255,255,255,.09);
  border: 1px solid rgba(255,255,255,.15);
  border-radius: 8px;
  padding: 0 4px 0 12px;
  gap: 8px;
  flex: 1;
  max-width: 380px;
}}
.topbar-search svg {{ opacity: .5; flex-shrink: 0; }}
.topbar-search .btn-clear {{ position: static; transform: none; }}
.topbar-search input {{
  background: none;
  border: none;
  outline: none;
  color: var(--white);
  font-size: .9rem;
  width: 100%;
  padding: 8px 0;
}}
.topbar-search input::placeholder {{ color: #6b7280; }}
.breadcrumb {{
  color: #9ca3af;
  font-size: .83rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}}
.breadcrumb strong {{ color: var(--white); }}
.btn-reset {{
  background: none;
  border: 1px solid rgba(255,255,255,.2);
  color: #d1d5db;
  font-size: .8rem;
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: background .15s, color .15s;
  flex-shrink: 0;
}}
.btn-reset:hover {{ background: rgba(255,255,255,.1); color: var(--white); }}

/* ===== MOBILE PILLS ===== */
.pills-bar {{
  display: none;
  padding: 10px 12px;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  background: var(--white);
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}}
.pills-bar::-webkit-scrollbar {{ display: none; }}
.pill {{
  flex-shrink: 0;
  padding: 5px 14px;
  border-radius: 99px;
  border: 1.5px solid #d1d5db;
  background: var(--white);
  color: var(--dark);
  font-size: .8rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background .15s, border-color .15s, color .15s;
}}
.pill:hover {{ border-color: var(--accent); color: var(--accent); }}
.pill.active {{ background: var(--accent); border-color: var(--accent); color: var(--white); font-weight: 600; }}

/* ===== CONTENT ===== */
.content {{
  flex: 1;
  padding: 20px;
}}

/* ===== GRID ===== */
.grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}}
@media (min-width: 480px) {{
  .grid {{ grid-template-columns: repeat(3, 1fr); }}
}}
@media (min-width: 900px) {{
  .grid {{ grid-template-columns: repeat(4, 1fr); }}
}}

/* ===== CARD ===== */
.card {{
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  cursor: pointer;
  transition: transform .18s, box-shadow .18s;
  display: flex;
  flex-direction: column;
  content-visibility: auto;
  contain-intrinsic-size: 0 280px;
}}
.card:hover {{ transform: translateY(-3px); box-shadow: var(--shadow-hover); }}
/* ===== SKELETON ===== */
@keyframes shimmer {{
  0%   {{ background-position: 200% 0; }}
  100% {{ background-position: -200% 0; }}
}}
.sk {{
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: 4px;
}}
.card-sk {{
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.card-sk .sk-img {{ aspect-ratio: 1/1; border-radius: 0; }}
.card-sk .sk-line {{ height: 13px; margin: 10px 10px 6px; width: 65%; }}
.card-sk .sk-tag  {{ height: 18px; margin: 0 10px 12px; width: 38%; border-radius: 99px; }}
/* ===== CAROUSEL ===== */
.carousel {{
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background: var(--white);
  cursor: grab;
  user-select: none;
}}
.carousel:active {{ cursor: grabbing; }}
.carousel-track {{
  display: flex;
  height: 100%;
  transition: transform .28s cubic-bezier(.4,0,.2,1);
  will-change: transform;
}}
.carousel-track img {{
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 8px;
  pointer-events: none;
}}
.carousel-btn {{
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(17,24,39,.55);
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 26px;
  height: 26px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  opacity: 0;
  transition: opacity .18s;
  padding: 0;
  line-height: 1;
}}
.carousel:hover .carousel-btn {{ opacity: 1; }}
.carousel-btn.prev {{ left: 4px; }}
.carousel-btn.next {{ right: 4px; }}
.carousel-dots {{
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
  z-index: 2;
}}
.carousel-dot {{
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: rgba(255,255,255,.5);
  transition: background .2s, transform .2s;
}}
.carousel-dot.on {{
  background: var(--accent);
  transform: scale(1.3);
}}
.img-count {{
  position: absolute;
  top: 6px;
  right: 7px;
  background: rgba(17,24,39,.6);
  color: #fff;
  font-size: .65rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 99px;
  z-index: 2;
  letter-spacing: .02em;
}}
.card-body {{
  padding: 8px 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}}
.card-name {{
  font-size: .82rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--dark);
  word-break: break-word;
}}
.card-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}}
.tag {{
  font-size: .68rem;
  padding: 2px 7px;
  border-radius: 99px;
  background: #ede9fe;
  color: var(--accent);
  font-weight: 500;
}}

/* ===== LOADER ===== */
.spinner {{
  width: 40px; height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin .7s linear infinite;
}}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}

/* ===== EMPTY STATE ===== */
.empty {{
  text-align: center;
  padding: 80px 20px;
  color: #6b7280;
}}
.empty svg {{ opacity: .3; margin-bottom: 16px; }}
.empty p {{ font-size: 1rem; }}

/* ===== PAGINATION ===== */
.pagination {{
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px;
  padding: 28px 20px 36px;
}}
.page-btn {{
  min-width: 36px;
  height: 36px;
  border: 1.5px solid #d1d5db;
  background: var(--white);
  color: var(--dark);
  border-radius: 8px;
  cursor: pointer;
  font-size: .88rem;
  font-weight: 500;
  padding: 0 10px;
  transition: background .15s, border-color .15s, color .15s;
  display: flex; align-items: center; justify-content: center;
}}
.page-btn:hover:not(:disabled) {{ border-color: var(--accent); color: var(--accent); }}
.page-btn.active {{ background: var(--accent); border-color: var(--accent); color: var(--white); font-weight: 700; }}
.page-btn:disabled {{ opacity: .35; cursor: default; }}
.page-ellipsis {{
  color: #9ca3af;
  padding: 0 4px;
  display: flex; align-items: center;
}}

/* ===== MODAL ===== */
.modal-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.65);
  z-index: 200;
  align-items: center;
  justify-content: center;
  padding: 16px;
}}
.modal-overlay.open {{ display: flex; }}
.modal {{
  background: var(--white);
  border-radius: 14px;
  max-width: 480px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,.4);
  overflow: hidden;
  animation: slideUp .2s ease;
}}
@keyframes slideUp {{
  from {{ opacity: 0; transform: translateY(24px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.modal-carousel {{
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  max-height: 420px;
  overflow: hidden;
  background: var(--light);
  cursor: grab;
}}
.modal-carousel:active {{ cursor: grabbing; }}
.modal-carousel .carousel-track img {{
  padding: 16px;
  object-fit: contain;
}}
.modal-carousel .carousel-btn {{
  width: 36px;
  height: 36px;
  font-size: 18px;
  opacity: .7;
}}
.modal-carousel:hover .carousel-btn {{ opacity: 1; }}
.modal-carousel .img-count {{
  font-size: .75rem;
  padding: 3px 9px;
}}
.modal-body {{
  padding: 16px 20px 20px;
}}
.modal-name {{
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--dark);
}}
.modal-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}}
.modal-tag {{
  font-size: .78rem;
  padding: 4px 12px;
  border-radius: 99px;
  background: #ede9fe;
  color: var(--accent);
  font-weight: 500;
}}
.modal-info {{
  font-size: .85rem;
  color: #6b7280;
  font-style: italic;
  margin-bottom: 16px;
  padding: 8px 12px;
  background: #f9fafb;
  border-left: 3px solid var(--accent);
  border-radius: 4px;
}}
.btn-close {{
  width: 100%;
  padding: 10px;
  background: var(--accent);
  color: var(--white);
  border: none;
  border-radius: 8px;
  font-size: .9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity .15s;
}}
.btn-close:hover {{ opacity: .88; }}

/* ===== RESPONSIVE ===== */
.sidebar-backdrop {{
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,.5);
  z-index: 150;
}}
@media (max-width: 640px) {{
  .sidebar {{ display: flex; z-index: 200; }}
  .main {{ margin-left: 0; }}
  .pills-bar {{ display: none; }}
  .topbar {{ padding: 0 12px; gap: 8px; }}
  .content {{ padding: 12px; }}
  .btn-sidebar-toggle {{ display: flex; z-index: 201; }}
  .main.expanded .topbar {{ padding-left: 12px; }}
  .sidebar-backdrop.visible {{ display: block; }}
}}
</style>
</head>
<body>

<!-- SIDEBAR -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-logo">3D<span>Cubik</span></div>
  <div class="sidebar-search">
    <input type="text" id="sidebarCatSearch" placeholder="Cerca categoria..." autocomplete="off"/>
    <button type="button" class="btn-clear" id="btnClearCatSearch" aria-label="Cancella">×</button>
  </div>
  <div class="sidebar-list" id="sidebarList"></div>
</aside>
<button type="button" class="btn-sidebar-toggle" id="btnSidebarToggle" aria-label="Mostra/nascondi categorie">
  <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
</button>
<div class="sidebar-backdrop" id="sidebarBackdrop"></div>

<!-- MAIN -->
<div class="main">

  <!-- TOPBAR -->
  <div class="topbar">
    <div class="topbar-search">
      <svg width="16" height="16" fill="none" stroke="#fff" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" id="searchInput" placeholder="Cerca prodotto..." autocomplete="off"/>
      <button type="button" class="btn-clear" id="btnClearSearch" aria-label="Cancella ricerca">×</button>
    </div>
    <div class="breadcrumb" id="breadcrumb"><strong>Tutti</strong> i prodotti</div>
    <button class="btn-reset" id="btnReset">Reset filtri</button>
  </div>

  <!-- PILLS MOBILE -->
  <div class="pills-bar" id="pillsBar"></div>

  <!-- CONTENT -->
  <div class="content">
    <div id="loader" style="display:none"></div>
    <div class="grid" id="skeletonGrid"></div>
    <div class="grid" id="grid" style="display:none"></div>
    <div class="empty" id="empty" style="display:none">
      <svg width="64" height="64" fill="none" stroke="#9ca3af" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/></svg>
      <p>Nessun prodotto trovato</p>
    </div>
    <div class="pagination" id="pagination"></div>
  </div>
</div>

<!-- MODAL -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <div id="modalImgWrap"></div>
    <div class="modal-body">
      <div class="modal-name" id="modalName"></div>
      <div class="modal-tags" id="modalTags"></div>
      <div class="modal-info" id="modalInfo">Disponibile in diverse misure</div>
      <button class="btn-close" id="btnClose">Chiudi</button>
    </div>
  </div>
</div>

<script>
const ALL_CATEGORIES = {categories_json};
const PER_PAGE = {PER_PAGE};
let PRODUCTS = [];
let state = {{ category: "Tutti", search: "", page: 1 }};

function thumb(src) {{ return src.replace("imgs/webp/", "imgs/thumb/"); }}

function showSkeleton() {{
  const sk = document.getElementById("skeletonGrid");
  sk.innerHTML = Array.from({{length:12}}, () =>
    `<div class="card-sk"><div class="sk sk-img"></div><div class="sk sk-line"></div><div class="sk sk-tag"></div></div>`
  ).join("");
  sk.style.display = "";
}}
function hideSkeleton() {{
  const sk = document.getElementById("skeletonGrid");
  sk.style.display = "none"; sk.innerHTML = "";
}}

async function loadData() {{
  showSkeleton();
  try {{
    const r = await fetch("products.json");
    if (!r.ok) throw new Error("HTTP " + r.status);
    PRODUCTS = await r.json();
    PRODUCTS.forEach((p, i) => {{ p.num = String(i).padStart(4, "0"); }});
  }} catch(e) {{
    hideSkeleton();
    document.getElementById("loader").style.cssText = "display:flex;padding:40px 20px";
    document.getElementById("loader").innerHTML = `<p style="color:#ef4444">Errore: ${{e.message}}</p>`;
    return;
  }}
  hideSkeleton();
  render();
  preloadFirstPage();
}}

function preloadFirstPage() {{
  const page = PRODUCTS.slice(0, Math.min(12, PER_PAGE));
  const frag = document.createDocumentFragment();
  page.forEach(p => {{
    const link = document.createElement("link");
    link.rel = "preload"; link.as = "image";
    link.href = thumb(p.i[0]);
    frag.appendChild(link);
  }});
  document.head.appendChild(frag);
}}

function loadImg(img) {{
  if (img.dataset.src) {{ img.src = img.dataset.src; delete img.dataset.src; }}
}}

function filtered() {{
  return PRODUCTS.filter(p => {{
    const catOk = state.category === "Tutti" || p.c.includes(state.category);
    const q = state.search.trim().toLowerCase();
    return catOk && (!q || p.n.toLowerCase().includes(q));
  }});
}}

function catCount(cat) {{
  if (cat === "Tutti") return PRODUCTS.length;
  return PRODUCTS.filter(p => p.c.includes(cat)).length;
}}

const HIERARCHY = {{
  "Bambini": ["Barbie", "Bing", "Cocomelon", "Dinosauri", "Hello Kitty", "Masha e Orso", "Orsetti", "Peppa Pig", "PJmask", "Sonic", "Super Mario", "Supereroi", "Unicorni"],
  "Disney": ["Bella e Bestia", "Carica 101", "Frozen", "Inside Out", "Oceania", "Principesse", "Re Leone", "Stitch", "Topolino", "Winnie The Pooh", "Zootropolis"]
}};
const CHILD_TO_PARENT = {{}};
for (const [p, cs] of Object.entries(HIERARCHY)) for (const c of cs) CHILD_TO_PARENT[c] = p;
const expandedParents = new Set();

function renderSidebar() {{
  const q = document.getElementById("sidebarCatSearch").value.trim().toLowerCase();
  const list = document.getElementById("sidebarList");
  const matchQ = c => !q || c.toLowerCase().includes(q);
  const items = [];

  if (matchQ("Tutti")) {{
    const a = state.category === "Tutti" ? " active" : "";
    items.push(`<div class="cat-item${{a}}" data-cat="Tutti"><span>Tutti</span><span class="badge">${{PRODUCTS.length}}</span></div>`);
  }}

  for (const cat of ALL_CATEGORIES) {{
    if (CHILD_TO_PARENT[cat]) continue;
    if (HIERARCHY[cat]) {{
      const children = HIERARCHY[cat].filter(c => ALL_CATEGORIES.includes(c) && catCount(c) > 0);
      const parentMatchesQ = matchQ(cat);
      const childrenMatchingQ = children.filter(matchQ);
      const showParent = q ? (parentMatchesQ || childrenMatchingQ.length > 0) : children.length > 0;
      if (!showParent) continue;
      const expanded = q ? true : expandedParents.has(cat);
      const a = state.category === cat ? " active" : "";
      items.push(`<div class="cat-item parent${{expanded ? ' expanded' : ''}}${{a}}" data-cat="${{escHtml(cat)}}" data-parent="${{escHtml(cat)}}"><span><span class="arrow" data-toggle="1">▶</span>${{escHtml(cat)}}</span><span class="badge">${{catCount(cat)}}</span></div>`);
      if (expanded) {{
        const visible = q && !parentMatchesQ ? childrenMatchingQ : children;
        for (const child of visible) {{
          const a = state.category === child ? " active" : "";
          items.push(`<div class="cat-item child${{a}}" data-cat="${{escHtml(child)}}"><span>${{escHtml(child)}}</span><span class="badge">${{catCount(child)}}</span></div>`);
        }}
      }}
    }} else {{
      if (!matchQ(cat) || catCount(cat) === 0) continue;
      const a = state.category === cat ? " active" : "";
      items.push(`<div class="cat-item${{a}}" data-cat="${{escHtml(cat)}}"><span>${{escHtml(cat)}}</span><span class="badge">${{catCount(cat)}}</span></div>`);
    }}
  }}

  list.innerHTML = items.join("");
  list.querySelectorAll(".cat-item .arrow[data-toggle]").forEach(el =>
    el.addEventListener("click", e => {{
      e.stopPropagation();
      const p = el.closest(".cat-item.parent").dataset.parent;
      if (expandedParents.has(p)) expandedParents.delete(p); else expandedParents.add(p);
      renderSidebar();
    }})
  );
  list.querySelectorAll(".cat-item").forEach(el =>
    el.addEventListener("click", () => {{
      const p = el.dataset.parent;
      if (p) {{
        if (expandedParents.has(p)) expandedParents.delete(p);
        else expandedParents.add(p);
      }}
      selectCategory(el.dataset.cat);
    }})
  );
}}

function renderPills() {{
  const bar = document.getElementById("pillsBar");
  const cats = ["Tutti", ...ALL_CATEGORIES].filter(c => c === "Tutti" || catCount(c) > 0);
  bar.innerHTML = cats.map(cat => {{
    const active = state.category === cat ? " active" : "";
    return `<div class="pill${{active}}" data-cat="${{escHtml(cat)}}">${{escHtml(cat)}}</div>`;
  }}).join("");
  bar.querySelectorAll(".pill").forEach(el =>
    el.addEventListener("click", () => selectCategory(el.dataset.cat))
  );
}}

function selectCategory(cat) {{
  state.category = cat; state.page = 1; render();
  if (window.innerWidth <= 640 && !document.getElementById("sidebar").classList.contains("collapsed")) {{
    _toggleSidebar();
  }}
}}

function renderBreadcrumb() {{
  const f = filtered();
  const bc = document.getElementById("breadcrumb");
  if (state.category === "Tutti" && !state.search) {{
    bc.innerHTML = `<strong>Tutti</strong> i prodotti (${{f.length}})`;
  }} else {{
    bc.innerHTML = `<strong>${{escHtml(state.category)}}</strong>` +
      (state.search ? ` &rarr; "<em>${{escHtml(state.search)}}</em>"` : "") +
      ` — ${{f.length}} prodott${{f.length === 1 ? "o" : "i"}}`;
  }}
}}

function renderGrid() {{
  const items = filtered();
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / PER_PAGE));
  if (state.page > totalPages) state.page = totalPages;
  const start = (state.page - 1) * PER_PAGE;
  const page = items.slice(start, start + PER_PAGE);
  const grid = document.getElementById("grid");
  const empty = document.getElementById("empty");

  if (page.length === 0) {{
    grid.innerHTML = ""; grid.style.display = "none"; empty.style.display = "";
  }} else {{
    empty.style.display = "none";
    grid.innerHTML = page.map((p, i) => {{
      const tags = p.c.map(c => `<span class="tag">${{escHtml(c)}}</span>`).join("");
      const thumbs = p.i.map(src => thumb(src));
      const multi = thumbs.length > 1;
      const slides = thumbs.map((t, ii) =>
        ii === 0
          ? `<img src="${{escHtml(t)}}" alt="${{escHtml(p.n)}}" loading="eager" decoding="async">`
          : `<img data-src="${{escHtml(t)}}" alt="${{escHtml(p.n)}}" decoding="async">`
      ).join("");
      const dots = multi ? thumbs.map((_,di) =>
        `<span class="carousel-dot${{di===0?" on":""}}"></span>`).join("") : "";
      return `<div class="card" data-idx="${{start+i}}">
        <div class="carousel" data-ci="0">
          ${{multi?`<span class="img-count">1/${{thumbs.length}}</span>`:""}}
          <div class="carousel-track">${{slides}}</div>
          ${{multi?`<button class="carousel-btn prev">&#8249;</button><button class="carousel-btn next">&#8250;</button><div class="carousel-dots">${{dots}}</div>`:""}}
        </div>
        <div class="card-body">
          <div class="card-name">${{p.num}}. ${{escHtml(p.n.replace(/_/g," "))}}</div>
          <div class="card-tags">${{tags}}</div>
        </div>
      </div>`;
    }}).join("");
    grid.style.display = "";

    grid.querySelectorAll(".carousel").forEach(car => {{
      const track = car.querySelector(".carousel-track");
      const dots = car.querySelectorAll(".carousel-dot");
      const count = car.querySelector(".img-count");
      const imgEls = car.querySelectorAll("img");
      const n = imgEls.length;
      if (n <= 1) return;
      function moveTo(idx) {{
        idx = (idx + n) % n;
        car.dataset.ci = idx;
        track.style.transform = `translateX(-${{idx*100}}%)`;
        dots.forEach((d,di) => d.classList.toggle("on", di===idx));
        if (count) count.textContent = `${{idx+1}}/${{n}}`;
        [idx, (idx+1)%n].forEach(j => loadImg(imgEls[j]));
      }}
      car.querySelector(".prev").addEventListener("click", e => {{ e.stopPropagation(); moveTo(+car.dataset.ci-1); }});
      car.querySelector(".next").addEventListener("click", e => {{ e.stopPropagation(); moveTo(+car.dataset.ci+1); }});
      let tx = 0;
      car.addEventListener("touchstart", e => {{ tx = e.touches[0].clientX; }}, {{passive:true}});
      car.addEventListener("touchend", e => {{
        const dx = e.changedTouches[0].clientX - tx;
        if (Math.abs(dx) > 40) moveTo(+car.dataset.ci + (dx<0?1:-1));
      }}, {{passive:true}});
    }});
    grid.querySelectorAll(".card").forEach(el =>
      el.addEventListener("click", () => openModal(filtered()[parseInt(el.dataset.idx)]))
    );
  }}
  renderPagination(total);
}}

function renderPagination(total) {{
  const totalPages = Math.max(1, Math.ceil(total / PER_PAGE));
  const pag = document.getElementById("pagination");
  if (totalPages <= 1) {{ pag.innerHTML = ""; return; }}
  const cur = state.page;
  const pages = [1];
  if (cur - 2 > 2) pages.push("...");
  for (let p = Math.max(2, cur-1); p <= Math.min(totalPages-1, cur+1); p++) pages.push(p);
  if (cur + 2 < totalPages - 1) pages.push("...");
  if (totalPages > 1) pages.push(totalPages);
  pag.innerHTML =
    `<button class="page-btn" id="prevBtn" ${{cur===1?"disabled":""}}>&#8592; Prev</button>` +
    pages.map(p => p==="..."
      ? `<span class="page-ellipsis">…</span>`
      : `<button class="page-btn${{p===cur?" active":""}}" data-page="${{p}}">${{p}}</button>`
    ).join("") +
    `<button class="page-btn" id="nextBtn" ${{cur===totalPages?"disabled":""}}>Next &#8594;</button>`;
  pag.querySelector("#prevBtn")?.addEventListener("click", () => goPage(cur-1));
  pag.querySelector("#nextBtn")?.addEventListener("click", () => goPage(cur+1));
  pag.querySelectorAll(".page-btn[data-page]").forEach(btn =>
    btn.addEventListener("click", () => goPage(parseInt(btn.dataset.page)))
  );
}}

function goPage(p) {{
  state.page = p; render(); window.scrollTo({{top:0, behavior:"smooth"}});
}}

let modalIdx = 0, modalImgs = [];

function openModal(p) {{
  modalImgs = p.i; modalIdx = 0;
  renderModalCarousel();
  document.getElementById("modalName").textContent = p.num + ". " + p.n.replace(/_/g," ");
  document.getElementById("modalInfo").textContent = p.d && p.d.trim() ? p.d : "Disponibile in diverse misure";
  document.getElementById("modalTags").innerHTML = p.c.map(c =>
    `<span class="modal-tag">${{escHtml(c)}}</span>`).join("");
  document.getElementById("modalOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}}

function renderModalCarousel() {{
  const wrap = document.getElementById("modalImgWrap");
  const multi = modalImgs.length > 1;
  wrap.innerHTML =
    `<div class="modal-carousel" id="mc"><div class="carousel-track" id="mct">` +
    modalImgs.map((src,i) =>
      i===0 ? `<img src="${{escHtml(src)}}" alt="" decoding="async">`
             : `<img data-src="${{escHtml(src)}}" alt="" decoding="async">`
    ).join("") +
    `</div>` +
    (multi ? `<button class="carousel-btn prev" id="mPrev">&#8249;</button>
      <button class="carousel-btn next" id="mNext">&#8250;</button>
      <div class="carousel-dots" id="mDots">${{modalImgs.map((_,i)=>`<span class="carousel-dot${{i===0?" on":""}}"></span>`).join("")}}</div>
      <span class="img-count" id="mCount">1/${{modalImgs.length}}</span>` : "") +
    `</div>`;
  if (multi) {{
    const track = document.getElementById("mct");
    const dots = document.getElementById("mDots").querySelectorAll(".carousel-dot");
    const countEl = document.getElementById("mCount");
    const imgEls = track.querySelectorAll("img");
    function mMoveTo(idx) {{
      modalIdx = (idx + modalImgs.length) % modalImgs.length;
      track.style.transform = `translateX(-${{modalIdx*100}}%)`;
      dots.forEach((d,di) => d.classList.toggle("on", di===modalIdx));
      countEl.textContent = `${{modalIdx+1}}/${{modalImgs.length}}`;
      [modalIdx, (modalIdx+1)%modalImgs.length].forEach(i => loadImg(imgEls[i]));
    }}
    document.getElementById("mPrev").onclick = () => mMoveTo(modalIdx-1);
    document.getElementById("mNext").onclick = () => mMoveTo(modalIdx+1);
    const mc = document.getElementById("mc");
    mc._keyFn = e => {{
      if (e.key==="ArrowLeft") mMoveTo(modalIdx-1);
      if (e.key==="ArrowRight") mMoveTo(modalIdx+1);
    }};
    let mtx=0;
    mc.addEventListener("touchstart", e => {{ mtx=e.touches[0].clientX; }}, {{passive:true}});
    mc.addEventListener("touchend", e => {{
      const dx = e.changedTouches[0].clientX - mtx;
      if (Math.abs(dx)>40) mMoveTo(modalIdx+(dx<0?1:-1));
    }}, {{passive:true}});
  }}
}}

function closeModal() {{
  document.getElementById("modalOverlay").classList.remove("open");
  document.getElementById("modalImgWrap").innerHTML = "";
  document.body.style.overflow = "";
  modalImgs=[]; modalIdx=0;
}}

function render() {{ renderSidebar(); renderPills(); renderBreadcrumb(); renderGrid(); }}

function escHtml(s) {{
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}}

let _st;
function setupClear(inputId, btnId, onClear) {{
  const input = document.getElementById(inputId);
  const btn = document.getElementById(btnId);
  const sync = () => btn.classList.toggle("visible", input.value !== "");
  input.addEventListener("input", sync);
  btn.addEventListener("click", () => {{ input.value=""; sync(); onClear(); input.focus(); }});
  sync();
}}
document.getElementById("searchInput").addEventListener("input", e => {{
  clearTimeout(_st);
  _st = setTimeout(() => {{
    const v = e.target.value;
    if (v && state.category !== "Tutti") state.category = "Tutti";
    state.search = v; state.page = 1; render();
  }}, 300);
}});
document.getElementById("sidebarCatSearch").addEventListener("input", renderSidebar);
setupClear("searchInput", "btnClearSearch", () => {{ state.search=""; state.page=1; render(); }});
setupClear("sidebarCatSearch", "btnClearCatSearch", renderSidebar);
const _isMobile = () => window.innerWidth <= 640;
const _sidebar = document.getElementById("sidebar");
const _sbBtn = document.getElementById("btnSidebarToggle");
const _sbBack = document.getElementById("sidebarBackdrop");
if (_isMobile()) {{
  _sidebar.classList.add("collapsed");
  _sbBtn.classList.add("collapsed");
}}
function _toggleSidebar() {{
  _sidebar.classList.toggle("collapsed");
  document.querySelector(".main").classList.toggle("expanded");
  _sbBtn.classList.toggle("collapsed");
  if (_isMobile()) _sbBack.classList.toggle("visible", !_sidebar.classList.contains("collapsed"));
}}
_sbBtn.addEventListener("click", _toggleSidebar);
_sbBack.addEventListener("click", _toggleSidebar);
document.getElementById("btnReset").addEventListener("click", () => {{
  state={{category:"Tutti",search:"",page:1}};
  document.getElementById("searchInput").value="";
  document.getElementById("sidebarCatSearch").value="";
  document.getElementById("btnClearSearch").classList.remove("visible");
  document.getElementById("btnClearCatSearch").classList.remove("visible");
  render();
}});
document.getElementById("btnClose").addEventListener("click", closeModal);
document.getElementById("modalOverlay").addEventListener("click", e => {{
  if (e.target===e.currentTarget) closeModal();
}});
document.addEventListener("keydown", e => {{
  if (e.key==="Escape") closeModal();
  const mc=document.getElementById("mc");
  if (mc&&mc._keyFn) mc._keyFn(e);
}});

loadData();
if ("serviceWorker" in navigator)
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(()=>{{}}));
</script>
</body>
</html>"""
    return html


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    reset_mode = "--reset" in sys.argv

    if reset_mode:
        print("⚠️  Modalità RESET: tutte le modifiche dell'admin verranno perse.")
        existing = None
    else:
        existing = load_existing_products()
        if existing:
            print(f"Merge con {len(existing)} prodotti esistenti (modifiche admin preservate).")
        else:
            print("Nessun products.json trovato — costruzione da zero.")

    print("Scansione imgs/webp/ ...")
    products = build_products(existing=existing)
    print(f"Prodotti totali: {len(products)}")

    # 1. Watermark (solo per immagini non ancora processate)
    apply_watermarks()

    # 2. Thumbnail (solo per immagini nuove)
    generate_thumbnails()

    # 2. products.json
    OUTPUT_JSON.write_text(
        json.dumps(products, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8"
    )
    print(f"Generato: {OUTPUT_JSON} ({OUTPUT_JSON.stat().st_size / 1024:.1f} KB)")

    # 3. index.html
    html = generate_html()
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"Generato: {OUTPUT_HTML} ({OUTPUT_HTML.stat().st_size / 1024:.1f} KB)")

    print()
    print_stats(products)
