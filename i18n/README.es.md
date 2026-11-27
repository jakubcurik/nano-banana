<p align="center">
  <img src="../assets/logo.png" width="132" alt="Logotipo de nano-banana: un personaje de plátano amarillo brillante que saluda sobre un cuadrado gris grafito oscuro">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>Imágenes desde tu agente de programación, con el gasto bajo control.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validación" src="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Versión" src="https://flat.badgen.net/github/release/jakubcurik/nano-banana?label=release&color=ffd54a&labelColor=0f1b2d"></a>
  <a href="../LICENSE"><img alt="Licencia: MIT" src="../assets/badges/license-mit.svg"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Estrellas" src="https://flat.badgen.net/github/stars/jakubcurik/nano-banana?label=stars&color=ffd54a&labelColor=0f1b2d"></a>
</p>

<p align="center">
  <img alt="Plugin para Claude Code" src="../assets/badges/claude-code-plugin.svg">
  <a href="https://agentskills.io"><img alt="Compatible con el formato Agent Skills" src="../assets/badges/agent-skills.svg"></a>
  <img alt="Python 3.11 o superior" src="../assets/badges/python.svg">
  <img alt="Gemini API" src="../assets/badges/gemini-api.svg">
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
  <img src="../assets/hero.jpg" width="880" alt="Un personaje de plátano 3D brillante pinta un paisaje soleado en un pequeño caballete, junto a un largo recibo de papel y unas monedas de oro. El título dice nano-banana.">
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

Aparte del texto y de la captura de la terminal, todas las imágenes de este README se hicieron con la skill. Todas las personas, lugares y objetos que aparecen en ellas están generados por IA. Los prompts están en [`assets/prompts`](../assets/prompts).

<p align="center">
  <img src="../assets/gallery/photo-gallery-wall.jpg" width="266" alt="Foto de móvil de una sola banana pegada con cinta americana plateada a una pared blanca de galería, junto a una tarjeta blanca en blanco; al fondo, desenfocados, dos visitantes la observan con seriedad.">
  <img src="../assets/gallery/photo-shopping-cart.jpg" width="266" alt="Foto de móvil de una banana abrochada con un cinturón rojo en el asiento infantil de un carrito de supermercado.">
  <img src="../assets/gallery/photo-car-seat.jpg" width="266" alt="Foto de móvil desde el asiento del conductor: una banana sentada derecha en el asiento del copiloto, con el cinturón de seguridad abrochado sobre ella.">
  <br>
  <sub><b>Fotos al estilo del móvil.</b> Una banana pegada con cinta en la pared de una galería, abrochada en un carrito de supermercado y sujeta con el cinturón en el asiento de un coche. Model 2.1, 2K, 3:4, unos 5 centavos de dólar cada una.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/edit-before-night-flash.jpg" width="372" alt="Una mujer pasa de noche junto a un escaparate, iluminada por el flash fuerte de la cámara, con una banana a medio pelar en la mano y mirando hacia la izquierda.">
  <img src="../assets/gallery/edit-after-sunny-day.jpg" width="372" alt="La misma foto con luz intensa de tarde y cielo azul: la misma mujer, la misma pose, la misma banana y el mismo escaparate.">
  <br>
  <sub><b>Edición con <code>--image</code>.</b> Una foto con flash de noche se convirtió en una tarde soleada. Todo lo demás se mantuvo igual, salvo la luz. Model 2.1, 1K, unos 3 centavos de dólar.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/graphic-infographic.jpg" width="760" alt="Una infografía titulada Anatomy of a banana: una banana brillante sobre fondo oscuro con cuatro etiquetas que señalan Stem, Peel, Fruit y Tip.">
  <br>
  <img src="../assets/gallery/graphic-poster.jpg" width="300" alt="Un póster de viajes retro con los textos BANANA ISLAND y Visit the sunny side, con una isla en forma de banana, palmeras y un velero al atardecer.">
  <img src="../assets/gallery/graphic-vector.jpg" width="375" alt="Una ilustración vectorial plana de una banana hecha con formas geométricas en amarillo y ámbar sobre un fondo verde azulado suave.">
  <br>
  <sub><b>Gráficos.</b> Una infografía y un póster de texto con Model Pro (2K, unos 13 centavos de dólar cada uno) y una ilustración vectorial plana con Model 2.1 (2K, unos 5 centavos de dólar).</sub>
</p>

<p align="center">
  <img src="../assets/gallery/mascot-hammock.jpg" width="372" alt="La mascota banana 3D brillante, con gafas de sol, descansa en una hamaca entre dos palmeras en una playa tropical.">
  <img src="../assets/gallery/mascot-surf.jpg" width="372" alt="La mascota banana 3D brillante sobre una tabla de surf pequeña, en una ola turquesa, con los brazos abiertos para mantener el equilibrio.">
  <br>
  <sub><b>La misma mascota en escenas nuevas</b> con <code>--follow-up</code>. Model 2.1, 1K, unos 3 centavos de dólar cada una.</sub>
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
