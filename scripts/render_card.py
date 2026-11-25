"""Yeşil Mühendis kartını (.dc.html) 1080x1350 PNG'ye çevirir.

Kullanım: python3 -I scripts/render_card.py KartNN.dc.html cikti.png
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

GROUND = "#0F3D2E"
ACCENT = "#F2B544"


def to_plain_html(src: str) -> str:
    s = src.replace("{{ground}}", GROUND).replace("{{accent}}", ACCENT)
    s = re.sub(r'<script src="\./support\.js"></script>\s*', "", s)
    s = re.sub(r'<script type="text/x-dc".*?</script>', "", s, flags=re.S)
    s = s.replace("<x-dc>", "").replace("</x-dc>", "")
    s = s.replace("<helmet>", "").replace("</helmet>", "")
    # Fontlar yüklenemezse benzer sistem fontlarına düş
    fallback = "<style>body{margin:0}*{font-synthesis:none}</style>"
    s = s.replace("</head>", fallback + "</head>", 1)
    return s


def main() -> None:
    src = Path(sys.argv[1]).read_text(encoding="utf-8")
    out = Path(sys.argv[2])
    html = to_plain_html(src)
    tmp = out.with_suffix(".render.html")
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome") if Path("/usr/bin/google-chrome").exists() else p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.goto(tmp.resolve().as_uri(), wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(800)
        overflow = page.evaluate(
            "() => { const r = document.body.firstElementChild; return r ? r.scrollHeight - r.clientHeight : 0 }"
        )
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        browser.close()
    tmp.unlink(missing_ok=True)
    print(f"ok {out} overflow_px={overflow}")


if __name__ == "__main__":
    main()
