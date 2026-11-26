<p align="center">
  <img src="../assets/logo.png" width="132" alt="nano-banana-Logo: eine gelbe Banane mit einem kleinen Preisschild auf einem marineblauen Quadrat">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>Bilder von deinem Coding-Agenten, mit Kontrolle über die Kosten.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/tests.yml?branch=main&style=flat-square&label=tests&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validierung" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/validate.yml?branch=main&style=flat-square&label=validate&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Release" src="https://img.shields.io/github/v/release/jakubcurik/nano-banana?style=flat-square&label=release&labelColor=0f1b2d&color=ffd54a"></a>
  <a href="../LICENSE"><img alt="Lizenz: MIT" src="https://img.shields.io/badge/license-MIT-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Sterne" src="https://img.shields.io/github/stars/jakubcurik/nano-banana?style=flat-square&labelColor=0f1b2d&color=ffd54a"></a>
</p>

<p align="center">
  <img alt="Plugin für Claude Code" src="https://img.shields.io/badge/Claude_Code-plugin-ffd54a?style=flat-square&labelColor=0f1b2d">
  <a href="https://agentskills.io"><img alt="Agent-Skills-Format" src="https://img.shields.io/badge/Agent_Skills-compatible-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <img alt="Python 3.11 oder neuer" src="https://img.shields.io/badge/python-3.11%2B-ffd54a?style=flat-square&labelColor=0f1b2d">
  <img alt="Gemini API" src="https://img.shields.io/badge/Gemini_API-Nano_Banana-ffd54a?style=flat-square&labelColor=0f1b2d">
</p>

<p align="center">
  <a href="#install">Installation</a> &middot;
  <a href="#quick-start">Schnellstart</a> &middot;
  <a href="#gallery">Galerie</a> &middot;
  <a href="#how-it-works">So funktioniert es</a> &middot;
  <a href="#models-and-prices">Modelle und Preise</a> &middot;
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot;
  <a href="README.zh-CN.md">简体中文</a> &middot;
  <a href="README.es.md">Español</a> &middot;
  <a href="README.ja.md">日本語</a> &middot;
  <a href="README.pt-BR.md">Português (Brasil)</a> &middot;
  Deutsch &middot;
  <a href="README.fr.md">Français</a> &middot;
  <a href="README.ko.md">한국어</a> &middot;
  <a href="README.cs.md">Čeština</a></sub>
</p>

<p align="center">
  <img src="../assets/hero.jpg" width="880" alt="Eine Cartoon-Banane mit runder Brille malt an einem Schreibtisch eine Landschaft auf eine kleine Staffelei, daneben liegen ein langer Papierbeleg und ein paar Goldmünzen. Der Titel lautet nano-banana.">
</p>

nano-banana ist ein Agent Skill, mit dem Claude Code und andere Coding-Agenten Bilder mit Googles Modellen Nano Banana erstellen und bearbeiten. Er behält außerdem im Blick, was das kostet.

Wenn du einen Agenten um ein Hero-Bild bittest, bekommst du eins. Sagst du aber „probier noch ein paar Varianten“, kann ein einfacher API-Aufruf ein Dutzend 4K-Generierungen starten, während du noch das erste Ergebnis ansiehst. Jedes Bild wird berechnet, und im Chat steht nirgends, wie viel.

Dieser Skill gibt vor jedem Aufruf den geschätzten Preis aus und danach die tatsächlichen Kosten. Er prüft deine Optionen gegen das, was das gewählte Modell unterstützt, sodass eine falsche Größe oder eine nicht unterstützte Thinking-Stufe auf deinem Rechner scheitert und nicht erst bei der API. Dazu gibt er dem Agenten eine kurze Routine: fragen, wofür das Bild gedacht ist, Referenzfotos besorgen, wenn das Motiv wie etwas Reales aussehen muss, den Prompt auf Englisch schreiben und sich das Ergebnis ansehen, bevor er es für fertig erklärt.

<sub>Inoffiziell. Nicht mit Google verbunden und nicht von Google unterstützt. „Nano Banana“ und „Gemini“ sind Googles Namen für seine Bildmodelle und die API.</sub>

## So sieht es aus

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="Terminal-Ausgabe einer Generierung: das Modell, geschätzte Kosten von 0,0504 USD, die Interaktions-ID, der Verbrauch von 1680 Bild-Tokens für 0,0504 USD und der Pfad der gespeicherten Datei.">
</p>

Das ist ein echter Lauf. Ein 2K-Bild mit dem Standardmodell kostet etwa fünf US-Cent, und du siehst die Zahl vor dem Aufruf und noch einmal danach.

<a id="gallery"></a>

## Galerie

Bis auf den Text und den Terminal-Screenshot ist jedes Bild in diesem README mit dem Skill entstanden. Die Prompts liegen in [`assets/prompts`](../assets/prompts).

<p align="center">
  <img src="../assets/gallery/1-illustration.jpg" width="760" alt="Eine flache Illustration einer dampfenden Kaffeetasse und eines Croissants auf einer Holztheke an einem sonnigen Fenster, rechts freier Platz für eine Überschrift.">
  <br>
  <sub><b>Text zu Bild.</b> Modell 2.1, 2K, 16:9, etwa 5 Cent.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/2a-edit-before.jpg" width="372" alt="Eine schlichte weiße Keramiktasse auf hellgrauem Studiohintergrund.">
  <img src="../assets/gallery/2b-edit-after.jpg" width="372" alt="Dieselbe weiße Tasse auf einem rustikalen Holztisch an einem sonnigen Fenster, neben einer kleinen Schale mit Kaffeebohnen.">
  <br>
  <sub><b>Bearbeiten mit <code>--follow-up</code>.</b> Dieselbe Tasse, neue Szene. Modell 2.1, 2K, etwa 5 Cent pro Bild.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/3-poster-text.jpg" width="400" alt="Ein minimalistisches Café-Plakat mit der Aufschrift FRESH COFFEE über einer flachen Kaffeetasse und der Zeile Open daily from 8 to 18.">
  <br>
  <sub><b>Text im Bild.</b> Modell Pro, 2K, 4:5, etwa 13 Cent.</sub>
</p>

<a id="install"></a>

## Installation

Claude Code, über den Plugin-Marketplace:

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

Jeder Agent, der `SKILL.md`-Skills liest, über [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add jakubcurik/nano-banana
```

Oder kopiere `skills/nano-banana/` von Hand in den Skills-Ordner deines Agenten, zum Beispiel `~/.claude/skills/` für Claude Code oder `~/.agents/skills/` für Codex, Gemini CLI und Cursor.

Außerdem brauchst du:

- [`uv`](https://docs.astral.sh/uv/), das `google-genai` und Python 3.11+ selbst holt. Ohne uv installierst du Python 3.11+ und `pip install "google-genai>=3.6,<4"`.
- Einen Gemini-API-Key aus [Google AI Studio](https://aistudio.google.com/apikey) mit aktivierter Abrechnung. Die Bildmodelle haben keinen kostenlosen Tarif.

Gib dem Skript den Key über die Umgebung, oder speichere ihn einmal außerhalb jedes Repositorys:

```bash
export GEMINI_API_KEY="your-key"
# or
mkdir -p ~/.config/nano-banana && printf '%s' "your-key" > ~/.config/nano-banana/api-key
```

<a id="quick-start"></a>

## Schnellstart

Sag deinem Agenten: „Mach ein Hero-Bild für die Website meines Cafés, 16:9“, „Entferne das Auto aus diesem Foto“, „Kombiniere diese beiden Fotos“. Der Skill springt von selbst an. Er fragt, wofür das Bild gedacht ist, schreibt den Prompt, nennt dir den Preis, wenn er nicht trivial ist, führt das Skript aus und prüft das Ergebnis.

Du kannst das Skript auch selbst aufrufen:

```bash
S=skills/nano-banana/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table" --estimate
uv run --script $S "A flat illustration of a red apple on a white table" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency EUR
```

Die Bilder landen in `.cache/nano-banana/`, jedes neben einer `.txt`-Datei mit dem Prompt, den Optionen und der Interaktions-ID.

<details>
<summary>Alle Optionen</summary>

| Option | Bedeutung |
|---|---|
| `-m 2.1 / 2 / pro / lite` | Modell, Standard `2.1` |
| `-s 512 / 1K / 2K / 4K` | Auflösung, Standard `1K` (512 nur beim Modell `2`) |
| `-a 16:9` | Seitenverhältnis: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; bei 2.1 und 2 auch 1:4, 4:1, 1:8, 8:1 |
| `-i photo.jpg` | Eingabebild zum Bearbeiten oder als Referenz, wiederholbar, maximal 14 |
| `-t minimal / medium / high` | Thinking-Stufe, hängt vom Modell ab |
| `--search` | Google-Search-Grounding, auch mit Bildersuche (nicht bei `lite`) |
| `--follow-up [ID]` | an das letzte Ergebnis oder an eine angegebene Interaktion anknüpfen |
| `-n 4` | Anzahl der Bilder, jedes wird einzeln berechnet |
| `-o Ordner` | Ausgabeordner |
| `--format png / jpeg` | Format der Ausgabedatei |
| `--prompt-file Datei` | liest den Prompt aus einer Datei |
| `--no-store` | Google bitten, die Interaktion nicht zu speichern (daran lässt sich dann nicht anknüpfen) |
| `--batch` | halber Preis, dauert bis zu 24 h (Modelle 2.1 und lite) |
| `--estimate` | gibt die Preisschätzung aus und stoppt |
| `--currency CZK` | zeigt Preise zusätzlich in dieser Währung (Kurs der Tschechischen Nationalbank) |

</details>

<a id="how-it-works"></a>

## So funktioniert es

Der Skill lässt den Agenten in einer festen Reihenfolge arbeiten. Zuerst fragt er, wofür das Bild gedacht ist. Soll es eine echte Art, ein Produkt oder einen Ort zeigen, besorgt er zwei oder drei Referenzfotos und lässt sie dich bestätigen. Danach schreibt er den Prompt auf Englisch und schätzt den Preis; bei mehr als etwa 0,50 USD oder mehr als vier Bildern fragt er vorher nach. Nach der Generierung sieht er sich das Ergebnis an und korrigiert Kleinigkeiten per Follow-up, statt von vorn anzufangen.

Der vollständige Ablauf steht in [`SKILL.md`](../skills/nano-banana/SKILL.md). Prompt-Vorlagen, Bearbeitungsvorlagen und eine Liste häufiger Fehler findest du in [`references/prompting.md`](../skills/nano-banana/references/prompting.md).

<a id="models-and-prices"></a>

## Modelle und Preise

Stand 26. November 2026, USD pro Bild.

| Modell | Am besten für | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | fast alles | 0,034 | 0,050 | 0,113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; von Google als veraltet markiert, noch kein Abschaltdatum | 0,067 | 0,101 | 0,151 |
| `pro` (`gemini-3-pro-image`) | die schwierigsten Prompts, viel Text | 0,134 | 0,134 | 0,240 |
| `lite` (`gemini-3.1-flash-lite-image`) | viele einfache Bilder, nur 1K, keine Suche | 0,034 | n/a | n/a |

Preise und Modelldaten stehen in [`models.json`](../skills/nano-banana/scripts/models.json). Das ist die einzige Datei, die du ändern musst, wenn Google seine [Preisliste](https://ai.google.dev/gemini-api/docs/pricing) ändert. `--search` wird zusätzlich berechnet: 5.000 Prompts mit Grounding pro Monat sind kostenlos, danach kosten 1.000 Suchanfragen 14 USD.

## Gut zu wissen

- Google speichert Interaktionen, damit Folgeaufrufe funktionieren: 55 Tage bei bezahlten Projekten, 1 Tag im kostenlosen Tarif. Nutze `--no-store` für sensible Fotos.
- Jedes generierte Bild trägt ein unsichtbares SynthID-Wasserzeichen.
- Das Modell erfindet Details. Wenn ein Bild zu einer echten Art, einem echten Produkt oder Gebäude passen muss, gib ihm per `-i` 2-3 Referenzfotos. Der Ablauf des Skills besteht darauf.
- Eine Anfrage mit Timeout kann trotzdem abgerechnet worden sein, deshalb wiederholt das Skript nie von selbst.
- Wenn du Ergebnisse veröffentlichst, die mit `--search` entstanden sind, verlangt Google, dass du seine Suchvorschläge anzeigst. Das Skript speichert sie neben dem Bild.

<a id="faq"></a>

## FAQ

**Google hat eine eigene `gemini-api`-CLI. Wozu dann dieser Skill?**
Die CLI führt den Aufruf aus, und das macht sie gut. Dieser Skill ergänzt, was um den Aufruf herum passiert. Vielleicht willst du beides.

| | Google `gemini-api`-CLI und Skills | nano-banana |
|---|---|---|
| Preisschätzung vorher, echte Kosten nachher | nein | ja |
| Der Agent fragt vor teuren Läufen nach | nein | ja |
| Optionen werden gegen das Modell geprüft | nein, die API lehnt sie ab | ja |
| Folgebearbeitungen ohne ID-Abtippen | manuell | `--follow-up` |
| Prompt und Optionen neben jedem Bild gespeichert | nein | ja |
| Prompting-Leitfaden und Vorlagen | nein | ja |

Die CLI ist eine Beta und entwickelt sich schnell, prüfe also beide, bevor du dich entscheidest.

**Funktioniert das auch außerhalb von Claude Code?**
Der Skill folgt dem offenen Format [Agent Skills](https://agentskills.io), andere Agenten, die `SKILL.md`-Dateien laden, können ihn also nutzen. Ich habe ihn nur in Claude Code getestet.

**Die Preise haben sich geändert. Was muss ich anpassen?**
`skills/nano-banana/scripts/models.json` sowie die Tabellen in `SKILL.md` und hier.

**Warum fragt er nach Referenzfotos?**
Ohne sie denkt sich das Modell die Details einer echten Sache aus, und das Ergebnis sieht plausibel aus und ist trotzdem falsch.

## Mitwirken

Issues und Pull Requests sind willkommen, besonders wenn Google Modelle, Preise oder die API ändert. Aktualisiere `models.json` und die Tabellen in `SKILL.md` und in diesem README gemeinsam.

Diese Übersetzung ist mit Hilfe von KI entstanden, Korrekturen sind willkommen.

Die Offline-Tests brauchen weder API-Key noch Netzwerk:

```bash
python -m unittest discover -s tests
```

## Lizenz

[MIT](../LICENSE)

## Star-Verlauf

<a href="https://www.star-history.com/jakubcurik/nano-banana#history">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
    <img alt="Diagramm des Star-Verlaufs" src="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
  </picture>
</a>
