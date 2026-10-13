"""Chibi (protagonista di PsicoLeva dal video 4) e selezionatore, in vettoriale SVG, a pezzi animabili.
Coordinate: origine ai piedi del personaggio, s = scala. Tutte le funzioni restituiscono una stringa SVG.
Parametri animabili: espr, guarda (-1..1), blink (0..1), braccia (posa), respiro (0..1), seduto.
"""
import math

HL = "#FFD200"; HL2 = "#ECC200"; PANT = "#363a52"; CAP = "#241c1a"; PELLE = "#f6e4d0"; SCURO = "#1a181e"
GUANCE = "#f4a8a0"; BOCCA = "#46201f"; LINGUA = "#e26e6e"


def _brow(cx, by, u, espr, sx):
    if espr == "ansioso":    yi, yo = by - u * .14, by + u * .05
    elif espr == "sicuro":   yi, yo = by + u * .05, by - u * .02
    elif espr == "scioccato": yi, yo = by - u * .1, by - u * .1
    elif espr in ("serio", "aggrottato"):    yi, yo = by + u * .08, by + u * .0
    elif espr in ("felice", "sorriso"):   yi, yo = by - u * .05, by - u * .03
    else:                    yi, yo = by, by
    xi, xo = cx - sx * u * .07, cx + sx * u * .2
    my = min(yo, yi) - u * .025
    return f'<path d="M{xo:.1f},{yo:.1f} Q{(xo+xi)/2:.1f},{my:.1f} {xi:.1f},{yi:.1f}" stroke="{SCURO}" stroke-width="{u*.065:.1f}" fill="none" stroke-linecap="round"/>'


def occhi_grandi(hx, hy, u, espr, guarda, blink, pelle=PELLE):
    pelle = pelle or PELLE
    t = ""; ex = guarda * u * .16; eo = u * .34
    for sx in (-1, 1):
        cx, cy = hx + sx * eo + ex, hy
        sw, sh = (u * .23, u * .29) if espr == "scioccato" else (u * .2, u * .25)
        ap = max(.06, 1 - blink)
        t += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{sw:.1f}" ry="{sh*ap:.1f}" fill="#fff"/>'
        if ap > .35:
            ir = u * (.1 if espr == "scioccato" else .14)
            ix = cx + ex * .4
            t += f'<ellipse cx="{ix:.1f}" cy="{cy+u*.03:.1f}" rx="{ir:.1f}" ry="{ir*1.1*ap:.1f}" fill="#3c2c1e"/>'
            t += f'<ellipse cx="{ix:.1f}" cy="{cy+u*.03:.1f}" rx="{ir*.55:.1f}" ry="{ir*.6*ap:.1f}" fill="#0e0c0e"/>'
            t += f'<circle cx="{ix+ir*.4:.1f}" cy="{cy-ir*.35:.1f}" r="{ir*.32:.1f}" fill="#fff"/>'
            if espr == "sicuro":
                t += f'<path d="M{cx-sw*1.1:.1f},{cy-sh*.42:.1f} L{cx+sw*1.1:.1f},{cy-sh*.42:.1f} L{cx+sw*1.1:.1f},{cy-sh*1.2:.1f} L{cx-sw*1.1:.1f},{cy-sh*1.2:.1f}Z" fill="{pelle}"/>'
                t += f'<path d="M{cx-sw:.1f},{cy-sh*.42:.1f} H{cx+sw:.1f}" stroke="{SCURO}" stroke-width="{u*.035:.1f}" stroke-linecap="round"/>'
        else:
            t += f'<path d="M{cx-sw:.1f},{cy:.1f} Q{cx:.1f},{cy+sh*.25:.1f} {cx+sw:.1f},{cy:.1f}" stroke="{SCURO}" stroke-width="{u*.035:.1f}" fill="none" stroke-linecap="round"/>'
        t += _brow(cx, cy - u * .36, u, espr, sx)
    return t


def occhi_punto(hx, hy, u, espr, guarda, blink):
    t = ""; ex = guarda * u * .16; eo = u * .34
    for sx in (-1, 1):
        cx, cy = hx + sx * eo + ex, hy
        ap = max(.08, 1 - blink)
        t += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{u*.09:.1f}" ry="{u*.11*ap:.1f}" fill="{SCURO}"/>'
        if ap > .4:
            t += f'<circle cx="{cx+u*.03:.1f}" cy="{cy-u*.04:.1f}" r="{u*.03:.1f}" fill="#fff"/>'
        t += _brow(cx, cy - u * .26, u, espr, sx)
    return t


def bocca(mx, my, u, espr, guarda=0):
    mx += guarda * u * .12; w = u * .05
    if espr == "aggrottato":
        return f'<path d="M{mx-u*.14:.1f},{my+u*.03:.1f} Q{mx:.1f},{my-u*.05:.1f} {mx+u*.14:.1f},{my+u*.03:.1f}" stroke="{SCURO}" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>'
    if espr == "sorriso":
        return f'<path d="M{mx-u*.15:.1f},{my-u*.01:.1f} Q{mx:.1f},{my+u*.1:.1f} {mx+u*.15:.1f},{my-u*.01:.1f}" stroke="{SCURO}" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>'
    if espr in ("normale", "serio"):
        return f'<path d="M{mx-u*.12:.1f},{my:.1f} L{mx+u*.12:.1f},{my:.1f}" stroke="{SCURO}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
    if espr == "felice":
        return f'<path d="M{mx-u*.17:.1f},{my-u*.02:.1f} Q{mx:.1f},{my+u*.2:.1f} {mx+u*.17:.1f},{my-u*.02:.1f} Z" fill="{BOCCA}" stroke="{SCURO}" stroke-width="{w*.6:.1f}" stroke-linejoin="round"/><ellipse cx="{mx:.1f}" cy="{my+u*.09:.1f}" rx="{u*.07:.1f}" ry="{u*.035:.1f}" fill="{LINGUA}"/>'
    if espr == "ansioso":
        x0, x1, y0, y1 = mx - u * .22, mx + u * .22, my - u * .07, my + u * .07
        g = "".join(f'<path d="M{mx+k*u*.08:.1f},{y0:.1f} V{y1:.1f}" stroke="#aaa" stroke-width="{u*.016:.1f}"/>' for k in range(-2, 3))
        return f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" rx="{u*.05:.1f}" fill="#fff" stroke="{SCURO}" stroke-width="{u*.035:.1f}"/><path d="M{x0:.1f},{my:.1f} H{x1:.1f}" stroke="#aaa" stroke-width="{u*.022:.1f}"/>' + g
    if espr == "sicuro":
        return f'<path d="M{mx-u*.18:.1f},{my+u*.02:.1f} Q{mx+u*.02:.1f},{my+u*.08:.1f} {mx+u*.2:.1f},{my-u*.06:.1f}" stroke="{SCURO}" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>'
    if espr == "scioccato":
        return f'<ellipse cx="{mx:.1f}" cy="{my+u*.05:.1f}" rx="{u*.13:.1f}" ry="{u*.17:.1f}" fill="{BOCCA}"/><ellipse cx="{mx:.1f}" cy="{my+u*.14:.1f}" rx="{u*.08:.1f}" ry="{u*.06:.1f}" fill="{LINGUA}"/>'
    return ""


def braccio(spalla, gomito, mano, col, w, pelle=PELLE, r=13):
    (a, b), (c, d), (e, f) = spalla, gomito, mano
    return (f'<path d="M{a:.1f},{b:.1f} L{c:.1f},{d:.1f} L{e:.1f},{f:.1f}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{e:.1f}" cy="{f:.1f}" r="{r}" fill="{pelle}"/>')


POSE = {  # (gomito, mano) per braccio sinistro (x<0) e destro (x>0), unità del personaggio
    "giu":     (((-62, -150), (-54, -112)), ((62, -150), (54, -112))),
    "foglio":  (((-66, -150), (-70, -112)), ((62, -150), (54, -112))),
    "trofeo":  (((-62, -150), (-54, -112)), ((112, -246), (150, -330))),
    "leva":    (((-62, -150), (-54, -112)), ((96, -190), (138, -196))),
    "fianchi": (((-74, -160), (-44, -128)), ((74, -160), (44, -128))),
    "indica":  (((-62, -150), (-54, -112)), ((100, -200), (160, -214))),
    "alza":    (((-62, -150), (-54, -112)), ((76, -262), (86, -340))),
    "fronte":  (((-62, -150), (-54, -112)), ((96, -262), (52, -372))),
    "petto":   (((-70, -160), (-26, -150)), ((70, -160), (26, -150))),
    "lente":   (((-62, -150), (-54, -112)), ((96, -220), (128, -272))),
    "dueman":  (((-80, -170), (-110, -226)), ((80, -170), (110, -226))),
    "rigido":  (((-52, -150), (-50, -100)), ((52, -150), (50, -100))),
}


def foglio(x, y, s, ang=-8):
    righe = "".join(f'<path d="M{-22},{-30+i*12} h{44 - (16 if i == 4 else 0)}" stroke="#7d8594" stroke-width="3" stroke-linecap="round"/>' for i in range(5))
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang}) scale({s})"><rect x="-32" y="-44" width="64" height="86" rx="4" fill="#d9d6cb"/>'
            f'<rect x="-29" y="-47" width="64" height="86" rx="4" fill="#f4f2ea"/>{righe}</g>')


def trofeo(x, y, s):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})">'
            f'<path d="M-34,-78 H34 Q34,-20 0,-8 Q-34,-20 -34,-78Z" fill="{HL}"/>'
            f'<path d="M-34,-70 Q-58,-66 -52,-42 Q-46,-30 -26,-30" stroke="{HL}" stroke-width="8" fill="none"/>'
            f'<path d="M34,-70 Q58,-66 52,-42 Q46,-30 26,-30" stroke="{HL}" stroke-width="8" fill="none"/>'
            f'<rect x="-7" y="-10" width="14" height="22" fill="#d8ac00"/><rect x="-26" y="10" width="52" height="14" rx="3" fill="#d8ac00"/>'
            f'<ellipse cx="-14" cy="-60" rx="7" ry="13" fill="#fff6c0" opacity=".7"/></g>')


def ciocca(hx, hy, r):
    ts = [i / 12 for i in range(13)]
    cur = [(hx + r * (.34 * t ** 1.3), hy - r * (1.0 - .58 * t)) for t in ts]
    L = [(x - r * .1 * (1 - t), y) for (x, y), t in zip(cur, ts)]
    R = [(x + r * .1 * (1 - t), y) for (x, y), t in zip(cur, ts)]
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in L + R[::-1]) + f'" fill="{HL}"/>'


def chibi(x, y, s=1.45, espr="normale", guarda=0.0, blink=0.0, braccia="giu", respiro=0.0, seduto=False, oggetto=None, tilt=0.0,
          maglia=HL, maniche=HL2, capelli=CAP, ciocca_gialla=True, lunghi=False, camice=False, occhiali=False, pelle=PELLE, inclina=0.0):
    """oggetto: None | 'foglio' | 'trofeo' | 'taccuino' | 'lente' | 'videocamera'. Restituisce (svg, (hx, hy, r)) in coordinate di scena.
    Con maglia/capelli/ciocca_gialla/lunghi/camice/occhiali si fanno gli altri personaggi (scienziati, persone)."""
    global PELLE_C
    PELLE_C = pelle
    g = ""
    dy = 0
    if seduto:  # visto di fronte: ginocchia verso di noi all'altezza del sedile, stinchi giu'
        g += f'<path d="M-16,-80 L-20,-10 M16,-80 L22,-10" stroke="{PANT}" stroke-width="24" stroke-linecap="round"/>'
        g += f'<rect x="-44" y="-112" width="88" height="40" rx="20" fill="#2e3248"/>'
    else:
        g += f'<path d="M-14,-100 L-18,-10 M14,-100 L20,-10" stroke="{PANT}" stroke-width="24" stroke-linecap="round"/>'
    g += '<ellipse cx="-24" cy="-10" rx="26" ry="12" fill="#f0f0f4"/><ellipse cx="28" cy="-10" rx="26" ry="12" fill="#f0f0f4"/>'
    sy = 1 + .02 * respiro
    corpo = f'<rect x="-46" y="-210" width="92" height="118" rx="30" fill="{maglia}"/>'
    if camice:
        maniche = "#e9e9ee"
        corpo = (f'<rect x="-50" y="-212" width="100" height="150" rx="26" fill="#f1f1f4"/><path d="M-14,-212 L0,-160 L14,-212Z" fill="{maglia}"/>'
                 f'<path d="M0,-160 V-70" stroke="#c9c9d0" stroke-width="3"/><rect x="18" y="-150" width="22" height="16" rx="3" fill="#d9d9e0"/>')
    if braccia == "incrociate":
        corpo += f'<rect x="-62" y="-172" width="124" height="40" rx="20" fill="{maniche}"/><circle cx="-48" cy="-162" r="12" fill="{pelle}"/><circle cx="50" cy="-144" r="12" fill="{pelle}"/>'
        gl = ml = gr = mr = None
    else:
        (gl, ml), (gr, mr) = POSE[braccia]
        corpo += braccio((-42, -196), gl, ml, maniche, 22, pelle)
    if oggetto == "trofeo":
        corpo += trofeo(mr[0] + 4, mr[1] - 8, 1.25)
    if braccia != "incrociate":
        corpo += braccio((42, -196), gr, mr, maniche, 22, pelle)
    if oggetto == "foglio":
        corpo += foglio(ml[0] - 4, ml[1] + 40, 1.0)
        corpo += f'<circle cx="{ml[0]}" cy="{ml[1]}" r="13" fill="{pelle}"/>'
    if oggetto == "taccuino":
        corpo += (f'<g transform="translate({mr[0]-30},{mr[1]-34})"><rect x="-34" y="-46" width="68" height="88" rx="5" fill="#f4f2ea"/>'
                  f'<path d="M-34,-46 H34" stroke="#c44" stroke-width="5"/>' + "".join(f'<path d="M{-22+i*10},-20 v26" stroke="#555" stroke-width="3"/>' for i in range(5)) + '</g>')
        corpo += f'<circle cx="{mr[0]}" cy="{mr[1]}" r="13" fill="{pelle}"/>'
    if oggetto == "lente":
        corpo += f'<g transform="translate({mr[0]},{mr[1]})"><path d="M0,0 L22,-26" stroke="#5a4630" stroke-width="10" stroke-linecap="round"/><circle cx="40" cy="-48" r="30" fill="#bfe3ff" fill-opacity=".35" stroke="#2b2c33" stroke-width="8"/></g><circle cx="{mr[0]}" cy="{mr[1]}" r="13" fill="{pelle}"/>'
    if oggetto == "videocamera":
        corpo += (f'<g transform="translate(0,-232)"><rect x="-62" y="-38" width="104" height="70" rx="10" fill="#34353d"/><circle cx="-22" cy="-56" r="22" fill="#34353d"/><circle cx="20" cy="-56" r="22" fill="#34353d"/>'
                  f'<path d="M42,-14 L84,-34 V20 L42,0Z" fill="#26272e"/><circle cx="-10" cy="-4" r="14" fill="#555"/></g>')
        corpo += f'<circle cx="{ml[0]}" cy="{ml[1]}" r="13" fill="{pelle}"/><circle cx="{mr[0]}" cy="{mr[1]}" r="13" fill="{pelle}"/>'
    hx, hy, r = 0, -310, 96
    testa = ""
    if lunghi:
        testa += f'<rect x="{hx-r*1.06:.1f}" y="{hy-r*.4:.1f}" width="{r*2.12:.1f}" height="{r*1.5:.1f}" rx="{r*.5:.1f}" fill="{capelli}"/>'
    testa += f'<ellipse cx="{hx}" cy="{hy-r*.02:.1f}" rx="{r*1.06:.1f}" ry="{r*1.04:.1f}" fill="{capelli}"/>'
    testa += f'<ellipse cx="{hx}" cy="{hy+r*.08:.1f}" rx="{r*.9:.1f}" ry="{r*.86:.1f}" fill="{pelle}"/>'
    testa += f'<path d="M{hx-r:.1f},{hy-r*.5:.1f} A{r:.1f},{r*.56:.1f} 0 0 1 {hx+r:.1f},{hy-r*.5:.1f} Z" fill="{capelli}"/>'
    for xx in (-.72, -.38, -.02, .34, .7):
        testa += f'<ellipse cx="{hx+xx*r:.1f}" cy="{hy-r*.68+abs(xx)*r*.14:.1f}" rx="{r*.22:.1f}" ry="{r*.18:.1f}" fill="{capelli}"/>'
    if ciocca_gialla:
        testa += ciocca(hx, hy, r)
    testa += f'<ellipse cx="{hx-r*.55:.1f}" cy="{hy+r*.32:.1f}" rx="{r*.12:.1f}" ry="{r*.07:.1f}" fill="{GUANCE}"/><ellipse cx="{hx+r*.55:.1f}" cy="{hy+r*.32:.1f}" rx="{r*.12:.1f}" ry="{r*.07:.1f}" fill="{GUANCE}"/>'
    testa += occhi_grandi(hx, hy + r * .12, r * .95, espr, guarda, blink, pelle)
    if occhiali:
        for sx in (-1, 1):
            testa += f'<circle cx="{hx+sx*r*.32+guarda*r*.15:.1f}" cy="{hy+r*.12:.1f}" r="{r*.27:.1f}" fill="none" stroke="#15151a" stroke-width="{r*.045:.1f}"/>'
    testa += bocca(hx, hy + r * .55, r * .85, espr, guarda)
    alza = -4 * respiro
    svg = (f'<g transform="translate({x:.1f},{y:.1f}) scale({s}) rotate({inclina:.2f} 0 -10)" filter="url(#ombraP)">' + g
           + f'<g transform="translate(0,{dy}) translate(0,-92) scale(1,{sy:.4f}) translate(0,92)">{corpo}</g>'
           + f'<g transform="translate(0,{dy+alza:.1f}) rotate({tilt:.2f} 0 -214)">{testa}</g></g>')
    return svg, (x, y + (hy + dy) * s, r * s)


def selezionatore(x, y, s=1.5, espr="serio", guarda=0.0, blink=0.0, seduto=True):
    """adulto in giacca scura, occhiali, braccia incrociate: chi giudica."""
    GIA = "#2c303c"; CAMI = "#e8e8ec"; CAPG = "#4a4a52"; PEL = "#eed8c2"
    g = ""
    dy = 0
    if seduto:
        g += f'<path d="M-18,-80 L-20,-10 M18,-80 L22,-10" stroke="#22252e" stroke-width="26" stroke-linecap="round"/><rect x="-50" y="-112" width="100" height="40" rx="20" fill="#2a2d38"/>'
        g += '<ellipse cx="-26" cy="-10" rx="28" ry="12" fill="#111216"/><ellipse cx="30" cy="-10" rx="28" ry="12" fill="#111216"/>'
    else:
        g += f'<path d="M-16,-100 L-18,-10 M16,-100 L20,-10" stroke="#22252e" stroke-width="26" stroke-linecap="round"/>'
    g += f'<g transform="translate(0,{dy})">'
    g += f'<rect x="-54" y="-220" width="108" height="130" rx="26" fill="{GIA}"/>'
    g += f'<path d="M-18,-220 L0,-178 L18,-220Z" fill="{CAMI}"/><path d="M-5,-196 L5,-196 L8,-150 L0,-140 L-8,-150Z" fill="#7a2d33"/>'
    # braccia incrociate: una fascia di giacca sul petto con le mani ai lati
    g += f'<rect x="-66" y="-170" width="132" height="40" rx="20" fill="#353a48"/><path d="M-60,-150 H60" stroke="#262a35" stroke-width="3"/>'
    g += f'<circle cx="-50" cy="-160" r="12" fill="{PEL}"/><circle cx="52" cy="-142" r="12" fill="{PEL}"/>'
    hx, hy, r = 0, -315, 90
    g += f'<ellipse cx="{hx}" cy="{hy+4}" rx="{r*.92:.1f}" ry="{r*.9:.1f}" fill="{PEL}"/>'
    g += f'<path d="M{hx-r*.92:.1f},{hy-r*.05:.1f} Q{hx-r*.95:.1f},{hy-r*1.05:.1f} {hx:.1f},{hy-r*.98:.1f} Q{hx+r*.95:.1f},{hy-r*1.05:.1f} {hx+r*.92:.1f},{hy-r*.05:.1f} Q{hx+r*.6:.1f},{hy-r*.6:.1f} {hx:.1f},{hy-r*.62:.1f} Q{hx-r*.6:.1f},{hy-r*.6:.1f} {hx-r*.92:.1f},{hy-r*.05:.1f}Z" fill="{CAPG}"/>'
    u = r
    g += occhi_punto(hx, hy + r * .1, u, espr, guarda, blink)
    for sx in (-1, 1):
        g += f'<circle cx="{hx+sx*u*.34+guarda*u*.16:.1f}" cy="{hy+r*.1:.1f}" r="{u*.2:.1f}" fill="none" stroke="#15151a" stroke-width="{u*.04:.1f}"/>'
    g += f'<path d="M{hx-u*.14+guarda*u*.16:.1f},{hy+r*.08:.1f} H{hx+u*.14+guarda*u*.16:.1f}" stroke="#15151a" stroke-width="{u*.04:.1f}"/>'
    g += bocca(hx, hy + r * .55, r * .85, espr, guarda)
    g += "</g>"
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" filter="url(#ombraP)">{g}</g>', (x, y + (hy + dy) * s, r * s)
