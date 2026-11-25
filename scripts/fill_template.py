"""Şablondaki {{ALAN}} yerlerini JSON'daki değerlerle doldurur (HTML kaçışlı).

Kullanım: python3 -I scripts/fill_template.py templates/gunun-bilgisi.html veriler.json cikti.html
"""
import html
import json
import sys
from pathlib import Path

tpl = Path(sys.argv[1]).read_text(encoding="utf-8")
data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
for key, value in data.items():
    tpl = tpl.replace("{{" + key + "}}", html.escape(str(value)))
missing = [part.split("}}")[0] for part in tpl.split("{{")[1:]]
if missing:
    sys.exit(f"Doldurulmamış alanlar: {missing}")
Path(sys.argv[3]).write_text(tpl, encoding="utf-8")
print("ok")
