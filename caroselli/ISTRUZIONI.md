# Routine: due caroselli Instagram a settimana (PsicoLeva)

Richiesta dell'utente (quarate, 13/10/2026): "fai uscire un paio di caroselli a settimana in automatico, notificami solo quando li posti, cerca di riassumere le cose che sono andate più di tendenza, non per forza un solo video". Ogni esecuzione pubblica UN carosello su Instagram senza chiedere conferma (l'utente l'ha già autorizzato con questa richiesta) e manda UNA notifica sul telefono solo a pubblicazione avvenuta (o se fallisce).

## 1. Preparazione
- Tutto il materiale sta sul ramo `claude/project-thread-1868md` del repo psicolevaita-dotcom/psicoleva.github.io, cartella `caroselli/`:
  `git fetch origin claude/project-thread-1868md && git checkout -B claude/project-thread-1868md origin/claude/project-thread-1868md`
- Pacchetti: `NO_PROXY= no_proxy= python3 -m pip install -q playwright pillow requests` (Chromium è già in /opt/pw-browsers, non lanciare `playwright install`).
- Leggi `caroselli/registro.md`: non ripetere un tema o uno studio già usati negli ultimi 6 caroselli.

## 2. Scegli il tema (tendenze)
- `caroselli/dati/video-nicchia-2025-10_2026-10.csv`: 1.781 video della nicchia con `outlier_x` (views / media del canale). Raggruppa per tema (`query` e titolo) e privilegia i temi con outlier mediano alto e molti video: oggi in testa ci sono calma e stoicismo sotto pressione, farsi rispettare, psicologia dei soldi e dei ricchi, trucchi e manipolazione ("dark psychology" in chiave difensiva), linguaggio del corpo, disciplina.
- Mescola: un carosello può riassumere studi presi da più video del canale (`caroselli/dati/script/*.md`, numeri già verificati) e studi nuovi. Per uno studio nuovo usa solo ricerche reali e pubblicate, cerca la fonte sul web e riporta i numeri esattamente come nell'abstract; se non trovi la fonte, non usarlo.
- Alterna i temi da un carosello all'altro.

## 3. Scrivi i testi (regole del brand, vincolanti)
- Usa le skill psicoleva-brand, copywriting e content-strategy se disponibili.
- Italiano semplice, zero gergo, ogni esperimento spiegato partendo dalla domanda a cui voleva rispondere. Tono asciutto, intelligente, umano. Niente emoji, niente slogan generici, niente frasi da AI (niente "non è X, è Y", niente elenchi "niente X, niente Y").
- Gancio in copertina che crea curiosità senza svelare la risposta; funziona bene il senso di colpa del lettore ("Sai esattamente cosa fare. Allora perché non lo fai?").
- 6-8 slide: copertina, 3-5 slide "studio" (una per studio, con barre o numeri veri), una slide "difesa" (cosa fare in pratica), una slide "finale" che rimanda al canale YouTube (CTA "CERCA PSICOLEVA SU YOUTUBE"; se il tema coincide con un video del canale, metti la sua miniatura). Non annunciare video futuri.
- Personaggio: solo il Chibi (mai il cervello).

## 4. Genera le immagini
- Scrivi la specifica JSON (formato in testa a `caroselli/motore/genera_carosello.py`) e lancia:
  `python3 caroselli/motore/genera_carosello.py spec.json caroselli/cNN` (NN = numero successivo nel registro, due cifre).
- Se esce con codice 2 (testi sovrapposti o fuori slide) accorcia i testi e rigenera. Guarda la panoramica.png con lo strumento di lettura immagini e controlla a occhio: niente che si sovrappone, niente che esce dai riquadri, titoli leggibili.
- Salva la specifica in `caroselli/cNN/spec.json`.

## 5. Pubblica
- Fai commit di `caroselli/cNN/` (solo slide-N.jpg, spec.json, panoramica.png, carosello.json) e push sul ramo `claude/project-thread-1868md` (le immagini vengono servite da raw.githubusercontent.com).
- Crea `caroselli/cNN/carosello.json`: `immagini` = `https://raw.githubusercontent.com/psicolevaita-dotcom/psicoleva.github.io/claude/project-thread-1868md/caroselli/cNN/slide-K.jpg` per K = 1..N; `alt` = una frase per slide; `titolo` = il gancio della copertina; `testo` = didascalia (2-3 frasi + "Il video completo è sul canale YouTube PsicoLeva." + riga Fonti + esattamente 5 hashtag mirati).
- Verifica che il primo link risponda 200 (`curl -s -o /dev/null -w "%{http_code}"`), poi:
  `cd caroselli/motore && python3 carica_carosello.py ../cNN/carosello.json --conferma --notifica`
  Lo script pubblica via Buffer (BUFFER_API_KEY), aspetta l'esito e manda la notifica ntfy (NTFY_TOPIC) con il link, oppure la notifica di errore.
- Aggiungi la riga al registro (data e ora italiana), commit e push.
- Se /mnt/project-files esiste, copia anche la cartella in /mnt/project-files/canale/caroselli/NN-tema/.

## Mai
- Mai pubblicare più di un carosello per esecuzione, mai su altri social, mai cancellare post esistenti.
- Se qualcosa blocca la pubblicazione (permessi, Buffer, rete), non insistere con giri alternativi: manda la notifica di errore con il motivo e fermati.
