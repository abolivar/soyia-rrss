# Calendario editorial SoyIA — README

Resumen de decisiones, flujo de trabajo y puntos a revisar antes de publicar.
Todo el contenido se genera desde una sola fuente de verdad: `generate_calendar.py`.
Si hay que corregir un caption, se edita ahí y se vuelve a correr (`python3 generate_calendar.py`)
para que el CSV, los guiones y el manifiesto queden siempre sincronizados.

---

## Entregables

| Archivo | Qué es |
|---|---|
| `soyia-calendario-completo.csv` | 160 posts en formato Social Planner (GoHighLevel). 162 líneas (2 de encabezado + 160 de datos). Listo para importar tras reemplazar `[REPO_BASE]`. |
| `soyia-guiones-carruseles.md` | Guion slide por slide de los 30 carruseles de caso (3 slides) y 10 premium (5–8 slides). El CSV solo lleva el caption; el texto de cada lámina vive aquí. |
| `soyia-repo-manifiesto.md` | Lista exacta de las **278 imágenes** a subir, con los nombres que el CSV espera. |
| `generate_calendar.py` | El generador. Fuente de verdad de los 160 textos. |

---

## Inventario (160 posts)

| Tipo | Cantidad | Categoría (`category`) | Día | Hora (Panamá, UTC−5) |
|---|---:|---|---|---|
| Frases | 30 | `Frases ADN` | Lunes | 08:30 |
| Mitos | 30 | `Mitos IA` | Martes | 11:30 |
| Datos | 30 | `Datos IA` | Miércoles | 08:30 |
| Cifras | 30 | `Cifras IA` | Jueves | 11:30 |
| Carruseles de caso (3 slides) | 30 | `Casos por vertical` | Viernes | 12:00 |
| Carruseles premium (5–8 slides) | 10 | `Carruseles Premium` | Viernes | 12:00 |

Fórmula semanal L–V: **Frase → Mito → Dato → Cifra → Carrusel.**

---

## Fechas

- **Arranque:** lunes **8 de junio de 2026**, 08:30.
- **Primeras 8 semanas (40 posts):** fechas reales secuenciales, del **2026-06-08** al **2026-07-31**.
- **Resto (120 posts):** fecha placeholder **`2050-01-01 00:00:00`** (el mismo patrón del sample para "no programar todavía"). Quedan cargados y se activan cambiando la fecha cuando David lo decida.

---

## Decisión sobre el desajuste de carruseles → **opción (c)**

Hay 40 carruseles (30 de caso + 10 premium) y 32 viernes en 32 semanas: **sobran 8 carruseles**.
Se eligió la **opción (c)** del brief (la más limpia, respeta la cadencia):

- **32 viernes** cargan un carrusel cada uno (22 de caso + 10 premium, intercalados).
- Los **8 carruseles de caso restantes** quedan como **"banco"** al final del CSV, con fecha placeholder `2050-01-01`. David los activa cuando quiera, sin romper la cadencia de un carrusel por viernes.
- Banco = `caso-23` a `caso-30` (verticales: real-estate, peluquería-barbería, odontología, restaurante-delivery, estética, abogados, clínica-salud, real-estate).

### Distribución de los 10 carruseles premium

No se publican todos al inicio. Se intercalan reemplazando un carrusel de caso, según el brief:

- **Meses 1–2 (semanas 2, 4, 6, 8):** premium 01–04 — fundamentos.
- **Meses 3–4 (semanas 10, 12, 14, 16):** premium 05–08 — dolor operativo / seguimiento.
- **Meses 5–6 (semanas 18, 22):** premium 09–10 — diagnóstico / conversión.

> Nota: como el contenido de Frase/Mito/Dato/Cifra es de 30 piezas, esos tipos llenan las semanas 1–30. Las semanas 31–32 solo llevan su carrusel de viernes. Esto no afecta la importación: el orden de las filas es cronológico para las 8 semanas reales y de planificación para el resto (todas con placeholder).

---

## Hosting de imágenes — resuelto

Las URLs del CSV **ya apuntan al repo** (no queda token `[REPO_BASE]` por reemplazar):

```
Base: https://raw.githubusercontent.com/abolivar/soyia-rrss/main/images
```

- Se sirve por **GitHub raw** sobre el repo público `abolivar/soyia-rrss`, carpeta `images/`. Funciona de inmediato sin habilitar GitHub Pages; Social Planner (GHL) descarga la imagen del lado servidor.
- **Ya viven en el repo (90 imágenes):** los 30 carruseles de caso (`caso-01..30-slide-1/2/3.png`), copiados desde `Carruseles SoyIA PNG/`. Esas URLs resuelven hoy.
- **Faltan por subir (188 imágenes):** `frase-*`, `mito-*`, `dato-*`, `cifra-*` y los `complejo-*` (premium). Diséñalas, nómbralas según `soyia-repo-manifiesto.md` y súbelas a `images/`. Mientras no existan, esas URLs dan 404 (esperado).
- Si prefieres GitHub Pages en vez de raw, la base sería `https://abolivar.github.io/soyia-rrss/images` tras habilitar Pages; habría que regenerar el CSV cambiando `REPO` en `generate_calendar.py`.

## Convención de nombres de imágenes

Las URLs del CSV usan la base de arriba + un nombre predecible:

```
frase-01.png … frase-30.png
mito-01.png  … mito-30.png
dato-01.png  … dato-30.png
cifra-01.png … cifra-30.png
caso-01-slide-1.png, caso-01-slide-2.png, caso-01-slide-3.png … hasta caso-30-*
complejo-01-slide-1.png … complejo-10-slide-N.png   (N = 5 a 8 según el carrusel)
```

Total: **278 imágenes** (30+30+30+30 + 30×3 + 64 de premium). El detalle exacto está en `soyia-repo-manifiesto.md`.

### Arte que David ya tiene (mapeo de referencia)

Las carpetas en `RRSS/` ya contienen arte que se alinea con esta estructura. Al exportar, renómbralo a la convención de arriba:

| Carpeta existente | Mapea a | Notas |
|---|---|---|
| `Carruseles SoyIA PNG/NN-vertical/` (`1-dolor`, `2-solucion`, `3-adn`) | `caso-NN-slide-1/2/3.png` | El orden de carpeta (01–30) y el vertical **coinciden** con `caso-01..30`. |
| `datos/data.jsx` (30 cifras con fuente) | textos de `cifra-01..30` | **Ya usado**: los 30 captions de Cifras salen de aquí, con su fuente real. |
| `biblioteca/biblioteca_01..30.png` | candidatos para `frase-01..30.png` | Verificar que el texto del arte coincida con el caption. |
| `terminos/01..30-termino.png` | candidatos para `dato-01..30.png` | Son placas de glosario; revisar correspondencia con cada Dato. |
| `mitos/Mito 01..10 PNG/` | arte de mitos (hay 10, faltan 20) | Las placas de Mito como imagen única son `mito-01..30.png`. Falta diseñar 20. |

---

## Flujo para David (de "CSV listo" a "importado")

La base de URL ya está puesta y los 90 slides de carrusel de caso ya están en el repo. Falta:

1. **Diseñar / exportar las 188 imágenes restantes** (`frase-*`, `mito-*`, `dato-*`, `cifra-*`, `complejo-*`) y nombrarlas según `soyia-repo-manifiesto.md`.
2. **Subirlas a la carpeta `images/`** del repo (`git add images/ && git commit && git push`).
3. **Importar** `soyia-calendario-completo.csv` a Social Planner (GoHighLevel). No hace falta find-replace: las URLs ya están resueltas.

> El nombre de archivo en `images/` debe coincidir 1:1 con el del CSV. Si el manifiesto dice `caso-07-slide-2.png`, ese archivo debe existir con ese nombre en `images/`.

---

## Especificación técnica del CSV (cumplida)

- **40 columnas**, en el mismo orden y con los mismos encabezados que `social-planner-advance-sample.csv` (2 filas de encabezado idénticas, datos desde la fila 3).
- Columnas pobladas: `postAtSpecificTime`, `content`, `imageUrls`, `mediaOptimization=TRUE`, `applyWatermark=FALSE`, `tags`, `category`, `Facebook type=post`, `Instagram type=post`. El resto (LinkedIn, GBP, YouTube, TikTok, Community, Pinterest) van **vacías**.
- **Comillas dobles** en campos con comas internas (imageUrls de carrusel, tags con comas) y en captions con saltos de línea — manejado por el escritor CSV.
- **Booleanos en MAYÚSCULA** (`TRUE` / `FALSE`).
- **Saltos de línea** dentro de los captions, dentro de campo entrecomillado (legibilidad).
- **Encoding UTF-8**, **terminador de fila CRLF** (`\r\n`), como el sample, para compatibilidad con GHL.
- Todo es tipo **`post`** (sin `story` ni `reel`).

---

## Hashtags

- Van **dentro del caption** (`content`), al final.
- **2 fijos primero, siempre:** `#SoyIA #CriterioPrimero` (en los 160 posts).
  - `#CriterioPrimero` es el hashtag propietario de tracking de toda la campaña.
- **6–10 variables** después: tema + nicho/geo + vertical cuando aplica. Total 8–12 por post.

---

## Cifras: fuentes a revisar antes de publicar

**No hay cifras inventadas.** Las 30 Cifras provienen de `datos/data.jsx`, que ya trae fuente atribuida.
Cada caption de Cifra cierra con `[FUENTE: …]`. **David debe validar que cada dato siga vigente y bien citado** antes de publicar. Fuentes usadas:

| Cifras | Fuente declarada |
|---|---|
| 01–07 | McKinsey |
| 08–10 | BCG |
| 11–14 | Deloitte |
| 15–20 | Microsoft Work Trend Index |
| 21–23 | Microsoft Work Trend Index 2026 |
| 24–27 | Salesforce · State of Sales 2026 |
| 28–29 | WhatsApp Business · Kantar |
| 30 | Intercom · 2026 |

> Acción para David: confirmar que estas fuentes y porcentajes correspondan a los reportes citados y al año. La etiqueta `[FUENTE: …]` queda visible en el caption; ajústala o quítala según tu política de publicación.
> **No quedaron cifras con `[CIFRA POR VALIDAR]`** porque todas tienen fuente atribuida en `data.jsx`. Si alguna no te convence, reescribe la idea sin el número en `generate_calendar.py` y vuelve a generar.

---

## Checklist de calidad (verificado)

- [x] 160 filas de datos + 2 de encabezado = **162 líneas**.
- [x] 40 posts con fecha real (2026-06-08 → 2026-07-31); 120 con placeholder `2050-01-01 00:00:00`.
- [x] Cada tipo cae en su día y respeta la fórmula semanal.
- [x] Ninguna cifra inventada: todas con `[FUENTE: …]` verificable.
- [x] Voz SoyIA en cada caption (anti-hype, criterio primero, sin gurú, sin cierre de servicio al cliente).
- [x] `#SoyIA` y `#CriterioPrimero` en los 160 posts + 6–10 variables coherentes.
- [x] Estructura de columnas idéntica al sample; comas internas entrecomilladas; booleanos en mayúscula; CRLF.
- [x] `category` y `tags` poblados en las 160 filas.
- [x] Carruseles: caption en `content`, slides en `soyia-guiones-carruseles.md`.
- [x] Manifiesto coherente con las URLs del CSV (mismo conteo y nombres): **278 imágenes**.
