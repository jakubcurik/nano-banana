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
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Versión" src="../assets/badges/release.svg"></a>
  <a href="../LICENSE"><img alt="Licencia: MIT" src="../assets/badges/license-mit.svg"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="Estrellas" src="../assets/badges/stars.svg"></a>
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

Este skill muestra el precio estimado antes de cada llamada y el coste real después, incluidos los tokens de razonamiento y de entrada. Una ejecución cuya estimación supera tu límite (0,50 USD salvo que pongas otro) se detiene antes de enviar nada. Comprueba tus opciones contra lo que admite el modelo elegido, así que un tamaño incorrecto o un nivel de razonamiento no compatible falla en tu máquina y no en la API. Para todo lo demás, le da al agente una rutina corta: averiguar para qué es la imagen, conseguir fotos de referencia cuando el sujeto tiene que parecerse a algo real, escribir el prompt en inglés y mirar el resultado antes de darlo por terminado.

<sub>No oficial. No está afiliado a Google ni cuenta con su respaldo. "Nano Banana" y "Gemini" son los nombres que Google da a sus modelos de imagen y a su API.</sub>

## Míralo en acción

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="Salida de la terminal en una generación: el modelo, un coste estimado de 0,0336 USD, la respuesta de la API en 17,9 segundos, la ruta del archivo guardado, la breve respuesta del modelo, el ID de la interacción y un coste real de 0,0426 USD desglosado en tokens de imagen, razonamiento, texto y entrada.">
</p>

Es una ejecución real. La imagen en sí, en 1K con el modelo predeterminado, se estima en 0,0336 USD. El coste real tras la llamada suma el razonamiento, la breve respuesta de texto del modelo y el prompt, aquí 0,0426 USD, y la salida muestra que la llamada tardó 18 segundos.

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
uv run --script $S --batch-result
uv run --script $S "Same scene at dusk. Keep everything else the same." --follow-up .cache/nano-banana/20261128-101500-a-flat-illustration-2.png

F=skills/nano-banana/scripts/finish.py
uv run --script $F .cache/nano-banana/hero.png --size 1200x630 --format webp
uv run --script $F .cache/nano-banana/icon.png --transparent
```

Las imágenes se guardan en `.cache/nano-banana/`, cada una junto a un archivo `.txt` con el prompt, las opciones, el ID de la interacción, la duración de la llamada y su coste. La carpeta recibe su propio `.gitignore`, así que nada de ella acaba en git.

Un trabajo por lotes espera como mucho 8 minutos (`--wait`); después el script termina y te dice cómo recoger el resultado. `--batch-result` guarda las imágenes cuando el trabajo ha terminado; si lo ejecutas otra vez, no las duplica.

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
| `--follow-up [IMAGE or ID]` | continuar desde el último resultado, desde una imagen elegida (su `.txt` guarda el ID) o desde una interacción concreta |
| `-n 4` | número de imágenes, cada una se cobra por separado |
| `-o folder` | carpeta de salida |
| `--name hero` | inicio del nombre de archivo en lugar del comienzo del prompt |
| `--format png / jpeg` | formato del archivo; 2.1, 2 y lite solo devuelven JPEG, así que ahí se rechaza `png` |
| `--prompt-file file` | leer el prompt desde un archivo |
| `--no-store` | pedir a Google que no guarde la interacción (así no se puede continuar sobre ella) |
| `--delete IMAGE or ID` | borrar una interacción guardada en Google |
| `--batch` | mitad de precio, hasta 24 h de espera (modelos 2.1 y lite) |
| `--wait 8` | minutos de espera a un trabajo por lotes antes de terminar; `0` solo lo envía |
| `--batch-result [JOB]` | recoger un trabajo por lotes; por defecto, el último enviado a la carpeta de salida |
| `--estimate` | muestra la estimación de precio y se detiene |
| `--max-cost 0.50` | detenerse antes de la llamada si la estimación supera esos USD |
| `--currency CZK` | muestra también los precios en esta moneda (cambio del Banco Nacional Checo) |

`--currency` y `--max-cost` también pueden venir de `NANO_BANANA_CURRENCY` y `NANO_BANANA_MAX_COST`, o de `~/.config/nano-banana/config.json` (`{"currency": "EUR", "max_cost": 1}`). Manda la línea de comandos, después el entorno y después el archivo.

`finish.py` admite `--size WxH` (rellena y recorta; `--keep` elige la parte que se queda), `--format webp / avif / jpeg / png`, `--quality` y `--transparent [COLOR]`.

</details>

<a id="how-it-works"></a>

## Cómo funciona

El skill hace que el agente trabaje en un orden fijo. Primero deduce para qué sirve la imagen a partir de tu petición y de tu proyecto, y solo pregunta lo que falta. Si debe mostrar una especie, un producto o un lugar reales, consigue dos o tres fotos de referencia y te pide que las confirmes. Después escribe el prompt en inglés y estima el precio. Por encima de 0,50 USD el propio script se niega a ejecutarse, y el agente solo sube el límite cuando tú aceptas; también pregunta antes de generar más de cuatro imágenes. Tras generar, mira el resultado, corrige los detalles con un seguimiento en lugar de empezar de cero y puede recortar y convertir la imagen para la página a la que va.

El flujo completo está en [`SKILL.md`](../skills/nano-banana/SKILL.md). Las plantillas de prompts, las plantillas de edición y una lista de errores comunes están en [`references/prompting.md`](../skills/nano-banana/references/prompting.md).

<a id="models-and-prices"></a>

## Modelos y precios

Datos a 28 de noviembre de 2026, USD por imagen. Los tokens de razonamiento y de entrada se pagan aparte, normalmente menos de un centavo por imagen.

| Modelo | Ideal para | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | casi todo | 0,034 | 0,050 | 0,113 |
| `2` (`gemini-3.1-flash-image`) | 512 px; Google lo ha marcado como obsoleto, aún sin fecha de cierre | 0,067 | 0,101 | 0,151 |
| `pro` (`gemini-3-pro-image`) | los prompts más difíciles, mucho texto | 0,134 | 0,134 | 0,240 |
| `lite` (`gemini-3.1-flash-lite-image`) | muchas imágenes sencillas, solo 1K, sin búsqueda | 0,034 | n/a | n/a |

Los precios y los datos de los modelos están en [`models.json`](../skills/nano-banana/scripts/models.json), el único archivo del que el script lee los precios cuando Google cambia su [lista de precios](https://ai.google.dev/gemini-api/docs/pricing); una prueba falla si las tablas de aquí y de `SKILL.md` dejan de coincidir con él. `--search` se cobra aparte: 5000 prompts con búsqueda al mes son gratis, y después 14 USD por cada 1000 consultas de búsqueda.

## Conviene saber

- Google guarda las interacciones para que funcione el seguimiento: 55 días en proyectos de pago, 1 día en el nivel gratuito. Usa `--no-store` con fotos sensibles, o borra una interacción después con `--delete`.
- Cada imagen generada lleva una marca de agua invisible SynthID.
- El modelo se inventa detalles. Cuando una imagen tiene que coincidir con una especie, un producto o un edificio reales, dale 2-3 fotos de referencia con `-i`. El flujo del skill insiste en eso.
- Tras un error, el script dice si es seguro volver a intentarlo. Una petición rechazada (4xx, como una opción incorrecta, una clave que falta o una cuota agotada) no se cobró. Un error del servidor o un tiempo de espera agotado sí pueden haberse cobrado, por eso el script nunca reintenta por su cuenta.
- En las pruebas reales de la 1.1, una imagen 1K con el modelo 2.1 tardó 11,5-17,9 segundos. Un agente cuya llamada a la shell agota su tiempo pierde una imagen ya pagada, por eso el skill le indica que deje tiempo suficiente o que ejecute los trabajos largos en segundo plano.
- El modelo no puede devolver una imagen transparente: entrega JPEG y, si le pides transparencia, pinta un falso tablero de ajedrez. Pide un fondo liso y recórtalo con `finish.py --transparent`, que elimina un color plano; las sombras suaves y los degradados se quedan.
- Si publicas un resultado hecho con `--search`, Google exige mostrar sus sugerencias de búsqueda. El script las guarda junto a la imagen.

<a id="faq"></a>

## Preguntas frecuentes

**Google tiene su propia CLI `gemini-api`. ¿Para qué usar esto?**
La CLI hace la llamada, y la hace bien. Este skill añade lo que rodea a la llamada. Puede que quieras ambas.

| | CLI `gemini-api` y skills de Google | nano-banana |
|---|---|---|
| Estimación de precio antes, coste real después | no | sí |
| Las ejecuciones caras se detienen hasta que subes el límite | no | sí (`--max-cost`) |
| Dice si una llamada fallida puede haberse cobrado | no | sí |
| Opciones comprobadas contra el modelo | no, las rechaza la API | sí |
| Ediciones de seguimiento sin copiar IDs | manual | `--follow-up` |
| Prompt y opciones guardados junto a cada imagen | no | sí |
| Resultados por lotes recuperables en otra ejecución | no | `--batch-result` |
| Recorte, conversión y fondo transparente para la web | no | `finish.py` |
| Guía de prompts y plantillas | no | sí |

La CLI está en beta y cambia rápido, así que revisa las dos antes de elegir.

**¿Funciona fuera de Claude Code?**
El skill sigue el formato abierto [Agent Skills](https://agentskills.io), así que otros agentes que carguen archivos `SKILL.md` pueden usarlo. Yo solo lo he probado en Claude Code.

**Los precios han cambiado. ¿Qué edito?**
`skills/nano-banana/scripts/models.json`, y las tablas de `SKILL.md`, de este README y de las traducciones. Las pruebas te avisan si alguna se queda atrás.

**¿Por qué pide fotos de referencia?**
Sin ellas, el modelo rellena con su imaginación los detalles de algo real, y el resultado parece plausible pero es incorrecto.

## Contribuir

Los issues y los pull requests son bienvenidos, sobre todo cuando Google cambia modelos, precios o la API. Actualiza juntos `models.json` y las tablas de `SKILL.md` y de este README. Esta traducción se hizo con ayuda de una IA, y se agradece que corrijas cualquier error que encuentres.

Las pruebas sin conexión no necesitan clave de API ni red (las pruebas de `finish.py` se ejecutan si Pillow está instalado y, si no, se omiten):

```bash
python -m unittest discover -s tests
```

## Licencia

[MIT](../LICENSE)
