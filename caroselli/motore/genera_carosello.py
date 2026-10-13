"""Generatore di caroselli Instagram PsicoLeva (1080x1350, stile buio e luce, Chibi da solo, senza cervello).
Uso: python3 genera_carosello.py spec.json cartella_uscita
 -> slide-01.png ... slide-NN.png, slide-N.jpg (per il caricamento) e panoramica.png nella cartella di uscita.
Esce con codice 2 se un controllo trova testi sovrapposti o fuori dalla slide (allora accorcia i testi e rigenera).

spec.json = {"slide": [ ... ]}, ogni slide ha "tipo":
  copertina: kicker_n, kicker, bianco, giallo, sottotitolo, espr ("felice"|"scioccato"|"ansioso"|"sicuro"|"serio"),
             posa ("giu"|"fianchi"|"dueman"|"fronte"|"petto"), fili (true = marionetta)
  studio:    n, etichetta, bianco, giallo, testo, chiusa, e UNO tra
             barre  = [[etichetta, percentuale 0-100, accesa], ...]   (2-3 righe)
             numeri = [[etichetta, valore breve es. "8 MESI", acceso], ...] (2 colonne)
  difesa:    kicker, bianco, giallo, testo, testo2, espr
  finale:    bianco, giallo, testo, copertina (percorso PNG 16:9 di una miniatura, facoltativo), cta (default "CERCA PSICOLEVA SU YOUTUBE")
Nei testi <em>parola</em> = parola in giallo. Titoli: max ~22 caratteri per riga (fs automatico).
"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from playwright.sync_api import sync_playwright
from chibi import chibi, HL
from base import DEFS, FONTCSS, CHROME, ombra_terra, QUI

W, H = 1080, 1350
ICONA = base64.b64encode(open(os.path.join(QUI, "icona.png"), "rb").read()).decode()

CSS = FONTCSS + """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#0d0e12;overflow:hidden;font-family:Inter,sans-serif;color:#f3f1ea}
.abs{position:absolute}
.col{position:absolute;left:80px;right:80px;top:78px;bottom:150px;display:flex;flex-direction:column;gap:30px}
.col>*{flex:none}
.chiusa{margin-top:auto;font-size:34px!important;color:#f3f1ea!important}
.kick{font-family:Bebas;font-size:46px;letter-spacing:3px;color:#c9c6bd}
.kick b{color:#FFD200;font-weight:400;margin-right:18px}
.tit{font-family:Bebas;line-height:.98;text-transform:uppercase}
.tit .w{display:block;color:#f3f1ea}
.tit .y{display:inline-block;background:#FFD200;color:#111;padding:6px 22px 0;margin-top:14px;margin-left:-4px}
.txt{font-size:37px;line-height:1.38;color:#d6d3cb;font-weight:500}
.txt em{font-style:normal;color:#FFD200;font-weight:700}
.piede{position:absolute;left:80px;right:80px;bottom:56px;height:56px;display:flex;align-items:center;justify-content:space-between;font-family:Bebas;font-size:34px;letter-spacing:3px;color:#8d8f9a}
.piede .logo{display:flex;align-items:center;gap:16px;color:#c9c6bd}
.piede img{width:52px;height:52px;border-radius:12px}
.riga{margin-bottom:22px}.riga:last-child{margin-bottom:0}
.riga .et{font-size:30px;color:#c9c6bd;font-weight:500;margin-bottom:10px}
.riga .bar{display:flex;align-items:center;gap:22px}
.riga .fill{height:62px;background:#4a4c56;border-radius:6px}
.riga .num{font-family:Bebas;font-size:74px;color:#9a9ca6;line-height:1;padding-top:6px}
.riga.on .fill{background:#FFD200}.riga.on .num{color:#FFD200}.riga.on .et{color:#f3f1ea}
.numeri{display:flex;gap:0;margin-top:20px}
.numeri>div{flex:1;text-align:center;padding:10px 20px}
.numeri>div+div{border-left:3px solid #2e3039}
.numeri .et{font-size:30px;color:#c9c6bd;font-weight:500;line-height:1.3;min-height:80px}
.numeri .v{font-family:Bebas;font-size:120px;line-height:1;color:#c9c6bd;margin-top:12px}
.numeri .on .v{color:#FFD200}.numeri .on .et{color:#f3f1ea}
"""

SOPRA = f'<rect width="{W}" height="{H}" fill="url(#vign)"/><rect width="{W}" height="{H}" filter="url(#grana)"/>'
GLOWF = f'<defs><filter id="glowF" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feGaussianBlur stdDeviation="5" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'


def fondo(cx=540, op=.35):
    return (f'<rect width="{W}" height="{H}" fill="url(#muro)"/>'
            f'<g filter="url(#b40)"><polygon points="{cx-120},0 {cx+120},0 {cx+520},{H} {cx-520},{H}" fill="url(#cono)" opacity="{op}"/></g>')


def BG(op=.35, cx=540, extra=""):
    return f'<svg class="abs" width="{W}" height="{H}">{fondo(cx, op)}{extra}{SOPRA}</svg>'


def alone(cx, cy, rx, ry):
    return f'<g filter="url(#b80)"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#6a5010" opacity=".55"/></g>'


def filo(a, b, c, d):
    return f'<path d="M{a:.0f},{b:.0f} L{c:.0f},{d:.0f}" stroke="{HL}" stroke-width="4" stroke-linecap="round" filter="url(#glowF)"/>'


def col(*parti, extra=""):
    return f'<div class="col" style="{extra}">' + "".join(parti) + "</div>"


def fs_titolo(bianco, giallo, base=128):
    m = max(len(bianco or ""), len(giallo or ""))
    return min(base, int(base * 19 / m)) if m > 19 else base


def titolo(bianco, giallo, fs=None):
    fs = fs or fs_titolo(bianco, giallo)
    w = f'<span class="w">{bianco}</span>' if bianco else ""
    return f'<div class="tit chk" style="font-size:{fs}px">{w}<span class="y">{giallo}</span></div>'


kick = lambda n, t: f'<div class="kick chk"><b>{n}</b>{t}</div>'
txt = lambda t, st="": f'<div class="txt chk" style="{st}">{t}</div>'
chiusa = lambda t: f'<div class="txt chiusa chk">{t}</div>'


def barre(righe):
    s = '<div class="chk" style="margin-top:20px">'
    for et, p, on in righe:
        s += (f'<div class="riga{" on" if on else ""}"><div class="et">{et}</div>'
              f'<div class="bar"><div class="fill" style="width:{max(8, p * 7.2):.0f}px"></div><div class="num">{p}%</div></div></div>')
    return s + "</div>"


def numeri(cols):
    return ('<div class="numeri chk">' + "".join(
        f'<div class="{"on" if on else ""}"><div class="et">{et}</div><div class="v">{v}</div></div>' for et, v, on in cols) + "</div>")


def s_copertina(d):
    s, mx, py = 1.08, 540, 1235
    posa = d.get("posa", "dueman" if d.get("fili") else "fianchi")
    disegno = ombra_terra(mx, py, 100) + chibi(mx, py, s, d.get("espr", "sicuro"), 0, braccia=posa)[0]
    if d.get("fili"):
        ml = (mx - 110 * s, py - 226 * s); mr = (mx + 110 * s, py - 226 * s); testa = (mx, py - 406 * s); cy0 = 560
        disegno += (filo(mx - 184, cy0 + 26, *ml) + filo(mx + 184, cy0 + 26, *mr) + filo(mx, cy0 + 76, testa[0], testa[1] + 4)
                    + f'<g filter="url(#ombraP)"><rect x="{mx-200}" y="{cy0}" width="400" height="26" rx="9" fill="#4a3a2a"/>'
                      f'<rect x="{mx-13}" y="{cy0-44}" width="26" height="120" rx="9" fill="#4a3a2a"/></g>')
    return (BG(.7, extra=alone(540, 930, 380, 320) + f'<g class="chk dis">{disegno}</g>')
            + col(kick(d.get("kicker_n", ""), d.get("kicker", "")), titolo(d["bianco"], d["giallo"], fs_titolo(d["bianco"], d["giallo"], 124)),
                  txt(d.get("sottotitolo", ""), "font-size:34px"), extra="bottom:auto"))


def s_studio(d):
    grafico = barre(d["barre"]) if d.get("barre") else numeri(d["numeri"]) if d.get("numeri") else ""
    return BG() + col(kick(d["n"], d["etichetta"]), titolo(d["bianco"], d["giallo"]), txt(d["testo"]), grafico,
                      chiusa(d.get("chiusa", "")))


def s_difesa(d):
    s7, x7, y7 = 1.0, 810, 1235
    return (BG(.55, cx=810, extra=alone(810, 1000, 240, 240) + ombra_terra(x7, y7, 95)
               + f'<g class="chk dis">{chibi(x7, y7, s7, d.get("espr", "sicuro"), -.4, braccia="fianchi")[0]}</g>')
            + col(kick(d.get("kicker", "LA DIFESA"), d.get("kicker2", "")), titolo(d["bianco"], d["giallo"], fs_titolo(d["bianco"], d["giallo"], 108)),
                  txt(d.get("testo", ""), "width:560px"), txt(d.get("testo2", ""), "color:#f3f1ea;width:560px;margin-top:10px")))


def s_finale(d):
    img = ""
    if d.get("copertina") and os.path.exists(d["copertina"]):
        b = base64.b64encode(open(d["copertina"], "rb").read()).decode()
        img = (f'<div class="chk" style="width:920px;height:518px;border-radius:18px;overflow:hidden;box-shadow:0 20px 60px #000">'
               f'<img src="data:image/png;base64,{b}" style="width:100%;height:100%;display:block"></div>')
    cta = d.get("cta", 'CERCA <span style="color:#FFD200">PSICOLEVA</span> SU YOUTUBE')
    return BG(.45) + col(kick(d.get("kicker", "IL VIDEO"), d.get("kicker2", "COMPLETO")), titolo(d["bianco"], d["giallo"], fs_titolo(d["bianco"], d["giallo"], 116)),
                         txt(d.get("testo", "")), img,
                         f'<div class="chk" style="margin-top:auto;font-family:Bebas;font-size:52px;letter-spacing:2px;color:#f3f1ea">{cta}</div>')


TIPI = {"copertina": s_copertina, "studio": s_studio, "difesa": s_difesa, "finale": s_finale}

CHECK = """() => { const r = [...document.querySelectorAll('.chk, .piede')].map(e => [String(e.className.baseVal ?? e.className), e.getBoundingClientRect()]);
 const out = []; for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) { const a = r[i][1], b = r[j][1];
 if ((r[i][0]+r[j][0]).includes('dis') && (r[i][0]+r[j][0]).includes('piede')) continue; if (a.width && b.width && a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) out.push(r[i][0] + ' x ' + r[j][0]); }
 return out.concat(r.filter(x => x[1].bottom > 1351 || x[1].right > 1081).map(x => 'fuori: ' + x[0])); }"""


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slides = spec["slide"]; n = len(slides); problemi = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        for k, d in enumerate(slides, 1):
            piede = (f'<div class="piede"><div class="logo"><img src="data:image/png;base64,{ICONA}">PSICOLEVA</div>'
                     f'<div>{"SCORRI &nbsp;›" if k == 1 else f"{k} / {n}"}</div></div>')
            html = (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
                    f'<svg width="0" height="0" style="position:absolute">{DEFS}{GLOWF}</svg>{TIPI[d["tipo"]](d)}{piede}</body></html>')
            pg.set_content(html); pg.wait_for_timeout(500)
            ov = pg.evaluate(CHECK)
            if ov: problemi.append((k, ov))
            tmp = f"{out}/.tmp.png"; pg.screenshot(path=tmp)
            im = Image.open(tmp).convert("RGB").resize((W, H), Image.LANCZOS); os.remove(tmp)
            im.save(f"{out}/slide-{k:02d}.png"); im.save(f"{out}/slide-{k}.jpg", quality=93)
            print("ok", k, ov or "")
        b.close()
    ims = [Image.open(f"{out}/slide-{k:02d}.png").resize((540, 675)) for k in range(1, n + 1)]
    r = (n + 3) // 4; m = Image.new("RGB", (550 * min(n, 4) - 10, 685 * r - 10), "#444")
    for i, im in enumerate(ims): m.paste(im, ((i % 4) * 550, (i // 4) * 685))
    m.save(f"{out}/panoramica.png")
    if problemi:
        print("SOVRAPPOSIZIONI:", problemi); sys.exit(2)


if __name__ == "__main__":
    main()
