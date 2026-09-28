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

FACES = ["pura-night", "orbit-dynamic-sky", "prose-blue", "clima-teal", "departure-charcoal", "spectrum-black",
         "sablier-graphite", "cipher-midnight", "adage-paper", "syntax-berry", "platform-indigo", "phase-purple",
         "titan-coral", "foundry-slate", "quartz-cyan", "dessau-ocean", "metric-rose", "horizon-sunrise",
         "halftone-forest", "arcade-green"]

PHONE = (868, 1785)


def content(lang):
    en = lang == "en"
    L = lambda f, e: e if en else f
    ph = lambda name, sizes, alt: img(name, [280, 560, 868], PHONE[0], PHONE[1], sizes, alt)
    mbp = lambda sizes, alt: img("mac-cadran-desktop", [640, 960, 1600, 2400], 2400, 1449, sizes, alt)
    studio = lambda sizes, alt: img("mac-led-board", [640, 960, 1600, 2400], 2400, 1844, sizes, alt)

    def face(slug):
        name = slug.split("-")[0].capitalize()
        return {"src": f"/assets/img/face-{slug}-{lang}.webp", "name": name,
                "alt": L(f"Le cadran {name} de Cadran sur un Mac", f"Cadran’s {name} clock face on a Mac")}

    return {
        "lang": lang,
        "url": f"{SITE}/" if en else f"{SITE}/fr/",
        "home": "/" if en else "/fr/",
        "og_locale": "en_US" if en else "fr_FR",
        "og_locale_alt": "fr_FR" if en else "en_US",
        "alt": {"href": "/fr/", "lang": "fr", "long": "Français"} if en else {"href": "/", "lang": "en", "long": "English"},
        "meta": {
            "title": L("Ilyes Abd-Lillah · Software & Design Engineer à Toulouse",
                       "Ilyes Abd-Lillah · Software & Design Engineer in Toulouse"),
            "description": L(f"Software & design engineer à Toulouse. {YEARS}+ ans à concevoir et construire des interfaces produit rapides et accessibles en React et TypeScript, des design systems et des apps macOS en SwiftUI.",
                             f"Software & design engineer in Toulouse. {YEARS}+ years designing and building fast, accessible product interfaces in React and TypeScript, design systems and native macOS apps in SwiftUI."),
            "og_title": "Ilyes Abd-Lillah · Software & Design Engineer",
            "og_description": L("Je conçois et développe des logiciels : Cadran, une horloge sur le fond d’écran du Mac ; Lift, une appli d’entraînement fondée sur la recherche ; Crypto LED Board, un dashboard crypto en direct. Toulouse, France.",
                                "I design and build software: Cadran, a clock on your Mac wallpaper; Lift, a research-based training app; Crypto LED Board, a live crypto dashboard. Toulouse, France."),
            "og_alt": L("Portrait d’Ilyes Abd-Lillah, software & design engineer à Toulouse, avec ses trois produits : Cadran, Lift et Crypto LED Board.",
                        "Portrait of Ilyes Abd-Lillah, software & design engineer in Toulouse, with his three products: Cadran, Lift and Crypto LED Board."),
        },
        "ui": {
            "skip": L("Aller au contenu", "Skip to content"),
            "home_label": L("Ilyes Abd-Lillah, accueil", "Ilyes Abd-Lillah, home"),
            "nav_label": "Sections",
            "to_light": L("Passer en mode clair", "Switch to light mode"),
            "to_dark": L("Passer en mode sombre", "Switch to dark mode"),
            "lang_label": L("Langue", "Language"),
        },
        "nav": [
            {"id": "work", "label": L("Projets", "Work")},
            {"id": "about", "label": L("À propos", "About")},
            {"id": "experience", "label": L("Parcours", "Experience")},
            {"id": "contact", "label": "Contact"},
        ],
        "hero": {
            "lede": L("Je transforme des idées produit complexes en interfaces rapides et accessibles, je construis les design systems qui aident les équipes à les livrer, et je fais des apps macOS natives en SwiftUI.",
                      "I turn complex product ideas into fast, accessible interfaces, build the design systems that help teams ship them, and make native macOS apps in SwiftUI."),
            "facts": Markup(L(f"{Y}+ ans · Lead Frontend chez FoodPilot · Toulouse, France",
                              f"{Y}+ years · Lead Frontend at FoodPilot · Toulouse, France")),
            "cta_mail": L("M’écrire", "Email me"),
            "cta_work": L("Voir les projets", "See the work"),
            "portrait_alt": L("Ilyes Abd-Lillah, en chemise, sur un toit à Toulouse.", "Ilyes Abd-Lillah in a shirt on a rooftop in Toulouse."),
        },
        "stage": {
            "title": L("Conçu, développé, publié.", "Designed, built, shipped."),
            "lede": L("Trois produits que j’ai faits de A à Z, sur Mac, sur iPhone et dans le navigateur.",
                      "Three products I made end to end, on the Mac, on the iPhone and in the browser."),
            "alt": L("Un bureau avec un Studio Display qui affiche Crypto LED Board, un MacBook Pro et un MacBook Air qui affichent Cadran, et deux téléphones qui affichent Lift.",
                     "A desk with a Studio Display showing Crypto LED Board, a MacBook Pro and a MacBook Air showing Cadran, and two phones showing Lift."),
            "legend_label": L("Les projets", "The projects"),
            "devices": [
                {"kind": "display", "cls": "", "eager": True, "img": studio("(min-width: 1400px) 670px, (min-width: 760px) 49vw, 74vw", "")},
                {"kind": "mbp", "cls": "", "eager": True, "img": mbp("(min-width: 1400px) 560px, (min-width: 760px) 41vw, 62vw", "")},
                {"kind": "mba", "cls": "", "eager": False, "img": img("mac-cadran-weather", [640, 1000, 1400], 1400, 848, "(min-width: 1400px) 490px, (min-width: 760px) 36vw, 54vw", "")},
                {"kind": "phone", "cls": "p1", "eager": False, "img": ph(f"phone-lift-today-{lang}", "(min-width: 1400px) 126px, (min-width: 760px) 9.2vw, 14vw", "")},
                {"kind": "phone", "cls": "p2", "eager": False, "img": ph(f"phone-lift-session-{lang}", "(min-width: 1400px) 126px, (min-width: 760px) 9.2vw, 14vw", "")},
            ],
            "legend": [
                {"id": "cadran", "name": "Cadran", "icon": "/assets/img/cadran-icon-112.webp"},
                {"id": "lift", "name": "Lift", "icon": "/assets/lift-icon.svg"},
                {"id": "led-board", "name": "Crypto LED Board", "icon": "/assets/crypto-led-board-icon.svg?v=dark-orange"},
            ],
        },
        "reel": {
            "title": L("Vingt cadrans, un fond d’écran.", "Twenty faces, one wallpaper."),
            "note": L("Cadran · 22 cadrans dans l’app", "Cadran · 22 clock faces in the app"),
            "rows": [[face(s) for s in FACES[:10]], [face(s) for s in FACES[10:]]],
        },
        "work": {
            "title": L("Projets.", "Selected work."),
            "lede": L("Chaque produit est conçu, développé et publié par moi, du premier croquis à la mise en ligne.",
                      "Each product is designed, engineered and shipped by me, from the first sketch to release."),
        },
        "projects": [
            {
                "id": "cadran", "name": "Cadran", "icon": "/assets/img/cadran-icon-112.webp", "light": "cadran", "glow": "#ff7a4d",
                "tagline": L("Une horloge de bureau pour macOS, dessinée sur le fond d’écran.", "A desktop clock for macOS, drawn on the wallpaper."),
                "body": [L("Cadran affiche des cadrans vivants sur la couche du fond d’écran, derrière les icônes, sur chaque Space et chaque écran. Une app SwiftUI native, un rendu Core Animation pensé pour consommer peu d’énergie, un mode économiseur d’écran et un site produit en Next.js.",
                           "Cadran renders live clock faces on the wallpaper layer, behind the icons, on every Space and display. A native SwiftUI app, Core Animation rendering tuned for low energy use, a screen saver mode and a Next.js product site.")],
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
                "media": {
                    "main": mbp("(min-width: 1300px) 1200px, 92vw", L("Cadran sur un MacBook Pro : une horloge à palettes sur le fond d’écran, avec le morceau en cours de lecture.",
                                                                       "Cadran on a MacBook Pro: a flip clock on the wallpaper, with the track now playing.")),
                    "pair": [
                        {**img("mac-cadran-weather", [640, 1000, 1400], 1400, 848, "(min-width: 760px) 46vw, 92vw",
                               L("Cadran sur un MacBook Air : un cadran avec la météo en direct au-dessus d’un paysage de lac.", "Cadran on a MacBook Air: a face with live weather over a lake wallpaper.")),
                         "title": L("Météo et calendrier", "Weather and calendar"), "caption": L("des complications en direct, sans widget.", "live complications, no widget.")},
                        {**img("mac-cadran-gallery", [640, 1000, 1400], 1400, 848, "(min-width: 760px) 46vw, 92vw",
                               L("La galerie de Cadran sur un MacBook Air : tous les cadrans en aperçu.", "Cadran’s gallery on a MacBook Air: every face previewed.")),
                         "title": L("La galerie", "The gallery"), "caption": L("tous les cadrans, en aperçu vivant.", "every face, previewed live.")},
                    ],
                    "tiles": [
                        {**img(f"cadran-feat-{n}", [720, 1200], 1200, h, "(min-width: 760px) 30vw, (min-width: 480px) 46vw, 92vw", alt), "title": t, "caption": cap}
                        for n, h, t, cap, alt in [
                            ("editor", 776, L("L’éditeur", "The editor"), L("Chaque cadran se règle sur place, sur le bureau.", "Every face is tuned in place, on the desktop."), L("L’éditeur de Cadran : couleurs, police et réglages du cadran.", "Cadran’s editor: colours, type and face settings.")),
                            ("per-monitor-setup", 800, L("Un cadran par écran", "A face per display"), L("Chaque écran garde son propre cadran.", "Every display keeps its own face."), L("Les réglages d’un cadran différent pour chaque écran.", "Settings for a different face on each display.")),
                            ("per-face-colors", 799, L("Couleurs par cadran", "Colours per face"), L("Une palette pour chaque cadran.", "A palette for every face."), L("Le choix des couleurs d’un cadran.", "Choosing a face’s colours.")),
                            ("move-resize", 776, L("Déplacer", "Move"), L("L’horloge se place où l’on veut.", "Put the clock anywhere."), L("Une horloge déplacée sur le bureau.", "A clock moved across the desktop.")),
                            ("resize-hide-clock", 776, L("Redimensionner", "Resize"), L("Plus grand, plus petit ou caché.", "Bigger, smaller or hidden."), L("Une horloge redimensionnée sur le bureau.", "A clock resized on the desktop.")),
                            ("screensaver", 776, L("Économiseur d’écran", "Screen saver"), L("Le même cadran quand le Mac se repose.", "The same face when the Mac rests."), L("Les réglages de l’économiseur d’écran de Cadran.", "Cadran’s screen saver settings.")),
                        ]
                    ],
                },
            },
            {
                "id": "lift", "name": "Lift", "icon": "/assets/lift-icon.svg", "light": "lift", "glow": "#3d7bff",
                "tagline": L("Un programme de musculation fondé sur la recherche, à installer sur son téléphone.", "A research-based training program you install on your phone."),
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
                "media": {"phones": [
                    {**ph(f"phone-lift-{s}-{lang}", "(min-width: 1200px) 230px, (min-width: 760px) 18vw, 62vw", alt), "title": t, "caption": cap, "speed": sp}
                    for s, t, cap, alt, sp in [
                        ("onboarding", L("Accueil", "Welcome"), L("Le plan part de ta date.", "The plan starts from your date."), L("L’écran d’accueil de Lift.", "Lift’s welcome screen."), "0.2"),
                        ("today", L("Aujourd’hui", "Today"), L("Où tu en es, et la prochaine séance.", "Where you stand, and the next session."), L("L’écran Aujourd’hui : séances restantes, phases du plan et prochaine séance.", "Today: sessions to go, the plan’s phases and the next session."), "0.8"),
                        ("session", L("En séance", "In a session"), L("Séries, charges, RIR et minuteur.", "Sets, loads, RIR and the timer."), L("Une séance guidée : prescription, séries et minuteur.", "A guided session: prescription, sets and the timer."), "0.3"),
                        ("calendar", L("Calendrier", "Calendar"), L("Blocs, décharges et phases.", "Blocks, deloads and phases."), L("Le calendrier : blocs, rotation des séances et phases.", "The calendar: blocks, the session rotation and phases."), "0.9"),
                        ("progress", L("Progrès", "Progress"), L("1RM estimé, poids et volume.", "Estimated 1RM, weight and volume."), L("L’écran Progrès : force estimée par exercice.", "Progress: estimated strength per exercise."), "0.4"),
                    ]
                ]},
            },
            {
                "id": "led-board", "name": "Crypto LED Board", "icon": "/assets/crypto-led-board-icon.svg?v=dark-orange", "light": "led", "glow": "#ff3f5c",
                "tagline": L("Un dashboard crypto en direct sur une matrice LED en pixel art.", "A live crypto dashboard on a pixel-art LED matrix."),
                "body": [L("On choisit une plateforme et une paire, puis on suit le prix, les graphiques, le carnet d’ordres et la profondeur de marché en temps réel. Tout est dessiné en matrice LED responsive, avec une typographie bitmap sur mesure et des effets CRT, alimentée par WebSocket.",
                           "Pick an exchange and a pair, then follow price, charts, order book and market depth in real time. Everything is drawn as a responsive LED matrix with custom bitmap typography and CRT effects, fed over WebSockets.")],
                "specs": [
                    (L("Rôle", "Role"), L("Design et développement", "Design and engineering")),
                    (L("Plateforme", "Platform"), L("Web · ordinateur et mobile", "Web · desktop and mobile")),
                    (L("Technologies", "Built with"), "React · TypeScript · Vite · WebSockets · Canvas 2D / WebGL"),
                    (L("Données", "Data"), L("Flux de marché en direct", "Live market feeds")),
                ],
                "facts": None,
                "links": [{"label": L("Ouvrir Crypto LED Board", "Open Crypto LED Board"), "href": "https://crypto-led-board.vercel.app/"}],
                "media": {
                    "main": studio("(min-width: 1300px) 1085px, 84vw", L("Crypto LED Board sur un Studio Display : Bitcoin contre USDT, prix, graphique sur un jour, carnet d’ordres et profondeur.",
                                                                         "Crypto LED Board on a Studio Display: Bitcoin against USDT, price, one-day chart, order book and depth.")),
                    "phone": ph("phone-led-board", "(min-width: 1300px) 200px, 17vw", L("Crypto LED Board sur téléphone.", "Crypto LED Board on a phone.")),
                    "caption": L("La même matrice LED, du Studio Display au téléphone.", "The same LED matrix, from a Studio Display to a phone."),
                },
            },
        ],
        "numbers": {
            "label": L("En chiffres", "In numbers"),
            "stats": [
                {"value": YEARS, "suffix": "+", "label": L("ans à concevoir et construire des interfaces", "years designing and building interfaces")},
                {"value": 3, "suffix": "", "label": L("produits conçus et publiés en solo", "products designed and shipped solo")},
                {"value": 22, "suffix": "", "label": L("cadrans dans Cadran", "clock faces in Cadran")},
                {"value": 31, "suffix": "", "label": L("études derrière les règles de Lift", "studies behind Lift’s rules")},
            ],
        },
        "about": {
            "title": L("À propos.", "About."),
            "body": [
                Markup(L(f"Je travaille là où le design et l’ingénierie se rejoignent. Depuis plus de {Y} ans, j’aide des équipes à livrer des interfaces produit, à mettre en place des design systems et à transformer les détails d’interaction en logiciels qui semblent pensés.",
                         f"I work where design and engineering meet. For more than {Y} years I’ve helped teams ship product interfaces, set up design systems and turn interaction details into software that feels intentional.")),
                L("Aujourd’hui, je dirige le frontend de FoodPilot chez Positive Solutions et je construis mes propres produits à côté. Je suis aussi à l’aise pour affiner l’API d’un composant que la courbe d’une transition.",
                  "Today I lead frontend engineering on FoodPilot at Positive Solutions and build my own products on the side. I’m as comfortable refining a component API as a transition curve."),
            ],
            "cares_title": L("Ce qui compte pour moi", "What I care about"),
            "cares": [
                L("Des interfaces produit à la hiérarchie claire, avec un mouvement qui a un sens", "Product interfaces with clear hierarchy and purposeful motion"),
                L("Des design systems qui font gagner du temps sans rien lâcher sur la qualité", "Design systems that help teams move faster without losing quality"),
                L("L’accessibilité, la performance et une architecture solide", "Accessibility, performance and resilient architecture"),
                L("Des expériences macOS natives en Swift et SwiftUI", "Native macOS experiences built with Swift and SwiftUI"),
            ],
            "toolbox": [
                {"title": L("Interfaces produit", "Product UI"), "list": ["React", "Next.js", "Vue.js", "TypeScript", "Tailwind CSS"]},
                {"title": L("Natif et design", "Native and design"), "list": ["Swift", "SwiftUI", "Core Animation", "Figma"]},
                {"title": L("Outils", "Tools"), "list": ["Node.js", "Vite", "GSAP", "Git", "Docker"]},
            ],
        },
        "xp": {
            "title": L("Parcours.", "Experience."),
            "lede": L("Des postes de lead frontend en entreprise produit, et mes propres apps.", "Frontend lead roles in product companies, and my own apps."),
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
            "lede": L("Un projet en tête, ou simplement envie de dire bonjour ? Écrivez-moi.", "Got a project in mind, or just want to say hello? Write to me."),
            "time_before": L("Il est ", "It’s "),
            "time_after": L(" à Toulouse.", " in Toulouse."),
        },
        "footer": {"line": L("Conçu et développé à Toulouse.", "Designed and built in Toulouse."), "nav_label": L("Liens", "Links")},
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
        "image": {"@type": "ImageObject", "url": f"{SITE}/assets/img/ilyes-portrait.webp", "width": 368, "height": 460},
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
         "description": c["projects"][1]["tagline"], "image": f"{SITE}/assets/img/phone-lift-today-{'en' if en else 'fr'}-868.webp",
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
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/assets/og/og-{lang}.jpg", "width": 1200, "height": 630},
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
    <image:image><image:loc>{SITE}/assets/img/phone-lift-today-{lang}-868.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/assets/img/mac-led-board-2400.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/assets/img/ilyes-portrait.webp</image:loc></image:image>
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
        "background_color": "#0b0c0f", "theme_color": "#0b0c0f",
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
