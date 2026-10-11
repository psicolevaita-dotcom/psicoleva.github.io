#!/usr/bin/env python3
"""Manda una notifica push (ntfy.sh) quando un thread finisce o chiede un permesso.

Lo chiamano gli hook Stop e Notification di Claude Code (vedi ../settings.json).
Non fa nulla se la variabile NTFY_TOPIC non e' impostata nell'ambiente cloud.
Non blocca mai il thread: ogni errore viene ignorato.
"""
import json
import os
import subprocess
import sys

# Strumenti con cui un thread parla all'utente: notifichiamo solo questi.
PARLA = {"mcp__hearthbot__reply": "text", "mcp__hearthbot__ask_decision": "question"}
TACE = {"mcp__hearthbot__no_reply_needed"}


def leggi_transcript(percorso):
    titolo, ultimo = "", None
    try:
        with open(percorso, encoding="utf-8") as f:
            for riga in f:
                try:
                    e = json.loads(riga)
                except ValueError:
                    continue
                if e.get("type") == "ai-title":
                    titolo = e.get("aiTitle") or titolo
                    continue
                msg = e.get("message")
                if not isinstance(msg, dict):
                    continue
                contenuto = msg.get("content")
                # Un nuovo messaggio dell'utente apre un nuovo turno.
                if e.get("type") == "user" and isinstance(contenuto, str) and not e.get("isMeta"):
                    ultimo = None
                    continue
                if e.get("type") == "assistant" and isinstance(contenuto, list):
                    for blocco in contenuto:
                        if blocco.get("type") != "tool_use":
                            continue
                        nome = blocco.get("name")
                        if nome in PARLA:
                            ultimo = (blocco.get("input") or {}).get(PARLA[nome], "")
                        elif nome in TACE:
                            ultimo = ""
    except OSError:
        pass
    return titolo, ultimo


def main():
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        return
    try:
        dati = json.load(sys.stdin)
    except ValueError:
        dati = {}

    evento = dati.get("hook_event_name", "")
    titolo, testo = leggi_transcript(dati.get("transcript_path", ""))
    titolo = titolo or "Claude"

    if evento == "Notification":
        intestazione = "Serve un permesso: " + titolo
        corpo = dati.get("message") or "Un thread aspetta la tua conferma."
        tag, priorita = "warning", 4
    else:
        if testo == "":
            return  # turno chiuso senza dire nulla all'utente
        intestazione = "Fatto: " + titolo
        corpo = testo or "Un thread ha finito il suo turno."
        tag, priorita = "white_check_mark", 3

    corpo = " ".join(corpo.split())
    if len(corpo) > 300:
        corpo = corpo[:297] + "..."

    pacchetto = {
        "topic": topic,
        "title": intestazione[:120],
        "message": corpo,
        "tags": [tag],
        "priority": priorita,
        "click": os.environ.get("NTFY_CLICK", "https://claude.ai/code"),
    }
    subprocess.run(
        ["curl", "-s", "-m", "8", "-o", "/dev/null", "-H", "Content-Type: application/json",
         "-d", json.dumps(pacchetto), "https://ntfy.sh/"],
        check=False,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
