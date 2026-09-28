#!/usr/bin/env python3
"""Renders the share images assets/og/og-en.jpg and og-fr.jpg (1200 x 630) with Playwright.

Run from the repository root after build.py:  python3 _build/og.py
"""
import asyncio, pathlib
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = pathlib.Path(__file__).resolve().parent

ICONS = {"cadran": "/assets/img/cadran-icon-112.webp", "lift": "/assets/lift-icon.svg", "led": "/assets/crypto-led-board-icon.svg"}
VARIANTS = {
    "en": [
        {"name": "Cadran", "what": "A clock app that draws on your Mac wallpaper", "icon": ICONS["cadran"]},
        {"name": "Lift", "what": "A research-based training app for the iPhone", "icon": ICONS["lift"]},
        {"name": "Crypto LED Board", "what": "Live crypto markets on a pixel-art LED matrix", "icon": ICONS["led"]},
    ],
    "fr": [
        {"name": "Cadran", "what": "Une horloge dessinée sur le fond d’écran du Mac", "icon": ICONS["cadran"]},
        {"name": "Lift", "what": "Une appli d’entraînement fondée sur la recherche", "icon": ICONS["lift"]},
        {"name": "Crypto LED Board", "what": "Les marchés crypto en direct sur une matrice LED", "icon": ICONS["led"]},
    ],
}


async def main():
    tpl = Environment(loader=FileSystemLoader(str(BUILD))).get_template("og.html.j2")
    out = ROOT / "assets" / "og"
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for lang, products in VARIANTS.items():
            html = tpl.render(lang=lang, root=ROOT.as_uri(), products=products)
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
