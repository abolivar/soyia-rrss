# -*- coding: utf-8 -*-
"""Genera soyia-muestra.csv: 4 posts de prueba (2 simples + 2 carruseles),
todos con imágenes reales ya publicadas en el repo. Misma estructura que el
calendario completo (40 columnas, 2 encabezados, CRLF, UTF-8)."""

import csv

IMG = "https://raw.githubusercontent.com/abolivar/soyia-rrss/main/images"
FIXED = "#SoyIA #CriterioPrimero"


def caro(prefix, n):
    return ", ".join(f"{IMG}/{prefix}-slide-{i}.png" for i in range(1, n + 1))


# (postAt, content, imageUrls, tags, category)
SAMPLE = [
    ("2026-06-09 10:00:00",
     "Modelo: un programa entrenado con muchos datos para reconocer patrones y predecir.\n\n"
     "No necesitas saber cómo funciona por dentro. Necesitas saber qué problema le estás pidiendo resolver. "
     "La herramienta cambia; el criterio para elegirla, no.\n\n"
     + FIXED + " #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #DiccionarioIA #ProcesoPrimero",
     f"{IMG}/termino-01.png",
     "soyia,muestra,dato,termino", "Datos IA"),

    ("2026-06-09 14:00:00",
     "La clienta escribió un sábado para reservar. Le contestaron el lunes. Ya tenía cita en otro lado.\n\n"
     "Una peluquería no pierde clientas por el corte. Las pierde por no responder cuando la clienta quería reservar. "
     "Con SoyIA, cada mensaje recibe respuesta y la agenda se llena sola.\n\n"
     + FIXED + " #Peluqueria #SalonDeBelleza #AutomatizacionConCriterio #SeguimientoComercial #PymesPanama #NegociosLATAM #IAaplicada",
     caro("caso-01", 3),
     "soyia,muestra,carrusel,peluqueria", "Casos por vertical"),

    ("2026-06-10 10:00:00",
     "Inteligencia artificial: tecnología que hace tareas antes exclusivas de humanos — entender lenguaje, "
     "analizar información, reconocer patrones, generar contenido.\n\n"
     "No es magia. Es capacidad aumentada cuando hay criterio detrás. El valor no está en tenerla. "
     "Está en aplicarla a un problema real del negocio.\n\n"
     + FIXED + " #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #DiccionarioIA #AutomatizacionSinHumo",
     f"{IMG}/termino-02.png",
     "soyia,muestra,dato,termino", "Datos IA"),

    ("2026-06-10 14:00:00",
     "Un interesado preguntó por un apartamento a las 11 p.m. Le respondieron dos días después. "
     "Ya estaba viendo otros tres.\n\n"
     "En bienes raíces, el primero que responde con claridad lleva ventaja. SoyIA contesta al instante, "
     "califica al interesado y te avisa cuándo vale tu tiempo.\n\n"
     + FIXED + " #RealEstate #BienesRaices #AutomatizacionConCriterio #SeguimientoComercial #PymesPanama #NegociosLATAM #IAaplicada",
     caro("caso-03", 3),
     "soyia,muestra,carrusel,real-estate", "Casos por vertical"),
]

HEADER_1 = (["All Social"] * 12 + ["Facebook", "Instagram", "LinkedIn", "LinkedIn"]
            + ["Google (GBP)"] * 10 + ["YouTube"] * 3 + ["TikTok"] * 7
            + ["Community", "Community", "Pinterest", "Pinterest"])
HEADER_2 = [
    "postAtSpecificTime (YYYY-MM-DD HH:mm:ss)", "content", "OGmetaUrl (url)",
    "imageUrls (comma-separated)", "gifUrl", "videoUrls (comma-separated)",
    "thumbnailUrl", "mediaOptimization (true/false)", "applyWatermark (true/false)",
    "tags (comma-separated)", "category", "followUpComment",
    "type (post/story/reel)", "type (post/story/reel)", "pdfTitle",
    "postAsPdf (true/false)", "eventType (call_to_action/event/offer)",
    "actionType (none/order/book/shop/learn_more/call/sign_up)", "title", "offerTitle",
    "startDate (YYYY-MM-DD HH:mm:ss)", "endDate (YYYY-MM-DD HH:mm:ss)",
    "termsConditions", "couponCode", "redeemOnlineUrl", "actionUrl",
    "title", "privacyLevel (private/public/unlisted)", "type (video/short)",
    "privacyLevel (everyone/friends/only_me)", "promoteOtherBrand (true/false)",
    "enableComment (true/false)", "enableDuet (true/false)", "enableStitch (true/false)",
    "videoDisclosure (true/false)", "promoteYourBrand (true/false)",
    "title", "notifyAllGroupMembers (true/false)", "title", "link",
]


def row(post_at, content, images, tags, category):
    c = [""] * 40
    c[0] = post_at
    c[1] = content
    c[3] = images
    c[7] = "TRUE"
    c[8] = "FALSE"
    c[9] = tags
    c[10] = category
    c[12] = "post"
    c[13] = "post"
    return c


with open("soyia-muestra.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER_1)
    w.writerow(HEADER_2)
    for s in SAMPLE:
        w.writerow(row(*s))

print("soyia-muestra.csv generado:", len(SAMPLE), "posts (2 simples + 2 carruseles)")
