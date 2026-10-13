#!/usr/bin/env python3
"""Pubblica Reel/Shorts su Instagram e TikTok tramite Buffer (API GraphQL, api.buffer.com).

Buffer non riceve file: il video deve stare a un link pubblico e permanente
(sito GitHub Pages di PsicoLeva). Buffer non accetta immagini di copertina:
si sceglie un fotogramma del video (le copertine degli Shorts sono già nel video).

Credenziali da variabile d'ambiente (mai nei file): BUFFER_API_KEY

Uso:
  python3 carica_buffer.py --canali                  # elenca i canali collegati
  python3 carica_buffer.py coda.json                 # prova: mostra cosa pubblicherebbe
  python3 carica_buffer.py coda.json --conferma      # pubblica subito
  python3 carica_buffer.py coda.json --conferma --coda   # mette in coda Buffer (orari Buffer)

coda.json: lista di elementi con campi
  url            link pubblico del video .mp4
  copertina_ms   millisecondo del fotogramma-copertina (facoltativo; Instagram e TikTok)
  testo          didascalia
  servizi        ["instagram", "tiktok"] (facoltativo, default entrambi)
  tipo           "storia" per pubblicarlo come storia Instagram (TikTok non ha storie via API)
  quando         orario di pubblicazione ISO con fuso (facoltativo; senza = subito)
  buffer         scritto dallo script: {servizio: id post}
"""
import json, os, sys
import requests

API = "https://api.buffer.com/"


def gql(query, variables=None):
    r = requests.post(API, json={"query": query, "variables": variables or {}}, timeout=60,
                      headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY'].strip()}"})
    d = r.json()
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:800])
    return d["data"]


def canali():
    org = gql("{ account { organizations { id } } }")["account"]["organizations"][0]["id"]
    q = "query($o: OrganizationId!){ channels(input:{organizationId:$o}) { id name service } }"
    return gql(q, {"o": org})["channels"]


CREA = """mutation($i: CreatePostInput!){ createPost(input:$i){
  ... on PostActionSuccess { post { id status } }
  ... on MutationError { message } } }"""


def pubblica(canale, v, modo):
    video = {"url": v["url"]}
    if v.get("copertina_ms") is not None:  # fotogramma usato come copertina
        video["metadata"] = {"thumbnailOffset": int(v["copertina_ms"])}
    meta = {}
    if canale["service"] == "instagram":
        storia = v.get("tipo") == "storia"   # "tipo": "storia" -> storia Instagram invece del Reel
        meta["instagram"] = {"type": "story" if storia else "reel", "shouldShareToFeed": not storia}
    elif canale["service"] == "tiktok":
        meta["tiktok"] = {}
    i = {"channelId": canale["id"], "text": v["testo"], "assets": [{"video": video}],
         "mode": modo, "schedulingType": "automatic", "needsApproval": False,
         "metadata": meta}
    if v.get("quando"):   # orario preciso, ISO con fuso (es. 2026-10-12T18:00:00+02:00)
        i["mode"], i["dueAt"] = "customScheduled", v["quando"]
    res = gql(CREA, {"i": i})["createPost"]
    if "post" not in res:
        raise RuntimeError(res.get("message", res))
    return res["post"]["id"]


def main():
    if "--canali" in sys.argv:
        for c in canali():
            print(c["service"], c["name"], c["id"])
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    coda = json.load(open(path, encoding="utf-8"))
    per_servizio = {c["service"]: c for c in canali()}
    modo = "addToQueue" if "--coda" in sys.argv else "shareNow"
    for v in coda:
        fatti = v.setdefault("buffer", {})
        for s in v.get("servizi", ["instagram", "tiktok"]):
            if s in fatti:
                continue
            if s not in per_servizio:
                print(f"  canale {s} non collegato a Buffer, salto")
                continue
            print(f"- {s}: {v['url'].rsplit('/', 1)[-1]} | {(v['testo'].splitlines() or [v.get('tipo', '')])[0]}")
            if "--conferma" in sys.argv:
                fatti[s] = pubblica(per_servizio[s], v, modo)
                json.dump(coda, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                print(f"  fatto: post {fatti[s]}")
    if "--conferma" not in sys.argv:
        print("\nProva: niente pubblicato. Aggiungi --conferma per pubblicare.")


if __name__ == "__main__":
    main()
