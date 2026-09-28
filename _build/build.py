#!/usr/bin/env python3
"""Builds the portfolio: index.html (EN), fr/index.html (FR), 404, sitemap, robots, llms.txt, manifest.

Run from the repository root:  python3 _build/build.py
Jekyll (GitHub Pages) ignores this folder because its name starts with an underscore.
"""
import json, datetime, re, pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = pathlib.Path(__file__).resolve().parent
SITE = "https://ilyomix.github.io"
EMAIL = "ilyes1204@gmail.com"
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year
YEARS = YEAR - 2017 - (1 if datetime.date.today() < datetime.date(YEAR, 9, 1) else 0)

ICONS = {
    "out": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
}

def icon(name):
    return Markup(f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

def img(name, widths, w, h, sizes, alt):
    return {
        "src": f"/assets/img/{name}-{widths[-1]}.webp",
        "srcset": ", ".join(f"/assets/img/{name}-{x}.webp {x}w" for x in widths),
        "sizes": sizes, "w": w, "h": h, "alt": alt,
    }

Y = Markup(f'<span data-years>{YEARS}</span>')

def content(lang):
    en = lang == "en"
    L = lambda f, e: e if en else f
    shots = "en" if en else "fr"
    cadran_desktop = lambda alt, sizes: img("mac-cadran-desktop", [640, 960, 1600, 2400], 2400, 1449, sizes, alt)
    return {
        "lang": lang,
        "url": f"{SITE}/" if en else f"{SITE}/fr/",
        "home": "/" if en else "/fr/",
        "og_locale": "en_US" if en else "fr_FR",
        "og_locale_alt": "fr_FR" if en else "en_US",
        "alt": {"href": "/fr/", "lang": "fr", "short": "FR", "long": "Français", "label": "Version française"} if en
               else {"href": "/", "lang": "en", "short": "EN", "long": "English", "label": "English version"},
        "meta": {
            "title": L("Ilyes Abd-Lillah · Software & Design Engineer à Toulouse",
                       "Ilyes Abd-Lillah · Software & Design Engineer in Toulouse"),
            "description": L(f"Software & design engineer à Toulouse. {YEARS}+ ans à concevoir et construire des interfaces produit rapides et accessibles en React et TypeScript, des design systems et des apps macOS en SwiftUI.",
                             f"Software & design engineer in Toulouse. {YEARS}+ years designing and building fast, accessible product interfaces in React and TypeScript, design systems and native macOS apps in SwiftUI."),
            "og_title": "Ilyes Abd-Lillah, software & design engineer",
            "og_description": L("Interfaces produit, design systems et apps macOS natives. Cadran, Lift, Crypto LED Board. Toulouse, France.",
                                "Product interfaces, design systems and native macOS apps. Cadran, Lift, Crypto LED Board. Toulouse, France."),
            "og_alt": L("Ilyes Abd-Lillah, software & design engineer à Toulouse, avec Cadran sur un MacBook Pro, Lift sur téléphone et Crypto LED Board sur un Studio Display.",
                        "Ilyes Abd-Lillah, software & design engineer in Toulouse, with Cadran on a MacBook Pro, Lift on a phone and Crypto LED Board on a Studio Display."),
        },
        "ui": {
            "skip": L("Aller au contenu", "Skip to content"),
            "home_label": L("Ilyes Abd-Lillah, accueil", "Ilyes Abd-Lillah, home"),
            "nav_label": L("Sections", "Sections"),
            "to_light": L("Passer en mode clair", "Switch to light mode"),
            "lang_label": L("Langue", "Language"),
            "to_dark": L("Passer en mode sombre", "Switch to dark mode"),
        },
        "nav": [
            {"id": "work", "label": L("Projets", "Work")},
            {"id": "about", "label": L("À propos", "About")},
            {"id": "experience", "label": L("Parcours", "Experience")},
            {"id": "contact", "label": "Contact"},
        ],
        "hero": {
            "role": "software & design engineer.",
            "lede": L("Je transforme des idées produit complexes en interfaces rapides et accessibles, je construis les design systems qui aident les équipes à les livrer, et je fais des apps macOS natives en SwiftUI.",
                      "I turn complex product ideas into fast, accessible interfaces, build the design systems that help teams ship them, and make native macOS apps in SwiftUI."),
            "facts": Markup(L(f"{Y}+ ans · Lead Frontend chez FoodPilot · Toulouse, France",
                              f"{Y}+ years · Lead Frontend at FoodPilot · Toulouse, France")),
            "cta_mail": L("M’écrire", "Email me"),
            "cta_work": L("Voir les projets", "See the work"),
        },
        "sheet_label": L("Aperçu des projets", "Work at a glance"),
        "fig_word": "Fig.",
        "figures": [
            {**cadran_desktop(L("Le bureau d’un Mac avec Cadran : une horloge à palettes sur le fond d’écran, derrière les icônes.",
                                "A Mac desktop running Cadran: a flip clock on the wallpaper, behind the icons."),
                              "(min-width: 860px) 36vw, 82vw"),
             "caption": L("Cadran sur macOS", "Cadran on macOS"), "target": "cadran", "phone": False},
            {**img(f"lift-home-{shots}", [390, 780], 780, 1688, "(min-width: 860px) 14vw, 46vw",
                   L("L’écran Aujourd’hui de Lift : progression vers la date objectif et prochaine séance.",
                     "Lift’s Today screen: progress towards the goal date and the next session.")),
             "caption": L("Lift, aujourd’hui", "Lift, today"), "target": "lift", "phone": True},
            {**img(f"lift-session-{shots}", [390, 780], 780, 1688, "(min-width: 860px) 14vw, 46vw",
                   L("Une séance guidée dans Lift : séries, charges, RIR et minuteur.",
                     "A guided session in Lift: sets, loads, RIR and the timer.")),
             "caption": L("Lift, en séance", "Lift, in a session"), "target": "lift", "phone": True},
            {**img("mac-led-board", [640, 960, 1600, 2400], 2400, 1844, "(min-width: 860px) 36vw, 82vw",
                   L("Crypto LED Board : prix, graphique, carnet d’ordres et profondeur du Bitcoin en matrice LED.",
                     "Crypto LED Board: Bitcoin price, chart, order book and depth as an LED matrix.")),
             "caption": "Crypto LED Board", "target": "led-board", "phone": False},
        ],
        "work": {
            "title": L("Projets.", "Selected work."),
            "lede": L("Trois produits que j’ai conçus, développés et publiés moi-même, d’une app Mac native à une web app installable.",
                      "Three products I designed, engineered and shipped myself, from a native Mac app to an installable web app."),
        },
        "projects": [
            {
                "id": "cadran", "name": "Cadran", "icon": "/assets/img/cadran-icon-112.webp",
                "tagline": L("Une horloge de bureau pour macOS, dessinée sur le fond d’écran.",
                             "A desktop clock for macOS, drawn on the wallpaper."),
                "body": [
                    L("Cadran affiche des cadrans vivants sur la couche du fond d’écran, derrière les icônes, sur chaque Space et chaque écran. Une app SwiftUI native, un rendu Core Animation pensé pour consommer peu d’énergie, un mode économiseur d’écran et un site produit en Next.js.",
                      "Cadran renders live clock faces on the wallpaper layer, behind the icons, on every Space and display. A native SwiftUI app, Core Animation rendering tuned for low energy use, a screen saver mode and a Next.js product site."),
                ],
                "specs": [
                    (L("Rôle", "Role"), L("Fondateur · design et développement", "Founder · design and engineering")),
                    (L("Plateforme", "Platform"), L("macOS 14 ou plus · Apple silicon et Intel", "macOS 14 or later · Apple silicon and Intel")),
                    (L("Technologies", "Built with"), "Swift · SwiftUI · Core Animation · Next.js"),
                    (L("Modèle", "Model"), L("Gratuit, avec un Pro en achat unique", "Free, with a one-time Pro upgrade")),
                ],
                "facts": L("Mis en avant sur Product Hunt · Cité dans Awesome Mac · Disponible sur Homebrew",
                           "Featured on Product Hunt · Listed in Awesome Mac · Available on Homebrew"),
                "links": [
                    {"label": "cadranapp.com", "href": "https://www.cadranapp.com"},
                    {"label": "Product Hunt", "href": "https://www.producthunt.com/products/cadran"},
                    {"label": "Awesome Mac", "href": "https://github.com/jaywcjlove/awesome-mac#general-tools"},
                ],
                "media": {"kind": "cadran", "shots": [
                    cadran_desktop(L("Cadran sur un MacBook Pro : une horloge à palettes sur le fond d’écran, avec le morceau en cours de lecture.",
                                     "Cadran on a MacBook Pro: a flip clock on the wallpaper, with the track now playing."),
                                   "(min-width: 1260px) 1180px, 92vw"),
                    img("mac-cadran-weather", [640, 1000, 1400], 1400, 848, "(min-width: 640px) 46vw, 92vw",
                        L("Cadran sur un MacBook Air : un cadran avec la météo en direct au-dessus d’un paysage de lac.", "Cadran on a MacBook Air: a clock face with live weather over a lake wallpaper.")),
                    img("mac-cadran-settings", [640, 1000, 1400], 1400, 848, "(min-width: 640px) 46vw, 92vw",
                        L("Cadran sur un MacBook Air : les réglages et le mode économiseur d’écran.", "Cadran on a MacBook Air: the settings and screen saver mode.")),
                ], "caption": L("Captures de l’app sur macOS : le bureau, la météo en direct et l’économiseur d’écran.",
                                "Screens from the app on macOS: the desktop, live weather and the screen saver.")},
            },
            {
                "id": "lift", "name": "Lift", "icon": "/assets/lift-icon.svg",
                "tagline": L("Un programme de musculation fondé sur la recherche, à installer sur son téléphone.",
                             "A research-based training program you install on your phone."),
                "body": [
                    L("Lift construit tout le plan à rebours depuis une date objectif : recomposition, sèche si besoin, puis stabilisation, en blocs séparés par des semaines de décharge. Il guide ensuite chaque séance série par série, chronomètre les repos et ajuste les charges d’après ce qu’on soulève vraiment.",
                      "Lift builds the whole plan backwards from a goal date: recomposition, a cut if needed, then stabilization, in blocks separated by deloads. It then guides each session set by set, times the rests and adjusts loads from what you actually lift."),
                    L("Chaque règle est rattachée à son niveau de preuve, sur 31 publications vérifiées. Il fonctionne hors ligne, en français et en anglais, sans compte : tout reste sur le téléphone.",
                      "Every rule is tagged with its level of evidence, from 31 checked publications. It works offline, in French and English, with no account: everything stays on the phone."),
                ],
                "specs": [
                    (L("Rôle", "Role"), L("Design et développement", "Design and engineering")),
                    (L("Plateforme", "Platform"), L("iPhone, en web app installable (PWA)", "iPhone, as an installable web app (PWA)")),
                    (L("Technologies", "Built with"), "React 19 · TypeScript · Vite · Tailwind CSS · Workbox"),
                    ("Code", L("Open source sur GitHub", "Open source on GitHub")),
                ],
                "facts": None,
                "links": [
                    {"label": L("Ouvrir Lift", "Open Lift"), "href": "https://ilyomix.github.io/lift/"},
                    {"label": L("Code source", "Source code"), "href": "https://github.com/Ilyomix/lift"},
                ],
                "media": {"kind": "lift", "shots": [
                    img(f"lift-home-{shots}", [390, 780], 780, 1688, "(min-width: 960px) 300px, 28vw",
                        L("L’écran Aujourd’hui : séances restantes, phases du plan et prochaine séance.", "Today: sessions to go, the plan’s phases and the next session.")),
                    img(f"lift-session-{shots}", [390, 780], 780, 1688, "(min-width: 960px) 300px, 28vw",
                        L("Une séance : prescription de l’exercice, séries à remplir et minuteur.", "A session: the exercise prescription, sets to log and the timer.")),
                    img(f"lift-calendar-{shots}", [390, 780], 780, 1688, "(min-width: 960px) 300px, 28vw",
                        L("Le calendrier : blocs, rotation des séances et phases jusqu’à la date objectif.", "The calendar: blocks, the session rotation and phases up to the goal date.")),
                ], "caption": L("Aujourd’hui, une séance guidée et le calendrier, dans la version française.",
                                "Today, a guided session and the calendar, in the English version.")},
            },
            {
                "id": "led-board", "name": "Crypto LED Board", "icon": "/assets/crypto-led-board-icon.svg?v=dark-orange",
                "tagline": L("Un dashboard crypto en direct sur une matrice LED en pixel art.",
                             "A live crypto dashboard on a pixel-art LED matrix."),
                "body": [
                    L("On choisit une plateforme et une paire, puis on suit le prix, les graphiques, le carnet d’ordres et la profondeur de marché en temps réel. Tout est dessiné en matrice LED responsive, avec une typographie bitmap sur mesure et des effets CRT, alimentée par WebSocket.",
                      "Pick an exchange and a pair, then follow price, charts, order book and market depth in real time. Everything is drawn as a responsive LED matrix with custom bitmap typography and CRT effects, fed over WebSockets."),
                ],
                "specs": [
                    (L("Rôle", "Role"), L("Design et développement", "Design and engineering")),
                    (L("Plateforme", "Platform"), L("Web · ordinateur et mobile", "Web · desktop and mobile")),
                    (L("Technologies", "Built with"), "React · TypeScript · Vite · WebSockets · Canvas 2D / WebGL"),
                    (L("Données", "Data"), L("Flux de marché en direct", "Live market feeds")),
                ],
                "facts": None,
                "links": [{"label": L("Ouvrir Crypto LED Board", "Open Crypto LED Board"), "href": "https://crypto-led-board.vercel.app/"}],
                "media": {"kind": "led", "shots": [
                    img("mac-led-board", [640, 960, 1600, 2400], 2400, 1844, "(min-width: 1200px) 1120px, 92vw",
                        L("Crypto LED Board sur un Studio Display : Bitcoin contre USDT, prix, graphique sur un jour, carnet d’ordres et profondeur.", "Crypto LED Board on a Studio Display: Bitcoin against USDT, price, one-day chart, order book and depth.")),
                ], "caption": L("Bitcoin contre USDT : prix, graphique sur un jour, carnet d’ordres et profondeur.",
                                "Bitcoin against USDT: price, one-day chart, order book and depth.")},
            },
        ],
        "about": {
            "title": L("À propos.", "About."),
            "portrait_alt": L("Ilyes Abd-Lillah sur un toit à Toulouse.", "Ilyes Abd-Lillah on a rooftop in Toulouse."),
            "body": [
                Markup(L(f"Je travaille là où le design et le développement se rejoignent. Depuis plus de {Y} ans, j’aide des équipes à livrer des interfaces produit, à mettre en place des design systems et à transformer les détails d’interaction en logiciels qui semblent pensés.",
                         f"I work where design and engineering meet. For more than {Y} years I’ve helped teams ship product interfaces, set up design systems and turn interaction details into software that feels intentional.")),
                L("Aujourd’hui, je dirige le frontend de FoodPilot chez Positive Solutions et je construis mes propres produits à côté. Je suis aussi à l’aise pour affiner l’API d’un composant que la courbe d’une transition.",
                  "Today I lead frontend engineering on FoodPilot at Positive Solutions and build my own products on the side. I’m as comfortable refining a component API as a transition curve."),
            ],
            "cares_title": L("Ce qui compte pour moi", "What I care about"),
            "cares": [
                L("Des interfaces produit à la hiérarchie claire, avec un mouvement qui a un sens", "Product interfaces with clear hierarchy and purposeful motion"),
                L("Des design systems qui font gagner du temps sans rien lâcher sur la qualité", "Design systems that help teams move faster without losing quality"),
                L("L’accessibilité, la performance et une architecture frontend solide", "Accessibility, performance and resilient frontend architecture"),
                L("Des expériences macOS natives en Swift et SwiftUI", "Native macOS experiences built with Swift and SwiftUI"),
            ],
            "toolbox": [
                {"title": L("Interfaces produit", "Product UI"), "list": ["React", "Next.js", "Vue.js", "TypeScript", "Tailwind CSS"]},
                {"title": L("Natif et design", "Native and design"), "list": ["Swift", "SwiftUI", "Core Animation", "Figma"]},
                {"title": L("Outils", "Tools"), "list": ["Node.js", "Vite", "Git", "Docker"]},
            ],
        },
        "xp": {
            "title": L("Parcours.", "Experience."),
            "lede": L("Des postes de lead frontend en entreprise produit, et mes propres apps.",
                      "Frontend lead roles in product companies, and my own apps."),
            "rows": [
                {"when": "2026", "role": L("Fondateur", "Founder"), "org": "Cadran", "href": "https://www.cadranapp.com"},
                {"when": L("2023 → aujourd’hui", "2023 → today"), "role": "Lead Frontend Engineer", "org": "FoodPilot · Positive Solutions", "href": "https://foodpilot.io"},
                {"when": "2021 → 2023", "role": "Technical Lead Frontend", "org": "Skilleos", "href": "https://www.skilleos.com"},
                {"when": "2020 → 2021", "role": "Technical Lead Frontend", "org": "Guidap", "href": "https://guidap.com"},
                {"when": "2019 → 2020", "role": L("Développeur frontend", "Frontend Developer"), "org": "Continental", "href": "https://www.continental.com"},
                {"when": "2019 → 2020", "role": L("Consultant frontend", "Frontend Consultant"), "org": "WE+", "href": None},
                {"when": "2016 → 2019", "role": L("Développeur frontend", "Frontend Developer"), "org": "Maestro Corporation", "href": None},
                {"when": "2012 → 2017", "role": "Expert en Technologies de l’Information", "org": "EPITECH", "href": "https://www.epitech.eu"},
            ],
        },
        "contact": {
            "title": L("Construisons-le bien.", "Let’s build it well."),
            "lede": L("Un projet en tête, ou simplement envie de dire bonjour ? Écrivez-moi.",
                      "Got a project in mind, or just want to say hello? Write to me."),
            "time_before": L("Il est ", "It’s "),
            "time_after": L(" à Toulouse.", " in Toulouse."),
        },
        "footer": {
            "line": L("Conçu et développé à Toulouse.", "Designed and built in Toulouse."),
            "nav_label": L("Liens", "Links"),
        },
    }


def jsonld(c):
    lang = c["lang"]
    en = lang == "en"
    person = {
        "@type": "Person", "@id": f"{SITE}/#person",
        "name": "Ilyes Abd-Lillah", "givenName": "Ilyes", "familyName": "Abd-Lillah",
        "alternateName": ["Ilyomix"],
        "jobTitle": "Software & Design Engineer",
        "description": c["meta"]["description"],
        "url": f"{SITE}/", "email": EMAIL,
        "image": {"@type": "ImageObject", "url": f"{SITE}/assets/img/ilyes-460.webp", "width": 460, "height": 460},
        "address": {"@type": "PostalAddress", "addressLocality": "Toulouse", "addressRegion": "Occitanie", "addressCountry": "FR"},
        "homeLocation": {"@type": "Place", "name": "Toulouse, France"},
        "worksFor": {"@type": "Organization", "name": "Positive Solutions", "url": "https://positive-solutions.io"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "EPITECH", "url": "https://www.epitech.eu"},
        "knowsLanguage": ["fr", "en"],
        "knowsAbout": ["Software engineering", "Design engineering", "Frontend engineering", "Design systems", "User interface design", "Web accessibility",
                       "Web performance", "React", "Next.js", "Vue.js", "TypeScript", "Tailwind CSS", "Swift", "SwiftUI",
                       "Core Animation", "macOS app development", "Progressive web apps"],
        "hasOccupation": {"@type": "Occupation", "name": "Software & Design Engineer",
                          "occupationLocation": {"@type": "City", "name": "Toulouse"},
                          "skills": "React, TypeScript, Next.js, Vue.js, SwiftUI, design systems, accessibility, performance"},
        "sameAs": ["https://github.com/Ilyomix", "https://www.linkedin.com/in/ilyes-abd-lillah", "https://www.cadranapp.com"],
    }
    apps = [
        {"@type": "SoftwareApplication", "@id": f"{SITE}/#cadran", "name": "Cadran", "url": "https://www.cadranapp.com",
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "macOS 14 or later",
         "description": c["projects"][0]["tagline"], "image": f"{SITE}/assets/img/mac-cadran-desktop-1600.webp",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
         "author": {"@id": f"{SITE}/#person"}, "creator": {"@id": f"{SITE}/#person"}},
        {"@type": "WebApplication", "@id": f"{SITE}/#lift", "name": "Lift", "url": "https://ilyomix.github.io/lift/",
         "applicationCategory": "HealthApplication", "operatingSystem": "iOS, Android, Web", "browserRequirements": "Requires JavaScript",
         "description": c["projects"][1]["tagline"], "image": f"{SITE}/assets/img/lift-home-{'en' if en else 'fr'}-780.webp",
         "isAccessibleForFree": True, "codeRepository": "https://github.com/Ilyomix/lift", "inLanguage": ["fr", "en"],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
         "author": {"@id": f"{SITE}/#person"}, "creator": {"@id": f"{SITE}/#person"}},
        {"@type": "WebApplication", "@id": f"{SITE}/#led-board", "name": "Crypto LED Board", "url": "https://crypto-led-board.vercel.app/",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "browserRequirements": "Requires JavaScript",
         "description": c["projects"][2]["tagline"], "image": f"{SITE}/assets/img/mac-led-board-1600.webp",
         "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
         "author": {"@id": f"{SITE}/#person"}, "creator": {"@id": f"{SITE}/#person"}},
    ]
    graph = [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Ilyes Abd-Lillah",
         "alternateName": ["Ilyomix", "Ilyes Abd-Lillah portfolio"], "inLanguage": ["en", "fr"],
         "publisher": {"@id": f"{SITE}/#person"}},
        {"@type": "ProfilePage", "@id": f"{c['url']}#page", "url": c["url"], "name": c["meta"]["title"],
         "description": c["meta"]["description"], "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#website"},
         "about": {"@id": f"{SITE}/#person"}, "mainEntity": {"@id": f"{SITE}/#person"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/assets/og/og-{lang}.png", "width": 1200, "height": 630},
         "dateModified": TODAY,
         "hasPart": [{"@id": a["@id"]} for a in apps]},
        person, *apps,
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    # keep spaces inside calc/clamp expressions around + and -
    return css.strip()


def main():
    from jinja2 import StrictUndefined
    env = Environment(undefined=StrictUndefined, loader=FileSystemLoader(str(BUILD)), autoescape=select_autoescape(["html", "j2"]),
                      trim_blocks=True, lstrip_blocks=True)
    tpl = env.get_template("page.html.j2")
    css = Markup(minify_css((BUILD / "site.css").read_text()))
    for lang, out in (("en", ROOT / "index.html"), ("fr", ROOT / "fr" / "index.html")):
        c = content(lang)
        html = tpl.render(c=c, css=css, jsonld=Markup(jsonld(c)), icon=icon, site=SITE, email=EMAIL, year=YEAR)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print("wrote", out.relative_to(ROOT), len(html.encode()) // 1024, "KB")

    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    sm = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
    for loc, lang in ((f"{SITE}/", "en"), (f"{SITE}/fr/", "fr")):
        sm += f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>
    <xhtml:link rel="alternate" hreflang="fr" href="{SITE}/fr/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
    <image:image><image:loc>{SITE}/assets/img/mac-cadran-desktop-2400.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/assets/img/lift-home-{lang}-780.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/assets/img/mac-led-board-2400.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/assets/img/ilyes-460.webp</image:loc></image:image>
  </url>
"""
    sm += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)

    (ROOT / "llms.txt").write_text(f"""# Ilyes Abd-Lillah

> Software & design engineer based in Toulouse, France (also known as Ilyomix). {YEARS}+ years building fast, accessible product interfaces in React and TypeScript, design systems, and native macOS apps in Swift and SwiftUI. Lead Frontend Engineer on FoodPilot at Positive Solutions.

- Site (English): {SITE}/
- Site (French): {SITE}/fr/
- GitHub: https://github.com/Ilyomix
- LinkedIn: https://www.linkedin.com/in/ilyes-abd-lillah
- Email: {EMAIL}

## Products

- [Cadran](https://www.cadranapp.com): a macOS app that draws live clock faces on the wallpaper layer, behind the icons, on every Space and display. Swift, SwiftUI, Core Animation, Next.js site. Featured on Product Hunt, listed in Awesome Mac.
- [Lift](https://ilyomix.github.io/lift/): a research-based hypertrophy program as an installable web app (PWA), bilingual, offline, no account. React, TypeScript, Vite. Source: https://github.com/Ilyomix/lift
- [Crypto LED Board](https://crypto-led-board.vercel.app/): a live crypto dashboard rendered as a pixel-art LED matrix, fed over WebSockets. React, TypeScript, Canvas / WebGL.

## Experience

- 2026: Founder, Cadran
- 2023 to today: Lead Frontend Engineer, FoodPilot (Positive Solutions)
- 2021 to 2023: Technical Lead Frontend, Skilleos
- 2020 to 2021: Technical Lead Frontend, Guidap
- 2019 to 2020: Frontend Developer, Continental; Frontend Consultant, WE+
- 2016 to 2019: Frontend Developer, Maestro Corporation
- 2012 to 2017: EPITECH, Expert en Technologies de l'Information
""")

    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": "Ilyes Abd-Lillah", "short_name": "Ilyes", "start_url": "/", "display": "browser",
        "background_color": "#0e0f12", "theme_color": "#0e0f12",
        "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/assets/icons/icon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }, indent=2) + "\n")

    # 404 page: a small standalone page in both languages, same look.
    c = content("en")
    page404 = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Ilyes Abd-Lillah</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icons/icon.svg" type="image/svg+xml">
<style>{css}</style>
</head>
<body>
<main class="wrap" style="min-height:100svh;display:grid;align-content:center;gap:28px;padding-block:64px">
  <h1 class="display h-section">This page doesn’t exist.</h1>
  <p class="lede" lang="fr">Cette page n’existe pas.</p>
  <div class="actions"><a class="btn btn-primary" href="/">Back to the site</a><a class="btn" href="/fr/" lang="fr">Retour au site</a></div>
</main>
</body>
</html>
"""
    (ROOT / "404.html").write_text(page404)
    print("wrote robots.txt, sitemap.xml, llms.txt, site.webmanifest, 404.html")


if __name__ == "__main__":
    main()
