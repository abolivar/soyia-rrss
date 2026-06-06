# Calendario editorial SoyIA — README

Calendario reconstruido sobre el **arte real** del directorio. Todo el contenido se genera
desde una sola fuente de verdad: `generate_calendar.py`. Si editas un caption, vuelve a correr
`python3 generate_calendar.py` y el CSV, los guiones y el manifiesto quedan sincronizados.

---

## Inventario real — 5 series · 130 posts · 260 imágenes

| Serie | Carpeta origen | Formato | Posts | Imágenes |
|---|---|---|---|---|
| **Biblioteca** (libros) | `biblioteca/` | 1 imagen | 30 | 30 |
| **Términos** (diccionario IA) | `terminos/` | 1 imagen | 30 | 30 |
| **Datos** (cifras) | `datos/` (`data.jsx`) | 1 imagen | 30 | 30 |
| **Mitos** | `mitos/` | carrusel 8 slides | 10 | 80 |
| **Casos por vertical** | `Carruseles SoyIA PNG/` | carrusel 3 slides | 30 | 90 |
| **Total** | | | **130** | **260** |

Todas las imágenes ya están en `images/` y se sirven en
`https://raw.githubusercontent.com/abolivar/soyia-rrss/main/images/<nombre>`.
**Verificado: las 260 URLs del CSV resuelven.** No quedan 404.

---

## Entregables

| Archivo | Qué es |
|---|---|
| `soyia-calendario-parte-1.csv` | **Para importar.** Posts 1–90. |
| `soyia-calendario-parte-2.csv` | **Para importar.** Posts 91–130. |
| `soyia-calendario-completo.csv` | Los 130 posts en un archivo (respaldo). Social Planner importa máx. 90 por archivo. |
| `soyia-guiones-carruseles.md` | Casos (3 slides, texto) + Mitos (8 slides, arte ya diseñado). |
| `soyia-repo-manifiesto.md` | Las 260 imágenes y su mapeo origen → nombre de producción. |
| `generate_calendar.py` | Generador. Fuente de verdad de los 130 textos. |

---

## Cadencia y fechas

5 posts por semana cuando hay mito; 4 el resto. Una publicación por día hábil, sin fines de semana.

| Día | Hora | Serie |
|---|---|---|
| Lunes | 08:30 | Término (diccionario) |
| Martes | 11:30 | Dato (cifra) |
| Miércoles | 08:30 | Biblioteca (libro) |
| Jueves | 11:30 | Caso (carrusel 3) |
| Viernes | 12:00 | Mito (carrusel 8) — **cada 3 semanas** (sem 3, 6, 9 … 30) |

- **Arranque:** lunes **8 de junio de 2026**, 08:30.
- **Cierre:** **1 de enero de 2027** (último mito). Span: **30 semanas**.
- Las 130 publicaciones tienen **fecha real**; sin placeholders.
- Los 10 mitos (carruseles premium de 8 slides) caen un viernes cada 3 semanas para no quemarlos.

> Nota: el último mito cae el 1-ene-2027 (feriado). Si no quieres publicar ese día, muévelo en Social Planner o cambia `MITO_EVERY`/`START` en el generador.

---

## Mapeo de imágenes (origen → producción)

El arte vive en sus carpetas originales y se copia a `images/` con nombres limpios y predecibles:

| Serie | Origen | En `images/` |
|---|---|---|
| Biblioteca | `biblioteca/biblioteca_NN.png` | `libro-01..30.png` |
| Términos | `terminos/NN-termino.png` | `termino-01..30.png` |
| Datos | `datos/NN-dato.png` | `dato-01..30.png` |
| Mitos | `mitos/Mito NN PNG/SoyIA_MitoNN_0K.png` | `mito-NN-slide-1..8.png` |
| Casos | `Carruseles SoyIA PNG/NN-*/{1-dolor,2-solucion,3-adn}.png` | `caso-NN-slide-1..3.png` |

Para regenerar `images/` desde las carpetas origen, la lógica de copia está en el bloque de
organización (se corrió una vez); el manifiesto lista los 260 nombres exactos.

---

## Captions por serie

- **Términos** y **Datos**: el texto sale del propio arte (`terminos/` y `data.jsx`). El caption repite la idea + el cierre de la placa.
- **Datos**: cada uno cierra con `[FUENTE: …]` (ver abajo).
- **Biblioteca**: caption = la bajada SoyIA del libro + ficha («Título», de Autor. Categoría).
- **Mitos**: el arte (8 slides) es autónomo; el caption resume el gancho + una línea de criterio.
- **Casos**: caption + guion de 3 slides en `soyia-guiones-carruseles.md`.

---

## Hashtags

- Dentro del caption, al final. **2 fijos primero, siempre:** `#SoyIA #CriterioPrimero`.
- Luego 6–7 variables por serie (tema + nicho/geo + vertical en casos). Total 8–12 por post.

---

## Datos: fuentes a validar antes de publicar

Las 30 cifras provienen de `datos/data.jsx` y llevan `[FUENTE: …]` en el caption:

| Datos | Fuente |
|---|---|
| 01–07 | McKinsey |
| 08–10 | BCG |
| 11–14 | Deloitte |
| 15–20 | Microsoft Work Trend Index |
| 21–23 | Microsoft Work Trend Index 2026 |
| 24–27 | Salesforce · State of Sales 2026 |
| 28–29 | WhatsApp Business · Kantar |
| 30 | Intercom · 2026 |

Confirma vigencia y atribución antes de publicar.

---

## Para importar

1. `soyia-calendario-parte-1.csv` (90 posts).
2. `soyia-calendario-parte-2.csv` (40 posts).

Las URLs ya resuelven; no hace falta find-replace. `soyia-calendario-completo.csv` es respaldo.

---

## Checklist (verificado)

- [x] 130 posts · 5 series · 260 imágenes; **0 imágenes faltantes** (todas resuelven).
- [x] Fechas reales 2026-06-08 → 2027-01-01; 0 placeholders.
- [x] Cada serie en su día; estructura de 40 columnas idéntica al sample; CRLF; UTF-8.
- [x] Booleanos en mayúscula; FB+IG = `post`; resto de columnas vacías.
- [x] `#SoyIA` y `#CriterioPrimero` en los 130 posts; `category` y `tags` poblados.
- [x] Carruseles con imágenes separadas por coma y entrecomilladas.
- [x] Split para import: 90 + 40.
- [x] Ninguna cifra inventada: todas con `[FUENTE: …]`.
