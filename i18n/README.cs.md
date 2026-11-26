<p align="center">
  <img src="../assets/logo.png" width="132" alt="Logo nano-banana: žlutý banán s malou cenovkou na tmavě modrém čtverci">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>Obrázky od tvého programovacího agenta, s útratou pod kontrolou.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/tests.yml?branch=main&style=flat-square&label=tests&labelColor=0f1b2d&cacheSeconds=600"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validate" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/validate.yml?branch=main&style=flat-square&label=validate&labelColor=0f1b2d&cacheSeconds=600"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Release" src="https://img.shields.io/github/v/release/jakubcurik/nano-banana?style=flat-square&label=release&labelColor=0f1b2d&color=ffd54a&cacheSeconds=600"></a>
  <a href="../LICENSE"><img alt="Licence MIT" src="https://img.shields.io/badge/license-MIT-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Hvězdičky" src="https://img.shields.io/github/stars/jakubcurik/nano-banana?style=flat-square&labelColor=0f1b2d&color=ffd54a&cacheSeconds=600"></a>
</p>

<p align="center">
  <img alt="Plugin pro Claude Code" src="https://img.shields.io/badge/Claude_Code-plugin-ffd54a?style=flat-square&labelColor=0f1b2d">
  <a href="https://agentskills.io"><img alt="Formát Agent Skills" src="https://img.shields.io/badge/Agent_Skills-compatible-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <img alt="Python 3.11 nebo novější" src="https://img.shields.io/badge/python-3.11%2B-ffd54a?style=flat-square&labelColor=0f1b2d">
  <img alt="Gemini API" src="https://img.shields.io/badge/Gemini_API-Nano_Banana-ffd54a?style=flat-square&labelColor=0f1b2d">
</p>

<p align="center">
  <a href="#instalace">Instalace</a> &middot;
  <a href="#rychlý-start">Rychlý start</a> &middot;
  <a href="#galerie">Galerie</a> &middot;
  <a href="#jak-to-funguje">Jak to funguje</a> &middot;
  <a href="#modely-a-ceny">Modely a ceny</a> &middot;
  <a href="#časté-otázky">Časté otázky</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot;
  <a href="README.zh-CN.md">简体中文</a> &middot;
  <a href="README.es.md">Español</a> &middot;
  <a href="README.ja.md">日本語</a> &middot;
  <a href="README.pt-BR.md">Português (Brasil)</a> &middot;
  <a href="README.de.md">Deutsch</a> &middot;
  <a href="README.fr.md">Français</a> &middot;
  <a href="README.ko.md">한국어</a> &middot;
  Čeština</sub>
</p>

<p align="center">
  <img src="../assets/hero.jpg" width="880" alt="Kreslený banán v kulatých brýlích maluje krajinu na malém stojanu u stolu, vedle dlouhý papírový účet a pár zlatých mincí. Nadpis zní nano-banana.">
</p>

nano-banana je skill pro agenty, díky kterému Claude Code a další programovací agenti vytvářejí a upravují obrázky pomocí modelů Google Nano Banana. Zároveň hlídá, kolik to stojí.

Když agenta požádáš o úvodní obrázek, dostaneš ho. Když ale řekneš "zkus ještě pár variant", obyčejné volání API může spustit tucet generování ve 4K, zatímco ty se pořád díváš na první výsledek. Každý obrázek se platí a v chatu se nikde nedozvíš, kolik.

Tenhle skill před každým voláním vypíše odhad ceny a po něm skutečnou cenu. Zkontroluje, jestli zvolený model tvé volby umí, takže špatná velikost nebo nepodporovaná úroveň přemýšlení selže na tvém počítači a ne až na API. Agentovi navíc dává krátký postup: zeptat se, k čemu obrázek je, sehnat referenční fotky, když má předmět vypadat jako něco skutečného, napsat prompt anglicky a výsledek si prohlédnout, než ho označí za hotový.

<sub>Neoficiální projekt. Nijak nesouvisí s Googlem a Google ho nepodporuje. "Nano Banana" a "Gemini" jsou názvy Googlu pro jeho obrazové modely a API.</sub>

## Ukázka

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="Výstup terminálu při jednom generování: model, odhad ceny 0,0504 USD, ID interakce, spotřeba 1680 obrazových tokenů za 0,0504 USD a cesta k uloženému souboru.">
</p>

Je to skutečný běh. Obrázek ve 2K na výchozím modelu stojí asi pět amerických centů a číslo vidíš před voláním i po něm.

## Galerie

Kromě textů a snímku terminálu vzniklo pomocí tohoto skillu všechno, co v README vidíš. Prompty najdeš v [`assets/prompts`](../assets/prompts).

<p align="center">
  <img src="../assets/gallery/1-illustration.jpg" width="760" alt="Plochá ilustrace parního hrnku s kávou a croissantu na dřevěném pultu u slunného okna, vpravo volné místo pro nadpis.">
  <br>
  <sub><b>Z textu na obrázek.</b> Model 2.1, 2K, 16:9, asi 5 centů.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/2a-edit-before.jpg" width="372" alt="Obyčejný bílý keramický hrnek na světle šedém ateliérovém pozadí.">
  <img src="../assets/gallery/2b-edit-after.jpg" width="372" alt="Stejný bílý hrnek na rustikálním dřevěném stole u slunného okna, vedle misky kávových zrn.">
  <br>
  <sub><b>Úprava přes <code>--follow-up</code>.</b> Stejný hrnek, nová scéna. Model 2.1, 2K, asi 5 centů za obrázek.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/3-poster-text.jpg" width="400" alt="Minimalistický plakát kavárny s nápisem FRESH COFFEE nad plochým hrnkem kávy a řádkem Open daily from 8 to 18.">
  <br>
  <sub><b>Text v obrázku.</b> Model Pro, 2K, 4:5, asi 13 centů.</sub>
</p>

## Instalace

Claude Code, z marketplace pluginů:

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

Jakýkoli agent, který čte skilly ze `SKILL.md`, přes [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add jakubcurik/nano-banana
```

Nebo zkopíruj složku `skills/nano-banana/` ručně do složky se skilly svého agenta, například `~/.claude/skills/` pro Claude Code nebo `~/.agents/skills/` pro Codex, Gemini CLI a Cursor.

Dál potřebuješ:

- [`uv`](https://docs.astral.sh/uv/), který si sám stáhne `google-genai` i Python 3.11+. Bez něj nainstaluj Python 3.11+ a `pip install "google-genai>=3.6,<4"`.
- API klíč z [Google AI Studia](https://aistudio.google.com/apikey) se zapnutým placením. Obrazové modely nemají bezplatný tarif.

Klíč předej skriptu přes proměnnou prostředí, nebo ho jednou ulož mimo jakýkoli repozitář:

```bash
export GEMINI_API_KEY="tvuj-klic"
# nebo
mkdir -p ~/.config/nano-banana && printf '%s' "tvuj-klic" > ~/.config/nano-banana/api-key
```

## Rychlý start

Řekni agentovi: "udělej úvodní obrázek pro web mé kavárny, 16:9", "odstraň z téhle fotky auto", "spoj tyhle dvě fotky". Skill se spustí sám. Zeptá se, k čemu obrázek je, napíše prompt, řekne ti cenu, když není zanedbatelná, spustí skript a zkontroluje výsledek.

Skript můžeš volat i sám:

```bash
S=skills/nano-banana/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table" --estimate
uv run --script $S "A flat illustration of a red apple on a white table" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency CZK
```

Obrázky se ukládají do `.cache/nano-banana/`, každý vedle souboru `.txt` s promptem, volbami a ID interakce.

<details>
<summary>Všechny volby</summary>

| Volba | Význam |
|---|---|
| `-m 2.1 / 2 / pro / lite` | model, výchozí `2.1` |
| `-s 512 / 1K / 2K / 4K` | rozlišení, výchozí `1K` (512 jen u modelu `2`) |
| `-a 16:9` | poměr stran: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; u 2.1 a 2 i 1:4, 4:1, 1:8, 8:1 |
| `-i foto.jpg` | vstupní obrázek k úpravě nebo jako vzor, lze opakovat, nejvýš 14 |
| `-t minimal / medium / high` | úroveň přemýšlení, podle modelu |
| `--search` | vyhledávání přes Google včetně obrázků (ne u `lite`) |
| `--follow-up [ID]` | navázat na poslední výsledek, nebo na zadanou interakci |
| `-n 4` | počet obrázků, každý se platí zvlášť |
| `-o složka` | výstupní složka |
| `--format png / jpeg` | formát výstupního souboru |
| `--prompt-file soubor` | načte prompt ze souboru |
| `--no-store` | požádá Google, aby interakci neukládal (na ni pak nejde navázat) |
| `--batch` | za poloviční cenu, výsledek může trvat až 24 h (modely 2.1 a lite) |
| `--estimate` | vypíše odhad ceny a skončí |
| `--currency CZK` | ukáže ceny i v jiné měně (kurz z ČNB) |

</details>

## Jak to funguje

Skill nutí agenta pracovat v pevném pořadí. Nejdřív se zeptá, k čemu obrázek je. Když má ukazovat skutečný druh, produkt nebo místo, sežene dvě nebo tři referenční fotky a nechá si je od tebe potvrdit. Potom napíše prompt anglicky a odhadne cenu. Pokud odhad přesáhne asi 0,50 USD nebo se mají generovat víc než čtyři obrázky, nejdřív se zeptá tebe. Po vygenerování výsledek prohlédne a drobnosti opraví navázáním, místo aby generoval znovu od začátku.

Celý postup je v [`SKILL.md`](../skills/nano-banana/SKILL.md). Šablony promptů, šablony úprav a seznam častých chyb najdeš v [`references/prompting.md`](../skills/nano-banana/references/prompting.md).

## Modely a ceny

Stav k 26. listopadu 2026, USD za obrázek.

| Model | Nejvhodnější na | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | skoro všechno | 0,034 | 0,050 | 0,113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; Google ho označil za zastaralý, konec zatím neoznámil | 0,067 | 0,101 | 0,151 |
| `pro` (`gemini-3-pro-image`) | nejtěžší zadání, hodně textu | 0,134 | 0,134 | 0,240 |
| `lite` (`gemini-3.1-flash-lite-image`) | spousta jednoduchých obrázků, jen 1K, bez vyhledávání | 0,034 | n/a | n/a |

Ceny a údaje o modelech jsou v [`models.json`](../skills/nano-banana/scripts/models.json). To je jediný soubor, který upravíš, když Google změní [ceník](https://ai.google.dev/gemini-api/docs/pricing). `--search` se účtuje zvlášť: 5 000 dotazů s vyhledáváním měsíčně je zdarma, pak 14 USD za 1 000 vyhledávání.

## Dobré vědět

- Google ukládá interakce, aby šlo navazovat: na placených projektech 55 dní, na bezplatném tarifu 1 den. U citlivých fotek použij `--no-store`.
- Každý vygenerovaný obrázek nese neviditelný vodoznak SynthID.
- Model si vymýšlí detaily. Když má obrázek odpovídat skutečnému druhu, produktu nebo budově, dej mu přes `-i` 2-3 referenční fotky. Postup skillu na tom trvá.
- Požadavek, který vypršel, mohl být přesto zaúčtovaný, proto skript nikdy neopakuje sám od sebe.
- Pokud zveřejníš výstup vytvořený přes `--search`, Google vyžaduje zobrazit návrhy vyhledávání. Skript je ukládá vedle obrázku.

## Časté otázky

**Google má vlastní CLI `gemini-api`. K čemu je tohle?**
CLI provede volání a dělá to dobře. Tenhle skill přidává to, co se děje kolem volání. Můžeš chtít obojí.

| | Google `gemini-api` CLI a skilly | nano-banana |
|---|---|---|
| Odhad ceny předem, skutečná cena potom | ne | ano |
| Agent se před drahým během zeptá | ne | ano |
| Volby zkontrolované podle modelu | ne, odmítne je až API | ano |
| Navazující úpravy bez opisování ID | ručně | `--follow-up` |
| Prompt a volby uložené vedle každého obrázku | ne | ano |
| Průvodce prompty a šablony | ne | ano |

CLI je beta a rychle se mění, takže před volbou zkontroluj obojí.

**Funguje to i mimo Claude Code?**
Skill používá otevřený formát [Agent Skills](https://agentskills.io), takže ho mohou použít i další agenti, kteří načítají soubory `SKILL.md`. Já jsem ho vyzkoušel jen v Claude Code.

**Ceny se změnily. Co mám upravit?**
Soubor `skills/nano-banana/scripts/models.json` a tabulky v `SKILL.md` a tady.

**Proč se ptá na referenční fotky?**
Bez nich si model detaily skutečné věci domýšlí a výsledek vypadá věrohodně a přitom je špatně.

## Přispívání

Issues i pull requesty jsou vítané, hlavně když Google změní modely, ceny nebo API. Soubor `models.json`, tabulky v `SKILL.md` a README upravuj společně. Tento překlad vznikl s pomocí AI, opravy jsou vítané.

Offline testy nepotřebují API klíč ani připojení k síti:

```bash
python -m unittest discover -s tests
```

## Licence

[MIT](../LICENSE)
