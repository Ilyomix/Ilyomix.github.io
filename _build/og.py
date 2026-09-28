#!/usr/bin/env python3
"""Renders the share images assets/og/og-en.jpg and og-fr.jpg (1200 x 630) with Playwright.

Run from the repository root after build.py:  python3 _build/og.py
"""
import asyncio, json, pathlib
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = pathlib.Path(__file__).resolve().parent

# Cadran's downloads as read by the last build, floored so the image stays true: 5,207 becomes 5,000+
N = json.loads((BUILD / "stats.json").read_text())["cadran_downloads"]
N = N // (1000 if N >= 2000 else 100) * (1000 if N >= 2000 else 100)
DL = {"en": f"{N:,}+", "fr": f"{N:,}+".replace(",", "\u00a0")}

ICONS = {"cadran": "/assets/img/cadran-icon-112.webp", "lift": "/assets/lift-icon.svg", "led": "/assets/crypto-led-board-icon.svg"}
VARIANTS = {
    "en": {
        "xp": {"now": "Lead Frontend Engineer at FoodPilot", "past": "Nearly ten years of experience · Skilleos, Guidap, Continental"},
        "apps_label": "Apps I’ve built",
        "based": "Based in Toulouse, France",
        "products": [
            {"name": "Cadran", "what": f"a clock on your Mac wallpaper · {DL['en']} downloads", "icon": ICONS["cadran"]},
            {"name": "Lift", "what": "a research-based training app", "icon": ICONS["lift"]},
            {"name": "Crypto LED Board", "what": "live crypto on an LED matrix", "icon": ICONS["led"]},
        ],
    },
    "fr": {
        "xp": {"now": "Lead Frontend Engineer chez FoodPilot", "past": "Près de dix ans d’expérience · Skilleos, Guidap, Continental"},
        "apps_label": "Apps que j’ai créées",
        "based": "Basé à Toulouse, France",
        "products": [
            {"name": "Cadran", "what": f"une horloge sur le fond d’écran du Mac · {DL['fr']} téléchargements", "icon": ICONS["cadran"]},
            {"name": "Lift", "what": "une appli d’entraînement fondée sur la recherche", "icon": ICONS["lift"]},
            {"name": "Crypto LED Board", "what": "la crypto en direct sur une matrice LED", "icon": ICONS["led"]},
        ],
    },
}


async def main():
    tpl = Environment(loader=FileSystemLoader(str(BUILD))).get_template("og.html.j2")
    out = ROOT / "assets" / "og"
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for lang, v in VARIANTS.items():
            html = tpl.render(lang=lang, root=ROOT.as_uri(), **v)
            tmp = BUILD / f".og-{lang}.html"
            tmp.write_text(html)
            await page.goto(tmp.as_uri(), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(300)
            png = out / f".og-{lang}.png"
            await page.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(out / f"og-{lang}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
            png.unlink(); tmp.unlink()
            print("wrote", (out / f"og-{lang}.jpg").relative_to(ROOT))
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
