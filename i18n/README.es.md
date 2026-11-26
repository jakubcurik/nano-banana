<p align="center">
  <img src="../assets/logo.png" width="132" alt="Logotipo de nano-banana: un plátano amarillo con una pequeña etiqueta de precio sobre un cuadrado azul marino">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>Imágenes desde tu agente de programación, con el gasto bajo control.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/tests.yml?branch=main&style=flat-square&label=tests&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validación" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/validate.yml?branch=main&style=flat-square&label=validate&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Versión" src="https://img.shields.io/github/v/release/jakubcurik/nano-banana?style=flat-square&label=release&labelColor=0f1b2d&color=ffd54a"></a>
  <a href="../LICENSE"><img alt="Licencia: MIT" src="https://img.shields.io/badge/license-MIT-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Estrellas" src="https://img.shields.io/github/stars/jakubcurik/nano-banana?style=flat-square&labelColor=0f1b2d&color=ffd54a"></a>
</p>

<p align="center">
  <img alt="Plugin para Claude Code" src="https://img.shields.io/badge/Claude_Code-plugin-ffd54a?style=flat-square&labelColor=0f1b2d">
  <a href="https://agentskills.io"><img alt="Compatible con el formato Agent Skills" src="https://img.shields.io/badge/Agent_Skills-compatible-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <img alt="Python 3.11 o superior" src="https://img.shields.io/badge/python-3.11%2B-ffd54a?style=flat-square&labelColor=0f1b2d">
  <img alt="Gemini API" src="https://img.shields.io/badge/Gemini_API-Nano_Banana-ffd54a?style=flat-square&labelColor=0f1b2d">
</p>

<p align="center">
  <a href="#install">Instalación</a> &middot;
  <a href="#quick-start">Inicio rápido</a> &middot;
  <a href="#gallery">Galería</a> &middot;
  <a href="#how-it-works">Cómo funciona</a> &middot;
  <a href="#models-and-prices">Modelos y precios</a> &middot;
  <a href="#faq">Preguntas frecuentes</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot;
  <a href="README.zh-CN.md">简体中文</a> &middot;
  Español &middot;
  <a href="README.ja.md">日本語</a> &middot;
  <a href="README.pt-BR.md">Português (Brasil)</a> &middot;
  <a href="README.de.md">Deutsch</a> &middot;
  <a href="README.fr.md">Français</a> &middot;
  <a href="README.ko.md">한국어</a> &middot;
  <a href="README.cs.md">Čeština</a></sub>
</p>

<p align="center">
  <img src="../assets/hero.jpg" width="880" alt="Un plátano de dibujos animados con gafas redondas pinta un paisaje en un pequeño caballete sobre un escritorio, junto a un recibo de papel muy largo y unas cuantas monedas de oro. El título dice nano-banana.">
</p>

nano-banana es un skill para agentes que permite a Claude Code y a otros agentes de programación crear y editar imágenes con los modelos Nano Banana de Google. Además, lleva la cuenta de lo que cuesta.

Si le pides a un agente una imagen de cabecera, te la da. Pero si le dices "prueba unas cuantas variantes más", una llamada directa a la API puede lanzar una docena de generaciones en 4K mientras tú sigues mirando la primera. Cada imagen se cobra, y en el chat nada te dice cuánto.

Este skill muestra el precio estimado antes de cada llamada y el coste real después. Comprueba tus opciones contra lo que admite el modelo elegido, así que un tamaño incorrecto o un nivel de razonamiento no compatible falla en tu máquina y no en la API. Para todo lo demás, le da al agente una rutina corta: preguntar para qué es la imagen, conseguir fotos de referencia cuando el sujeto tiene que parecerse a algo real, escribir el prompt en inglés y mirar el resultado antes de darlo por terminado.

<sub>No oficial. No está afiliado a Google ni cuenta con su respaldo. "Nano Banana" y "Gemini" son los nombres que Google da a sus modelos de imagen y a su API.</sub>

## Míralo en acción

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="Salida de la terminal en una generación: el modelo, un coste estimado de 0,0504 USD, el ID de la interacción, el uso de 1680 tokens de imagen por 0,0504 USD y la ruta del archivo guardado.">
</p>

Es una ejecución real. Una imagen en 2K con el modelo predeterminado cuesta unos cinco centavos de dólar, y ves la cifra antes de la llamada y otra vez después.

<a id="gallery"></a>

## Galería

Aparte del texto y de la captura de la terminal, todas las imágenes de este README se hicieron con el skill. Los prompts están en [`assets/prompts`](../assets/prompts).

<p align="center">
  <img src="../assets/gallery/1-illustration.jpg" width="760" alt="Una ilustración plana de una taza de café humeante y un cruasán sobre una barra de madera junto a una ventana soleada, con espacio vacío a la derecha para un titular.">
  <br>
  <sub><b>De texto a imagen.</b> Modelo 2.1, 2K, 16:9, unos 5 centavos.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/2a-edit-before.jpg" width="372" alt="Una taza de cerámica blanca lisa sobre un fondo de estudio gris claro.">
  <img src="../assets/gallery/2b-edit-after.jpg" width="372" alt="La misma taza blanca sobre una mesa de madera rústica junto a una ventana soleada, al lado de un pequeño cuenco con granos de café.">
  <br>
  <sub><b>Edición con <code>--follow-up</code>.</b> La misma taza, otra escena. Modelo 2.1, 2K, unos 5 centavos por imagen.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/3-poster-text.jpg" width="400" alt="Un cartel minimalista de cafetería que dice FRESH COFFEE sobre una taza de café plana, con la línea Open daily from 8 to 18.">
  <br>
  <sub><b>Texto dentro de una imagen.</b> Modelo Pro, 2K, 4:5, unos 13 centavos.</sub>
</p>

<a id="install"></a>

## Instalación

Claude Code, desde el marketplace de plugins:

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

Cualquier agente que lea skills con `SKILL.md`, mediante [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add jakubcurik/nano-banana
```

O copia `skills/nano-banana/` a mano en la carpeta de skills de tu agente, por ejemplo `~/.claude/skills/` para Claude Code o `~/.agents/skills/` para Codex, Gemini CLI y Cursor.

También necesitas:

- [`uv`](https://docs.astral.sh/uv/), que descarga por su cuenta `google-genai` y Python 3.11+. Sin él, instala Python 3.11+ y ejecuta `pip install "google-genai>=3.6,<4"`.
- Una clave de la API de Gemini de [Google AI Studio](https://aistudio.google.com/apikey), con la facturación activada. Los modelos de imagen no tienen nivel gratuito.

Pásale la clave al script por una variable de entorno, o guárdala una sola vez fuera de cualquier repositorio:

```bash
export GEMINI_API_KEY="your-key"
# or
mkdir -p ~/.config/nano-banana && printf '%s' "your-key" > ~/.config/nano-banana/api-key
```

<a id="quick-start"></a>

## Inicio rápido

Pídele a tu agente: "haz una imagen de cabecera para el sitio de mi cafetería, 16:9", "quita el coche de esta foto", "combina estas dos fotos". El skill se activa solo. Pregunta para qué es la imagen, escribe el prompt, te dice el precio cuando no es insignificante, ejecuta el script y revisa el resultado.

También puedes llamar al script tú mismo:

```bash
S=skills/nano-banana/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table" --estimate
uv run --script $S "A flat illustration of a red apple on a white table" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency EUR
```

Las imágenes se guardan en `.cache/nano-banana/`, cada una junto a un archivo `.txt` con el prompt, las opciones y el ID de la interacción.

<details>
<summary>Todas las opciones</summary>

| Opción | Significado |
|---|---|
| `-m 2.1 / 2 / pro / lite` | modelo, por defecto `2.1` |
| `-s 512 / 1K / 2K / 4K` | resolución, por defecto `1K` (512 solo en el modelo `2`) |
| `-a 16:9` | relación de aspecto: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9; en 2.1 y 2 también 1:4, 4:1, 1:8, 8:1 |
| `-i photo.jpg` | imagen de entrada para editar o como referencia, se puede repetir, máximo 14 |
| `-t minimal / medium / high` | nivel de razonamiento, según el modelo |
| `--search` | búsqueda con Google como base, incluida la búsqueda de imágenes (no en `lite`) |
| `--follow-up [ID]` | continuar desde el último resultado, o desde una interacción concreta |
| `-n 4` | número de imágenes, cada una se cobra por separado |
| `-o folder` | carpeta de salida |
| `--format png / jpeg` | formato del archivo de salida |
| `--prompt-file file` | leer el prompt desde un archivo |
| `--no-store` | pedir a Google que no guarde la interacción (así no se puede continuar sobre ella) |
| `--batch` | mitad de precio, hasta 24 h de espera (modelos 2.1 y lite) |
| `--estimate` | muestra la estimación de precio y se detiene |
| `--currency CZK` | muestra también los precios en esta moneda (cambio del Banco Nacional Checo) |

</details>

<a id="how-it-works"></a>

## Cómo funciona

El skill hace que el agente trabaje en un orden fijo. Primero pregunta para qué sirve la imagen. Si debe mostrar una especie, un producto o un lugar reales, consigue dos o tres fotos de referencia y te pide que las confirmes. Después escribe el prompt en inglés y estima el precio; si supera unos 0,50 USD o hay que generar más de cuatro imágenes, te pregunta antes. Tras generar, mira el resultado y corrige los detalles con un seguimiento en lugar de empezar de cero.

El flujo completo está en [`SKILL.md`](../skills/nano-banana/SKILL.md). Las plantillas de prompts, las plantillas de edición y una lista de errores comunes están en [`references/prompting.md`](../skills/nano-banana/references/prompting.md).

<a id="models-and-prices"></a>

## Modelos y precios

Datos a 26 de noviembre de 2026, USD por imagen.

| Modelo | Ideal para | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | casi todo | 0,034 | 0,050 | 0,113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; Google lo ha marcado como obsoleto, aún sin fecha de cierre | 0,067 | 0,101 | 0,151 |
| `pro` (`gemini-3-pro-image`) | los prompts más difíciles, mucho texto | 0,134 | 0,134 | 0,240 |
| `lite` (`gemini-3.1-flash-lite-image`) | muchas imágenes sencillas, solo 1K, sin búsqueda | 0,034 | n/a | n/a |

Los precios y los datos de los modelos están en [`models.json`](../skills/nano-banana/scripts/models.json), el único archivo que hay que editar cuando Google cambia su [lista de precios](https://ai.google.dev/gemini-api/docs/pricing). `--search` se cobra aparte: 5000 prompts con búsqueda al mes son gratis, y después 14 USD por cada 1000 consultas de búsqueda.

## Conviene saber

- Google guarda las interacciones para que funcione el seguimiento: 55 días en proyectos de pago, 1 día en el nivel gratuito. Usa `--no-store` con fotos sensibles.
- Cada imagen generada lleva una marca de agua invisible SynthID.
- El modelo se inventa detalles. Cuando una imagen tiene que coincidir con una especie, un producto o un edificio reales, dale 2-3 fotos de referencia con `-i`. El flujo del skill insiste en eso.
- Una petición que agota el tiempo de espera puede haberse cobrado igualmente, por eso el script nunca reintenta por su cuenta.
- Si publicas un resultado hecho con `--search`, Google exige mostrar sus sugerencias de búsqueda. El script las guarda junto a la imagen.

<a id="faq"></a>

## Preguntas frecuentes

**Google tiene su propia CLI `gemini-api`. ¿Para qué usar esto?**
La CLI hace la llamada, y la hace bien. Este skill añade lo que rodea a la llamada. Puede que quieras ambas.

| | CLI `gemini-api` y skills de Google | nano-banana |
|---|---|---|
| Estimación de precio antes, coste real después | no | sí |
| El agente pregunta antes de las ejecuciones caras | no | sí |
| Opciones comprobadas contra el modelo | no, las rechaza la API | sí |
| Ediciones de seguimiento sin copiar IDs | manual | `--follow-up` |
| Prompt y opciones guardados junto a cada imagen | no | sí |
| Guía de prompts y plantillas | no | sí |

La CLI está en beta y cambia rápido, así que revisa las dos antes de elegir.

**¿Funciona fuera de Claude Code?**
El skill sigue el formato abierto [Agent Skills](https://agentskills.io), así que otros agentes que carguen archivos `SKILL.md` pueden usarlo. Yo solo lo he probado en Claude Code.

**Los precios han cambiado. ¿Qué edito?**
`skills/nano-banana/scripts/models.json`, y las tablas de `SKILL.md` y de este README.

**¿Por qué pide fotos de referencia?**
Sin ellas, el modelo rellena con su imaginación los detalles de algo real, y el resultado parece plausible pero es incorrecto.

## Contribuir

Los issues y los pull requests son bienvenidos, sobre todo cuando Google cambia modelos, precios o la API. Actualiza juntos `models.json` y las tablas de `SKILL.md` y de este README. Esta traducción se hizo con ayuda de una IA, y se agradece que corrijas cualquier error que encuentres.

Las pruebas sin conexión no necesitan clave de API ni red:

```bash
python -m unittest discover -s tests
```

## Licencia

[MIT](../LICENSE)

## Historial de estrellas

<a href="https://www.star-history.com/jakubcurik/nano-banana#history">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
    <img alt="Gráfico del historial de estrellas" src="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
  </picture>
</a>
