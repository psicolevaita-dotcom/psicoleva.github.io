#!/usr/bin/env python3
"""Pubblica un carosello Instagram tramite Buffer (API GraphQL). Usa le funzioni di carica_buffer.py.

Le immagini devono stare a un link pubblico (repo GitHub psicoleva.github.io, link raw.githubusercontent.com).
Credenziali da variabile d'ambiente: BUFFER_API_KEY

Uso:
  python3 carica_carosello.py carosello.json              # prova: mostra cosa pubblicherebbe
  python3 carica_carosello.py carosello.json --conferma   # pubblica subito
  python3 carica_carosello.py --stato <id post>           # stato del post (sent, error...) e link
  python3 carica_carosello.py carosello.json --conferma --notifica   # pubblica, attende l'esito e manda la notifica

carosello.json: {"immagini": [url, ...], "alt": [testo alternativo per immagine, ...], "testo": didascalia,
                 "quando": ISO con fuso (facoltativo), "buffer": scritto dallo script}
"""
import json, os, sys, time
import requests
from carica_buffer import gql, canali, CREA


def notifica(titolo, testo, link=None):
    """notifica push sul telefono (ntfy, variabile NTFY_TOPIC); riprova se ntfy risponde 429"""
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        return False
    h = {"Title": titolo.encode("utf-8"), "Tags": "white_check_mark"}
    if link:
        h["Click"] = link
    for t in (0, 5, 20, 60):
        time.sleep(t)
        try:
            if requests.post(f"https://ntfy.sh/{topic}", data=testo.encode("utf-8"), headers=h, timeout=20).ok:
                return True
        except requests.RequestException:
            pass
    return False


def stato(pid):
    q = "query($i: PostId!){ post(input:{id:$i}){ status externalLink error{ message } } }"
    return gql(q, {"i": pid})["post"]


def main():
    if "--stato" in sys.argv:
        print(json.dumps(stato(sys.argv[sys.argv.index("--stato") + 1]), ensure_ascii=False))
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    c = json.load(open(path, encoding="utf-8"))
    if c.get("buffer"):
        print("già pubblicato:", c["buffer"]); return
    ig = {ch["service"]: ch for ch in canali()}["instagram"]
    alt = c.get("alt") or [""] * len(c["immagini"])
    assets = [{"image": {"url": u, "metadata": {"altText": a or "Slide del carosello PsicoLeva"}}} for u, a in zip(c["immagini"], alt)]
    print(f"- instagram carosello: {len(assets)} immagini | {c['testo'].splitlines()[0]}")
    if "--conferma" not in sys.argv:
        print("\nProva: niente pubblicato. Aggiungi --conferma per pubblicare."); return
    i = {"channelId": ig["id"], "text": c["testo"], "assets": assets, "mode": "shareNow",
         "schedulingType": "automatic", "needsApproval": False,
         "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}
    if c.get("quando"):
        i["mode"], i["dueAt"] = "customScheduled", c["quando"]
    res = gql(CREA, {"i": i})["createPost"]
    if "post" not in res:
        raise RuntimeError(res.get("message", res))
    c["buffer"] = {"instagram": res["post"]["id"]}
    json.dump(c, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("fatto: post", res["post"]["id"], res["post"]["status"])
    if "--notifica" in sys.argv and not c.get("quando"):
        for _ in range(20):   # aspetta che Buffer lo mandi davvero a Instagram
            time.sleep(15)
            st = stato(res["post"]["id"])
            if st["status"] in ("sent", "error"):
                break
        print(json.dumps(st, ensure_ascii=False))
        c["esito"] = st
        json.dump(c, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        tit = c.get("titolo", c["testo"].splitlines()[0])[:80]
        if st["status"] == "sent":
            notifica("Carosello pubblicato su Instagram", tit, st.get("externalLink"))
        else:
            notifica("Carosello NON pubblicato", f"{tit}: {(st.get('error') or {}).get('message', st['status'])}")


if __name__ == "__main__":
    main()
