#!/usr/bin/env python3
"""Renders the share images assets/og/og-en.png and og-fr.png (1200 x 630) with Playwright.

Run from the repository root after build.py:  python3 _build/og.py
"""
import asyncio, pathlib
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = pathlib.Path(__file__).resolve().parent

VARIANTS = {
    "en": {"role": ["software & design engineer."], "place": "Toulouse, France", "size": 108, "strip_top": 376},
    "fr": {"role": ["software & design engineer."], "place": "Toulouse, France", "size": 108, "strip_top": 376},
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
            await page.screenshot(path=str(out / f"og-{lang}.png"))
            tmp.unlink()
            print("wrote", (out / f"og-{lang}.png").relative_to(ROOT))
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
