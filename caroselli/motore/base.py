"""Pezzi comuni dello stile buio e luce (copiati dal motore del video 4): filtri SVG, font Bebas, ombra a terra."""
import base64, os
QUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONT = os.path.join(QUI, "BebasNeue-Regular.ttf")
FONTCSS = "@font-face{font-family:Bebas;src:url(data:font/ttf;base64," + base64.b64encode(open(FONT, "rb").read()).decode() + ")}"

DEFS = """<defs>
 <filter id="ombraP" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="8" dy="10" stdDeviation="9" flood-color="#000" flood-opacity=".55"/></filter>
 <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
 <filter id="b40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="b80" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="80"/></filter>
 <linearGradient id="muro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0e12"/><stop offset="1" stop-color="#1a1b21"/></linearGradient>
 <linearGradient id="pav" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1f25"/><stop offset="1" stop-color="#0a0b0d"/></linearGradient>
 <linearGradient id="fascio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD84A" stop-opacity=".75"/><stop offset="1" stop-color="#FFB800" stop-opacity="0"/></linearGradient>
 <linearGradient id="cono" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE27A" stop-opacity=".55"/><stop offset="1" stop-color="#FFC400" stop-opacity=".05"/></linearGradient>
 <linearGradient id="anta" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2c2d35"/><stop offset="1" stop-color="#17181d"/></linearGradient>
 <radialGradient id="alone" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFC21A" stop-opacity=".35"/><stop offset="1" stop-color="#FFC21A" stop-opacity="0"/></radialGradient>
 <radialGradient id="vign" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
 <filter id="grana"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .08 0"/></filter>
</defs>"""


def ombra_terra(x, y, w=110):
    return f'<g filter="url(#b12)" opacity=".8"><ellipse cx="{x}" cy="{y}" rx="{w}" ry="16" fill="#000"/></g>'
