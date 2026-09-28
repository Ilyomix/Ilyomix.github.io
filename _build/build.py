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
            "description": L("Software & design engineer basé à Toulouse. Près de dix ans à concevoir et construire des interfaces produit rapides et accessibles en React et TypeScript, et des apps macOS en SwiftUI.",
                             "Software & design engineer based in Toulouse. Nearly a decade designing and building fast, accessible product interfaces in React and TypeScript, and native macOS apps in SwiftUI."),
            "og_title": "Ilyes Abd-Lillah · Software & Design Engineer",
            "og_description": L("Software & design engineer basé à Toulouse, Lead Frontend Engineer chez FoodPilot après près de dix ans à construire des interfaces produit. Apps créées : Cadran (2 500+ téléchargements), Lift et Crypto LED Board.",
                                "Software & design engineer based in Toulouse, Lead Frontend Engineer at FoodPilot after nearly a decade building product interfaces. Apps I’ve built: Cadran (2,500+ downloads), Lift and Crypto LED Board."),
            "og_alt": L("Portrait d’Ilyes Abd-Lillah, software & design engineer basé à Toulouse, Lead Frontend Engineer chez FoodPilot, avec ses apps Cadran, Lift et Crypto LED Board.",
                        "Portrait of Ilyes Abd-Lillah, software & design engineer based in Toulouse, Lead Frontend Engineer at FoodPilot, with his apps Cadran, Lift and Crypto LED Board."),
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
            "lede": L("Je conçois et construis des logiciels, avec autant de soin pour l’interface que pour le code qui la fait tourner.",
                      "I design and build software, with as much care for the interface as for the code that runs it."),
            "facts": L("Lead Frontend Engineer chez FoodPilot · près de dix ans d’expérience",
                       "Lead Frontend Engineer at FoodPilot · nearly ten years of experience"),
            "cta_mail": L("M’écrire", "Email me"),
            "based": L("Basé à Toulouse", "Based in Toulouse"),
            "cta_work": L("Voir les projets", "See the work"),
            "portrait_alt": L("Ilyes Abd-Lillah, en chemise, sur un toit à Toulouse.", "Ilyes Abd-Lillah in a shirt on a rooftop in Toulouse."),
        },
        "stage": {
            "title": L("Conçus, construits, publiés.", "Designed, built, shipped."),
            "lede": L("Trois produits personnels, menés de l’idée à la mise en ligne : sur Mac, sur iPhone et sur le web.",
                      "Three products of my own, taken from idea to release: on the Mac, the iPhone and the web."),
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
        "work": {
            "title": L("Projets.", "Selected work."),
            "lede": L("Pour chacun, le design, le code et la mise en ligne sont de moi.",
                      "For each one, the design, the code and the release are mine."),
        },
        "projects": [
            {
                "id": "cadran", "name": "Cadran", "icon": "/assets/img/cadran-icon-112.webp", "light": "cadran", "glow": "#ff7a4d",
                "tagline": L("Une horloge de bureau pour macOS, dessinée sur le fond d’écran.", "A desktop clock for macOS, drawn on the wallpaper."),
                "body": [L("Cadran dessine des cadrans vivants sur la couche du fond d’écran, derrière les icônes, sur chaque Space et chaque écran. J’ai dessiné les cadrans et construit l’app SwiftUI native, son rendu Core Animation économe en énergie, l’économiseur d’écran et le site produit.",
                           "Cadran draws live clock faces on the wallpaper layer, behind the icons, on every Space and every display. I designed the faces and built the native SwiftUI app, its low-energy Core Animation rendering, the screen saver and the product site.")],
                "specs": [
                    (L("Rôle", "Role"), L("Fondateur · design et ingénierie", "Founder · design and engineering")),
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
                    "faces_title": L("Les cadrans", "The faces"),
                    "faces_note": L("chacun dessiné pour le fond d’écran du Mac.", "each one drawn for the Mac wallpaper."),
                    "faces": [face(sl) for sl in FACES],
                    "tiles": [
                        {**img(f"cadran-feat-{n}", [720, 1200], 1200, h, "(min-width: 760px) 30vw, (min-width: 480px) 46vw, 92vw", alt), "title": t, "caption": cap}
                        for n, h, t, cap, alt in [
                            ("editor", 776, L("L’éditeur", "The editor"), L("Chaque cadran se règle sur place, sur le bureau.", "Every face is tuned in place, on the desktop."), L("L’éditeur de Cadran : couleurs, police et réglages du cadran.", "Cadran’s editor: colours, type and face settings.")),
                            ("per-monitor-setup", 800, L("Un cadran par écran", "A face per display"), L("Chaque écran garde son propre cadran.", "Every display keeps its own face."), L("Les réglages d’un cadran différent pour chaque écran.", "Settings for a different face on each display.")),
                            ("per-face-colors", 799, L("Couleurs par cadran", "Colors per face"), L("Une palette pour chaque cadran.", "A palette for every face."), L("Le choix des couleurs d’un cadran.", "Choosing a face’s colours.")),
                            ("move-resize", 776, L("Déplacer", "Move"), L("L’horloge se place où l’on veut.", "Put the clock anywhere."), L("Une horloge déplacée sur le bureau.", "A clock moved across the desktop.")),
                            ("resize-hide-clock", 776, L("Redimensionner", "Resize"), L("Plus grand, plus petit ou caché.", "Bigger, smaller or hidden."), L("Une horloge redimensionnée sur le bureau.", "A clock resized on the desktop.")),
                            ("screensaver", 776, L("Économiseur d’écran", "Screen saver"), L("Le même cadran quand le Mac se repose.", "The same face when the Mac rests."), L("Les réglages de l’économiseur d’écran de Cadran.", "Cadran’s screen saver settings.")),
                        ]
                    ],
                },
            },
            {
                "id": "lift", "name": "Lift", "icon": "/assets/lift-icon.svg", "light": "lift", "glow": "#3d7bff",
                "tagline": L("Un programme de musculation fondé sur la recherche, installé comme une app sur l’iPhone.", "A research-based training program, installed like an app on the iPhone."),
                "body": [
                    L("Lift construit un plan d’entraînement complet à rebours depuis une date objectif, puis guide chaque séance série par série : il chronomètre les repos et ajuste les charges d’après ce qu’on soulève vraiment.",
                      "Lift builds a complete training plan backwards from a goal date, then guides each session set by set: it times the rests and adjusts the loads from what you actually lift."),
                    L("Ses règles s’appuient sur la recherche en sciences du sport. Il fonctionne hors ligne, en français et en anglais, sans compte : tout reste sur le téléphone.",
                      "Its rules come from sports science research. It works offline, in French and English, with no account: everything stays on the phone."),
                ],
                "specs": [
                    (L("Rôle", "Role"), L("Design et ingénierie", "Design and engineering")),
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
                        ("onboarding", L("Accueil", "Welcome"), L("Le plan part d’une date objectif.", "The plan starts from a goal date."), L("L’écran d’accueil de Lift.", "Lift’s welcome screen."), "0.2"),
                        ("today", L("Aujourd’hui", "Today"), L("L’avancement et la prochaine séance.", "Progress so far and the next session."), L("L’écran Aujourd’hui : séances restantes, phases du plan et prochaine séance.", "Today: sessions to go, the plan’s phases and the next session."), "0.8"),
                        ("session", L("En séance", "In a session"), L("Séries, charges et minuteur de repos.", "Sets, loads and the rest timer."), L("Une séance guidée : prescription, séries et minuteur.", "A guided session: prescription, sets and the timer."), "0.3"),
                        ("calendar", L("Calendrier", "Calendar"), L("Tout le plan, semaine par semaine.", "The whole plan, week by week."), L("Le calendrier : blocs, rotation des séances et phases.", "The calendar: blocks, the session rotation and phases."), "0.9"),
                        ("progress", L("Progrès", "Progress"), L("Force, poids et volume dans le temps.", "Strength, weight and volume over time."), L("L’écran Progrès : force estimée par exercice.", "Progress: estimated strength per exercise."), "0.4"),
                    ]
                ]},
            },
            {
                "id": "led-board", "name": "Crypto LED Board", "icon": "/assets/crypto-led-board-icon.svg?v=dark-orange", "light": "led", "glow": "#ff3f5c",
                "tagline": L("Un tableau de bord crypto en direct, sur une matrice LED en pixel art.", "A live crypto dashboard on a pixel-art LED matrix."),
                "body": [L("On choisit une plateforme et une paire, puis on suit le prix, les graphiques, le carnet d’ordres et la profondeur de marché en temps réel. Tout est dessiné sur une matrice LED responsive, avec une typographie bitmap sur mesure et des effets CRT, alimentés en direct par WebSocket.",
                           "Pick an exchange and a pair, then follow the price, charts, order book and market depth in real time. Everything is drawn on a responsive LED matrix, with custom bitmap type and CRT effects, fed live over WebSockets.")],
                "specs": [
                    (L("Rôle", "Role"), L("Design et ingénierie", "Design and engineering")),
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
                {"value": YEARS, "suffix": "+", "display": f"{YEARS}+", "label": L("ans d’expérience", "years of experience")},
                {"value": 2500, "suffix": "+", "display": L("2\u00a0500+", "2,500+"), "label": L("téléchargements de Cadran, en distribution directe", "Cadran downloads, distributed directly")},
                {"value": 5, "suffix": "", "display": "5", "label": L("recommandations sur LinkedIn", "recommendations on LinkedIn")},
                {"value": 3, "suffix": "", "display": "3", "label": L("langues : français, anglais, arabe", "languages: French, English, Arabic")},
            ],
        },
        "reco": {
            "title": L("Ce qu’ils en disent.", "In their words."),
            "lede": L("Extraits de recommandations reçues sur LinkedIn.", "Excerpts from recommendations on LinkedIn."),
            "quotes": [
                {"lang": "en", "text": "He is an incredibly dedicated and passionate professional who brings a high level of craftsmanship to what he builds. Ilyes has a great eye for detail, delivering pixel-perfect frontends that demonstrate his commitment to quality and UX.",
                 "who": L("Un collègue de l’équipe FoodPilot", "A colleague on the FoodPilot team"), "context": "Positive Solutions"},
                {"lang": "fr", "text": "C'est un professionnel que je recommande vivement. Il est impliqué, il est passionné et grâce à lui j'ai appris énormément.",
                 "who": "Mehdi T.", "context": L("Deux ans ensemble chez Skilleos", "Two years together at Skilleos")},
            ],
            "more": L("Lire les cinq sur LinkedIn", "Read all five on LinkedIn"),
        },
        "others": {
            "title": L("Autres projets", "Other projects"),
            "list": [
                {"when": "Open source", "name": "Crypto Sensor", "href": None,
                 "what": L("Un tableau de bord d’analyse du marché crypto, construit en une journée avec Next.js et TypeScript.",
                           "A crypto market analytics dashboard, built in a day with Next.js and TypeScript.")},
                {"when": "2024", "name": "PeekFi", "href": "https://peekfi.netlify.app",
                 "what": L("Un suivi des cryptomonnaies en temps réel, avec tendances et recherche, en React.",
                           "A real-time crypto tracker with trends and search, in React.")},
                {"when": "2018", "name": "Liberty Rider × MACIF", "href": None,
                 "what": L("Le site vitrine du partenariat entre Liberty Rider et la MACIF, et de ses avantages pour les assurés.",
                           "The showcase site for the Liberty Rider and MACIF partnership and its benefits for policyholders.")},
                {"when": L("2014 → 2017", "2014 → 2017"), "name": "Envio", "href": None,
                 "what": L("Une solution domotique intelligente, conçue en équipe pendant Epitech.",
                           "A smart home system, built as a team during Epitech.")},
            ],
        },
        "about": {
            "title": L("À propos.", "About."),
            "body": [
                Markup(L(f"Je travaille là où le design et l’ingénierie se rejoignent. Depuis près de dix ans, j’aide des équipes à livrer des interfaces produit, à mettre en place des design systems et à soigner chaque détail d’interaction, jusqu’à ce que le logiciel paraisse évident.",
                         f"I work where design and engineering meet. For nearly a decade, I’ve helped teams ship product interfaces, set up design systems and turn interaction details into software that feels intentional.")),
                L("Aujourd’hui, je dirige le frontend de FoodPilot chez Positive Solutions et je construis mes propres produits à côté. Je suis aussi à l’aise pour affiner l’API d’un composant que la courbe d’une transition.",
                  "Today I lead frontend engineering on FoodPilot at Positive Solutions and build my own products on the side. I’m as comfortable refining a component API as a transition curve."),
            ],
            "lang_title": L("Langues", "Languages"),
            "langs": [(L("Français", "French"), L("langue maternelle", "native")), (L("Anglais", "English"), L("courant", "full professional")), (L("Arabe", "Arabic"), L("professionnel", "professional working"))],
            "cares_title": L("Ce qui compte pour moi", "What I care about"),
            "cares": [
                L("Des interfaces à la hiérarchie claire, où chaque animation a une raison d’être", "Interfaces with a clear hierarchy, where every animation has a reason"),
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
            "lede": L("D’abord en équipe produit, puis lead frontend, avec mes propres apps en parallèle.", "Product teams first, then frontend lead roles, with my own apps alongside."),
            "rows": [
                {"when": "2026", "role": L("Fondateur", "Founder"), "org": "Cadran", "href": "https://www.cadranapp.com"},
                {"when": L("2023 → aujourd’hui", "2023 → today"), "role": "Lead Frontend Engineer", "org": "FoodPilot · Positive Solutions", "href": "https://foodpilot.io"},
                {"when": "2021 → 2023", "role": "Technical Lead Frontend", "org": "Skilleos", "href": "https://www.skilleos.com"},
                {"when": "2020 → 2021", "role": "Technical Lead Frontend", "org": "Guidap", "href": "https://guidap.com"},
                {"when": "2019 → 2020", "role": L("Développeur frontend", "Frontend Developer"), "org": "Continental", "href": "https://www.continental.com"},
                {"when": "2019 → 2020", "role": L("Consultant frontend", "Frontend Consultant"), "org": "WE+", "href": None},
                {"when": "2016 → 2019", "role": L("Développeur frontend", "Frontend Developer"), "org": "Maestro Corporation", "href": None},
                {"when": "2012 → 2017", "role": "Expert en Technologies de l’Information", "org": "EPITECH", "href": "https://www.epitech.eu"},
                {"when": "2013", "role": L("Prix So’Créativ", "So’Créativ prize"), "org": "So Toulouse · Epitech × ISEG", "href": None},
            ],
        },
        "contact": {
            "title": L("Travaillons ensemble.", "Let’s work together."),
            "lede": L("Un projet, un poste ou simplement un bonjour : écrivez-moi.", "A project, a role or just a hello: write to me."),
            "time_before": L("Il est ", "It’s "),
            "time_after": L(" à Toulouse.", " in Toulouse."),
        },
        "footer": {"line": L("Conçu et construit à Toulouse.", "Designed and built in Toulouse."), "nav_label": L("Liens", "Links")},
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
        "knowsLanguage": ["fr", "en", "ar"],
        "award": ["Prix So’Créativ, So Toulouse (2013)"],
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
- Other projects: Crypto Sensor (open source crypto analytics dashboard, Next.js), PeekFi (crypto tracker, React), Liberty Rider × MACIF (showcase site, 2018), Envio (smart home system, Epitech, 2014–2017).

## Facts

- Cadran: self-distributed, more than 2,500 downloads
- 5 recommendations on LinkedIn
- Languages: French (native), English (full professional), Arabic (professional working)
- Prix So'Créativ, So Toulouse (2013)

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
