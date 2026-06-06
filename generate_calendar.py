# -*- coding: utf-8 -*-
"""
Generador del calendario editorial SoyIA (Instagram + Facebook).
Produce, desde una sola fuente de verdad:
  - soyia-calendario-completo.csv   (formato Social Planner / GoHighLevel, 40 columnas, CRLF)
  - soyia-guiones-carruseles.md     (guion slide por slide de los 40 carruseles)
  - soyia-repo-manifiesto.md        (lista exacta de archivos de imagen a subir)

Convención de imágenes (token [REPO_BASE] para un único find-replace):
  frase-01.png .. frase-30.png
  mito-01.png  .. mito-30.png
  dato-01.png  .. dato-30.png
  cifra-01.png .. cifra-30.png
  caso-NN-slide-1.png .. caso-NN-slide-3.png   (NN = 01..30)
  complejo-NN-slide-1.png .. complejo-NN-slide-N.png (NN = 01..10, N = 5..8)
"""

import csv
from datetime import date, timedelta

REPO = "https://raw.githubusercontent.com/abolivar/soyia-rrss/main/images"
PLACEHOLDER = "2050-01-01 00:00:00"
FIXED_TAGS = "#SoyIA #CriterioPrimero"

# ---------------------------------------------------------------------------
# 1. CONTENIDO  ·  FRASES (30) — Lunes 08:30 — categoría "Frases ADN"
#    (gancho, contexto)
# ---------------------------------------------------------------------------
FRASES = [
    ("La IA no reemplaza tu criterio. Lo expone.",
     "Si tu proceso es un desorden, automatizarlo solo te da desorden más rápido. El orden va primero. La herramienta, después."),
    ("Automatizar el caos solo te da caos más rápido.",
     "La velocidad no arregla un proceso roto. Lo amplifica. Ordena primero, conecta después."),
    ("La herramienta no es la estrategia.",
     "Comprar IA sin un proceso claro es comprar un volante sin tener carro."),
    ("Criterio primero. Automatización después.",
     "Ese es el orden. No al revés. La tecnología amplifica lo que ya existe: orden o desorden."),
    ("Una pyme ordenada le gana a una corporación caótica.",
     "La IA no premia el tamaño. Premia la claridad del proceso."),
    ("Si no sabes por qué pierdes clientes, ninguna IA te lo va a adivinar.",
     "Primero el diagnóstico. Después la solución. Nunca al revés."),
    ("La IA no piensa por ti. Piensa contigo.",
     "La diferencia entre pedirle cosas y pensar con ella es la diferencia entre una herramienta y una ventaja."),
    ("El problema rara vez es de ventas. Casi siempre es de proceso.",
     "Más leads sobre un proceso roto no es crecimiento. Es más fuga."),
    ("Automatizar no es sonar frío. Es responder a tiempo.",
     "El cliente no se queja de que un sistema le conteste. Se queja de que nadie le conteste."),
    ("No necesitas más herramientas. Necesitas menos fricción.",
     "Cada app nueva sin criterio es un problema nuevo con interfaz bonita."),
    ("La IA con contexto resuelve. Sin contexto, solo acelera el caos.",
     "Darle datos sucios a un modelo es pedirle que se equivoque más rápido."),
    ("Lo que no puedes explicar, no lo puedes automatizar.",
     "Si tu proceso solo vive en la cabeza de una persona, no tienes proceso. Tienes suerte."),
    ("Responder rápido no es opcional. Es la venta.",
     "El cliente que escribe hoy no espera hasta mañana. Le escribe a otro."),
    ("La IA no es magia. Es disciplina con esteroides.",
     "Hace bien lo que ya hacías bien. Y peor lo que hacías mal."),
    ("El seguimiento cierra más que el descuento.",
     "La mayoría de las ventas se pierden en el silencio después del primer mensaje."),
    ("Tu CRM no es una agenda de contactos. Es tu memoria comercial.",
     "Sin memoria, cada conversación empieza de cero. Y el cliente lo nota."),
    ("Más rápido no siempre es mejor. Claro siempre lo es.",
     "La velocidad sin claridad solo te lleva al error antes."),
    ("La IA buena es la que no se nota.",
     "Cuando el proceso fluye, nadie aplaude la herramienta. Solo funciona."),
    ("Si todo es urgente, nada tiene proceso.",
     "La improvisación constante no es agilidad. Es ausencia de sistema."),
    ("El cliente no quiere presión. Quiere claridad.",
     "Vender no es insistir. Es responder bien, a tiempo, con contexto."),
    ("No automatices lo que ni siquiera deberías estar haciendo.",
     "Antes de hacer algo más rápido, pregunta si vale la pena hacerlo."),
    ("La tecnología no decide por ti. Ejecuta más rápido lo que tú ya definiste.",
     "Por eso el criterio va primero. Siempre."),
    ("Un proceso claro vale más que diez herramientas conectadas.",
     "La integración no arregla la confusión. La distribuye."),
    ("Tu competencia no te gana por tener mejor IA. Te gana por responder primero.",
     "La ventaja casi nunca es tecnológica. Es operativa."),
    ("Dato sucio, decisión sucia.",
     "La IA es tan buena como la información que le das. Ordena la entrada y mejora la salida."),
    ("Hacer más no es avanzar. Avanzar es hacer lo que importa.",
     "La automatización mal usada solo te deja ocupado más rápido."),
    ("La IA no entiende tu negocio. Tú se lo tienes que explicar.",
     "El contexto no se compra. Se construye."),
    ("Si no mides, no estás mejorando. Estás adivinando con confianza.",
     "Lo que no se mide, no se gestiona. Se justifica."),
    ("El humano define el criterio. La IA ejecuta a escala.",
     "Esa división del trabajo es la que funciona. La otra solo suena bien."),
    ("Menos adorno. Más criterio.",
     "Esa es la marca. Esa es la forma de trabajar."),
]

# ---------------------------------------------------------------------------
# 2. MITOS (30) — Martes 11:30 — categoría "Mitos IA"
#    (linea_mito, refutacion)
# ---------------------------------------------------------------------------
MITOS = [
    ('Mito: "La IA es solo para empresas grandes."',
     "Falso. La IA no pregunta cuántos empleados tienes. Pregunta si tu proceso está claro. Una pyme ordenada le saca más provecho que una corporación caótica con presupuesto."),
    ('Mito: "Mi negocio es demasiado humano para automatizar."',
     "Lo humano no es contestar lo mismo 40 veces al día. Eso es repetición. Automatiza la repetición y te queda tiempo para lo que sí es humano."),
    ('Mito: "Con WhatsApp normal me basta."',
     "Te basta para conversar. No para no perder conversaciones. Sin seguimiento ni orden, WhatsApp es un buzón donde se pierden ventas."),
    ('Mito: "El CRM es solo para vendedores."',
     "El CRM es la memoria del negocio. Si solo vive en la cabeza de tu gente, se va cuando ellos se van."),
    ('Mito: "Automatizar es sonar frío y robótico."',
     "Lo frío es no responder. Una respuesta a tiempo, con contexto, se siente más humana que un silencio de tres días."),
    ('Mito: "La IA va a reemplazar a mi equipo."',
     "La IA no reemplaza a quien piensa. Reemplaza la tarea que no debería estar consumiendo a quien piensa."),
    ('Mito: "Primero necesito tener todo perfecto para empezar."',
     "Perfecto no llega nunca. Necesitas un proceso claro, no perfecto. Empieza por ordenar uno, no por esperar a los diez."),
    ('Mito: "La IA es carísima."',
     "Cara es la venta que se pierde por no responder a tiempo. La IA mal elegida cuesta. El cliente que se fue, también."),
    ('Mito: "Esto es muy técnico para mi negocio."',
     "No necesitas programar. Necesitas saber qué proceso quieres ordenar. Lo técnico es problema de la herramienta, no tuyo."),
    ('Mito: "La IA aprende sola y se configura sola."',
     "La IA no adivina tu negocio. Aprende del contexto que tú le das. Sin contexto, inventa con seguridad."),
    ('Mito: "Más automatización siempre es mejor."',
     "Automatizar un proceso malo lo vuelve un problema rápido y constante. Primero arregla. Después acelera."),
    ('Mito: "Si contesto rápido parezco desesperado."',
     "Contestar rápido no es desesperación. Es respeto por el tiempo del cliente. El que tarda tres días no se ve interesante. Se ve ausente."),
    ('Mito: "La IA solo sirve para redactar textos."',
     "Eso es el 5%. El resto es ordenar seguimiento, calificar leads, recordar tareas y darte contexto para decidir."),
    ('Mito: "Mi industria es muy especial para esto."',
     "Toda industria cree que es la excepción. Ninguna lo es cuando hablamos de responder a tiempo y no perder al cliente."),
    ('Mito: "Implementar IA toma meses y paraliza todo."',
     "No tienes que cambiarlo todo de golpe. Ordena un proceso, automatiza ese, mide. Después el siguiente."),
    ('Mito: "La IA comete errores, mejor no la uso."',
     "Tu proceso manual también comete errores: el lead olvidado, el seguimiento que no pasó. La pregunta no es si hay error. Es cuál te cuesta más."),
    ('Mito: "Los chatbots espantan a los clientes."',
     "Lo que espanta es un bot sin criterio que no entiende nada. Uno con contexto, que resuelve o pasa al humano a tiempo, retiene."),
    ('Mito: "Tengo poco volumen, no me hace falta."',
     "El bajo volumen es justo cuando cada cliente pesa más. Perder uno de diez duele más que perder uno de mil."),
    ('Mito: "La IA es una moda que va a pasar."',
     "La electricidad también pareció moda. Lo que pasa son las promesas infladas. La capacidad de responder mejor y a tiempo no pasa de moda."),
    ('Mito: "Necesito un equipo de tecnología para esto."',
     "Necesitas claridad sobre tu proceso. La parte técnica se resuelve. La falta de criterio, no."),
    ('Mito: "Si automatizo, pierdo el control."',
     "Al revés. Sin sistema no tienes control: tienes memoria frágil y suerte. El proceso ordenado es lo que te devuelve el control."),
    ('Mito: "La IA es solo para vender más."',
     "También sirve para vender mejor: al cliente correcto, con el contexto correcto, sin quemar la base persiguiendo a todos."),
    ('Mito: "Ya uso varias apps, eso es suficiente."',
     "Diez apps desconectadas no son un sistema. Son diez lugares donde se pierde la información."),
    ('Mito: "El cliente siempre prefiere que lo atienda una persona."',
     "El cliente prefiere que le resuelvan. A las 11 de la noche, prefiere una respuesta clara de un sistema que un “te contesto mañana”."),
    ('Mito: "Esto solo funciona en Estados Unidos."',
     "La fricción de no responder a tiempo es igual en Panamá que en cualquier lado. El proceso ordenado no tiene nacionalidad."),
    ('Mito: "La IA va a aburrir a mis clientes con mensajes."',
     "Lo que aburre es el spam sin criterio. El seguimiento útil, en el momento correcto, no molesta. Se agradece."),
    ('Mito: "Primero vendo más, después ordeno."',
     "Vender más sobre el desorden es multiplicar el desorden. El orden no es lo que haces después de crecer. Es lo que te deja crecer."),
    ('Mito: "La IA es impersonal por definición."',
     "La personalización real necesita memoria y contexto. Justo lo que un sistema hace mejor que una libreta y una agenda saturada."),
    ('Mito: "Si funciona como está, para qué cambiar."',
     "“Funciona” suele significar “todavía no se ha caído”. Lo que depende de que nadie falle no funciona. Aguanta."),
    ('Mito: "La IA decide por mí y me quita el negocio."',
     "La IA ejecuta lo que tú defines. Si no defines criterio, no es que la IA decida mal. Es que nadie decidió."),
]

# ---------------------------------------------------------------------------
# 3. DATOS (30) — Miércoles 08:30 — categoría "Datos IA"
#    Verdades operativas (no necesariamente números). (verdad, contexto)
# ---------------------------------------------------------------------------
DATOS = [
    ("Muchos negocios no pierden clientes por falta de interés. Los pierden por falta de seguimiento.",
     "El interés del cliente tiene fecha de caducidad. Si nadie responde a tiempo, se enfría solo."),
    ("Un lead no es una venta. Es una intención con fecha de vencimiento.",
     "Lo que haces en las primeras horas decide si esa intención se convierte o se evapora."),
    ("La mayoría de las ventas no se pierden en el “no”. Se pierden en el silencio.",
     "Nadie dijo que no. Simplemente nadie volvió a escribir."),
    ("Un CRM no es una base de datos de contactos. Es la memoria de cada conversación.",
     "Sin esa memoria, cada interacción empieza de cero y el cliente lo siente."),
    ("Automatizar un proceso empieza por poder explicarlo en una hoja.",
     "Si no cabe en un diagrama simple, todavía no es un proceso. Es una costumbre."),
    ("La diferencia entre un dato y una decisión es el contexto.",
     "Un número suelto no dice nada. El mismo número, en contexto, cambia lo que haces mañana."),
    ("Un agente de IA no es un chatbot con otro nombre.",
     "El chatbot responde. El agente ejecuta tareas, sigue reglas y actúa con el contexto de tu negocio."),
    ("El primer mensaje no vende. Abre la puerta. La venta vive en el seguimiento.",
     "Casi nadie compra en el primer contacto. Casi todos compran a quien siguió ahí."),
    ("“Tener los datos” no sirve de nada si están en cinco lugares distintos.",
     "La información dispersa no es información. Es trabajo pendiente disfrazado."),
    ("Calificar un lead es decidir a quién le dedicas tiempo, no perseguir a todos.",
     "Tratar a todos igual es la forma más cara de no priorizar a nadie."),
    ("Un proceso que solo funciona cuando una persona específica está, no es un proceso.",
     "Es una dependencia. Y las dependencias se enferman, renuncian y se van de vacaciones."),
    ("La IA generativa produce texto. La automatización conecta acciones. No son lo mismo.",
     "Una redacta. La otra hace que las cosas pasen sin que tengas que recordarlas."),
    ("El tiempo de respuesta no es un detalle de servicio. Es una variable de conversión.",
     "Mientras más tardas, menos vale el lead. La curva baja rápido."),
    ("Lo que parece un problema de marketing muchas veces es un problema de seguimiento.",
     "No faltan leads. Falta qué pasa con los leads que ya llegaron."),
    ("Un “prompt” no es un truco mágico. Es una instrucción clara.",
     "La IA responde a la claridad. La misma regla que tu equipo."),
    ("La integración no arregla el desorden. Lo conecta.",
     "Unir dos procesos malos te da un proceso malo más grande y más rápido."),
    ("El dato más caro es el cliente que ya pagó y nadie volvió a contactar.",
     "Conseguir uno nuevo cuesta mucho más que cuidar al que ya confió."),
    ("Un embudo no es un dibujo bonito. Es saber dónde se cae la gente.",
     "Si no sabes en qué etapa pierdes clientes, no tienes embudo. Tienes esperanza."),
    ("La personalización no es poner el nombre del cliente. Es recordar su contexto.",
     "“Hola, [nombre]” no es personalización. Saber qué te preguntó la semana pasada, sí."),
    ("Automatizar el seguimiento no es dejar de atender. Es no olvidar a nadie.",
     "La memoria humana falla bajo volumen. El sistema no se cansa en el cliente número 50."),
    ("Un proceso comercial sin etapas definidas no se puede mejorar. Solo repetir.",
     "Para optimizar algo, primero hay que poder nombrar sus partes."),
    ("El “lo tengo en la cabeza” es el punto único de falla más común en una pyme.",
     "Lo que no está escrito ni sistematizado no es del negocio. Es de una persona."),
    ("La IA no reduce el trabajo humano. Lo reubica hacia donde el humano suma.",
     "Saca a tu gente de la tarea repetitiva y ponla donde se necesita criterio."),
    ("Responder “déjame ver y te confirmo” sin un sistema detrás casi siempre termina en olvido.",
     "La buena intención no es un proceso. El recordatorio automático, sí."),
    ("Un negocio que no mide su tiempo de respuesta no sabe cuántas ventas está perdiendo.",
     "No es que no las pierda. Es que no las ve."),
    ("El contexto es lo que separa una respuesta útil de una respuesta genérica.",
     "Sin saber quién pregunta y por qué, hasta la mejor IA suena a folleto."),
    ("Tener muchos canales abiertos sin un lugar que los unifique multiplica el caos, no la atención.",
     "Cinco bandejas distintas no es estar disponible. Es estar disperso."),
    ("La adopción de una herramienta no se mide en si la instalaste. Se mide en si cambió cómo trabajas.",
     "Una licencia pagada que nadie usa no es tecnología. Es gasto."),
    ("Lo urgente desplaza a lo importante hasta que lo importante se vuelve urgente y caro.",
     "El proceso existe justamente para que lo importante no dependa de la urgencia."),
    ("La mejor automatización es invisible: el cliente solo nota que lo atendieron bien y a tiempo.",
     "Cuando funciona, nadie habla de la herramienta. Hablan de la experiencia."),
]

# ---------------------------------------------------------------------------
# 4. CIFRAS (30) — Jueves 11:30 — categoría "Cifras IA"
#    Tomadas de datos/data.jsx (verificadas y atribuidas). (linea_cifra, angulo, fuente)
# ---------------------------------------------------------------------------
CIFRAS = [
    ("88% de las organizaciones ya usa IA regularmente en al menos una función del negocio.",
     "La IA ya no es novedad. La diferencia está en cómo la conectas al negocio.", "McKinsey"),
    ("Solo cerca de 1/3 de las empresas ha empezado a escalar sus programas de IA a nivel organizacional.",
     "Muchos usan IA. Pocos la convierten en sistema.", "McKinsey"),
    ("62% de las organizaciones ya experimenta con agentes de IA: 23% los escala y 39% explora.",
     "Los agentes ya entraron al juego. El reto es que no jueguen solos.", "McKinsey"),
    ("No más del 10% de las empresas está escalando agentes de IA en funciones específicas.",
     "Mucho discurso de agentes. Todavía poca implementación seria.", "McKinsey"),
    ("Más de 2/3 de las empresas usa IA en más de una función — y la mitad, en tres o más.",
     "La IA deja de ser herramienta cuando empieza a conectar áreas.", "McKinsey"),
    ("Solo 39% reporta impacto de la IA en el EBIT a nivel empresa, y la mayoría lo cifra por debajo del 5%.",
     "La IA sin proceso puede impresionar, pero no necesariamente mueve el negocio.", "McKinsey"),
    ("51% de las organizaciones que usa IA ya vio al menos una consecuencia negativa; casi un tercio, por inexactitud.",
     "La IA sin criterio no es ventaja. Es riesgo con buena interfaz.", "McKinsey"),
    ("Solo 5% de las empresas es considerada “future-built” en IA; 35% la escala y 60% casi no captura valor.",
     "El problema no es tener IA. Es saber convertirla en capacidad operativa.", "BCG"),
    ("5× más de incremento de ingresos logran las empresas “future-built” — y 3× más reducción de costos.",
     "La ventaja no está en el prompt. Está en el modelo operativo.", "BCG"),
    ("Hacia 2028, 29% del valor total de IA representarán los agentes; hoy ya rondan el 17%.",
     "Los agentes no son moda: son una nueva capa de operación.", "BCG"),
    ("+50% creció el acceso de los trabajadores a la IA durante 2025.",
     "La adopción sube más rápido que la madurez de muchas empresas.", "Deloitte"),
    ("Solo 34% de las empresas está realmente reimaginando el negocio con IA.",
     "Automatizar lo mismo de siempre no es transformación. Es maquillar el desorden.", "Deloitte"),
    ("Solo 1 de cada 5 empresas tiene un modelo maduro de gobernanza para agentes autónomos.",
     "Antes de soltar agentes, hay que definir límites, contexto y responsabilidad.", "Deloitte"),
    ("42% de las empresas cree que su estrategia está lista para IA — pero menos en infraestructura, datos, riesgo y talento.",
     "La estrategia suena bien hasta que toca conectarla con la operación.", "Deloitte"),
    ("82% de los líderes ve este año como clave para repensar estrategia y operaciones; 81% integrará agentes en 12–18 meses.",
     "El momento no es “probar IA”. Es rediseñar cómo trabaja la empresa.", "Microsoft Work Trend Index"),
    ("80% de la fuerza laboral dice no tener tiempo ni energía para su trabajo, mientras 53% de líderes exige más productividad.",
     "El cuello de botella no es la gente. Es el sistema donde trabaja la gente.", "Microsoft Work Trend Index"),
    ("275 interrupciones al día recibe cada empleado: una cada 2 minutos durante la jornada.",
     "No necesitas más apps. Necesitas menos fricción.", "Microsoft Work Trend Index"),
    ("46% de los líderes dice que su empresa ya usa agentes para automatizar flujos de trabajo completos.",
     "La automatización ya no es “recordatorio y correo”. Es flujo completo.", "Microsoft Work Trend Index"),
    ("42% acude a la IA antes que a un colega por su disponibilidad 24/7; le siguen velocidad (30%) e ideas ilimitadas (28%).",
     "La IA no reemplaza al humano. Cubre lo que el humano no debería cargar solo.", "Microsoft Work Trend Index"),
    ("52% todavía ve la IA como herramienta de comandos; solo 46% la trata como “socio de pensamiento”.",
     "La diferencia está entre pedirle cosas a la IA y pensar con ella.", "Microsoft Work Trend Index"),
    ("66% de los usuarios de IA gana tiempo para trabajo de alto valor; 58% produce lo que no podía hace un año.",
     "La IA bien usada no abarata el trabajo humano. Lo sube de nivel.", "Microsoft Work Trend Index 2026"),
    ("49% de las conversaciones en Copilot apoyan trabajo cognitivo: análisis, decisiones y pensamiento creativo.",
     "La IA ya no es solo “escríbeme un texto”. Está entrando en decisiones.", "Microsoft Work Trend Index 2026"),
    ("15× crecieron los agentes activos en Microsoft 365 año contra año; en grandes empresas, 18×.",
     "La adopción de agentes se acelera. La pregunta es quién los gobierna.", "Microsoft Work Trend Index 2026"),
    ("60% de su semana dedican los vendedores a tareas que no son vender; solo 40% va a vender.",
     "El problema comercial no suele ser falta de talento. Es exceso de fricción.", "Salesforce · State of Sales 2026"),
    ("69% de los profesionales de ventas dice que el cliente exige más ROI medible; 67%, más personalización.",
     "El cliente no quiere presión. Quiere claridad, contexto y seguimiento.", "Salesforce · State of Sales 2026"),
    ("94% de los líderes de ventas con agentes los considera críticos para responder a las demandas del negocio.",
     "Los agentes no son adorno tecnológico. Son capacidad comercial.", "Salesforce · State of Sales 2026"),
    ("90% de los vendedores con agentes entiende mejor a sus clientes; 88% se acerca más a sus metas.",
     "El agente correcto no reemplaza al vendedor. Le da memoria, contexto y velocidad.", "Salesforce · State of Sales 2026"),
    ("73.3% de los consumidores prefiere la mensajería para hablar con negocios; 72.4% compra más a quien la ofrece.",
     "WhatsApp no es un canal secundario. Para muchos clientes, es la puerta principal.", "WhatsApp Business · Kantar"),
    ("74.6% de los consumidores confía más en un negocio si puede escribirle; 66.8% se frustra si no puede.",
     "La confianza también se construye respondiendo donde el cliente ya conversa.", "WhatsApp Business · Kantar"),
    ("82% de los líderes de soporte invirtió en IA este año; 87% lo hará en 2026, pero solo 10% llegó a un despliegue maduro.",
     "Todos quieren IA en atención. Pocos tienen el proceso listo para que funcione.", "Intercom · 2026"),
]

# ---------------------------------------------------------------------------
# 5. CARRUSELES DE CASO (30) — Viernes 12:00 — categoría "Casos por vertical"
#    vertical, caption, (slide1 dolor, slide2 solucion, slide3 adn)
#    El orden y vertical coinciden con las carpetas de arte existentes.
# ---------------------------------------------------------------------------
CASOS = [
    dict(vertical="peluqueria", hashtags="#Peluqueria #SalonDeBelleza",
         caption="La clienta escribió un sábado para reservar. Le contestaron el lunes. Ya tenía cita en otro lado.\n\nUna peluquería no pierde clientas por el corte. Las pierde por no responder cuando la clienta quería reservar. Con SoyIA, cada mensaje recibe respuesta y la agenda se llena sola.",
         s1="Sábado, 9 p.m. Una clienta escribe para reservar. Nadie contesta hasta el lunes. Para entonces, ya reservó en otro lado.",
         s2="SoyIA responde al instante, muestra los horarios libres y agenda la cita. Sin que pierdas el sábado ni la clienta.",
         s3="No pierdes clientas por el corte. Las pierdes por el silencio."),
    dict(vertical="peluqueria", hashtags="#Peluqueria #SalonDeBelleza",
         caption="Tres citas no llegaron hoy. Nadie las confirmó. Nadie llenó el hueco.\n\nLa silla vacía no avisa. SoyIA confirma cada cita, le recuerda a la clienta y reacomoda los cancelados. El día no se trabaja a medias.",
         s1="Tres citas no llegaron hoy. Nadie confirmó, nadie avisó. La silla quedó vacía y el día, a medias.",
         s2="SoyIA confirma cada cita un día antes, le recuerda a la clienta y, si alguien cancela, ofrece el espacio a quien estaba esperando.",
         s3="La silla vacía no es mala suerte. Es seguimiento que no pasó."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Un interesado preguntó por un apartamento a las 11 p.m. Le respondieron dos días después. Ya estaba viendo otros tres.\n\nEn bienes raíces, el primero que responde con claridad lleva ventaja. SoyIA contesta al instante, califica al interesado y te avisa cuándo vale tu tiempo.",
         s1="11 p.m. Un interesado pregunta por la propiedad. La respuesta llega dos días después. Ya agendó visitas con otros tres.",
         s2="SoyIA responde al momento, filtra quién busca en serio y quién solo curiosea, y te pasa solo los contactos que valen tu tiempo.",
         s3="En bienes raíces no gana el que tiene mejor propiedad. Gana el que responde primero."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Tienes 400 contactos en el teléfono. No sabes a cuántos seguiste este mes.\n\nLa base de datos dormida es la venta que ya pagaste y no cobraste. SoyIA retoma cada contacto en el momento correcto, sin que tengas que acordarte de nadie.",
         s1="400 contactos en tu teléfono. La mitad preguntó algo hace meses. Nadie volvió a escribirles.",
         s2="SoyIA retoma cada contacto en el momento correcto, recuerda en qué quedaron y te avisa cuándo conviene volver a llamar.",
         s3="El cliente que ya preguntó no está perdido. Está esperando que alguien vuelva."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Pasaste el sábado mostrando una propiedad a alguien que no tenía cómo comprarla.\n\nTu tiempo es el inventario más caro que tienes. SoyIA califica al interesado antes de la visita: presupuesto, plazo, intención. Vas a las que cierran.",
         s1="Bloqueaste el sábado para una visita. El interesado ni tenía el presupuesto. Tiempo perdido que no vuelve.",
         s2="SoyIA pregunta lo importante antes de la cita: presupuesto, plazo, qué busca. Llegas a la visita ya sabiendo si vale la pena.",
         s3="Mostrar a todos no es vender más. Es perder tiempo más rápido."),
    dict(vertical="odontologia", hashtags="#Odontologia #Dentista",
         caption="El paciente terminó el tratamiento y nunca volvió al control. Nadie le recordó.\n\nEn odontología, el seguimiento es salud y es facturación. SoyIA recuerda cada control, reactiva pacientes y mantiene la agenda llena sin perseguir a nadie a mano.",
         s1="El paciente terminó su tratamiento hace ocho meses. Tocaba control. Nadie le escribió. No volvió.",
         s2="SoyIA recuerda cada control, reactiva a los pacientes que toca y agenda sin que la recepción tenga que perseguir a nadie.",
         s3="El paciente no se fue. Solo nadie le recordó volver."),
    dict(vertical="odontologia", hashtags="#Odontologia #Dentista",
         caption='Cotizaste un tratamiento. El paciente dijo "lo pienso". Nadie volvió a escribir.\n\nLa mayoría de los tratamientos no se rechazan. Se quedan esperando un seguimiento que nunca llega. SoyIA retoma cada cotización en el momento justo, sin sonar a presión.',
         s1='"Déjame pensarlo y te aviso." El paciente nunca avisó. Tú tampoco volviste a escribir. La cotización quedó en el aire.',
         s2="SoyIA da seguimiento a cada cotización pendiente con un mensaje claro, en el momento correcto, sin sonar a presión.",
         s3="El tratamiento no se rechazó. Se quedó esperando un seguimiento."),
    dict(vertical="estetica", hashtags="#Estetica #MedicinaEstetica",
         caption="Las promociones las mandas a todos por igual. Llegan a quien ya compró y a quien nunca preguntó.\n\nHablarle a todos por igual es la forma más cara de no hablarle a nadie. SoyIA segmenta por interés e historial y manda la oferta correcta a la persona correcta.",
         s1="Mandaste la promo a toda la lista. A la clienta frecuente y a la que pidió que no le escribieran. La misma palabra para todos.",
         s2="SoyIA segmenta por lo que cada cliente ya hizo y le manda la oferta que tiene sentido para ella. No spam. Relevancia.",
         s3="Hablarle a todos igual es no hablarle a nadie."),
    dict(vertical="restaurante", hashtags="#Restaurantes #Gastronomia",
         caption="El cliente preguntó por reservas en Instagram un viernes. Respondiste el lunes, sin mesa y sin cliente.\n\nEl viernes a la noche no espera al lunes. SoyIA responde reservas y pedidos al instante, en el canal donde el cliente ya está escribiendo.",
         s1="Viernes, hora pico. Llegan diez mensajes pidiendo mesa. Los contestas el lunes. Para entonces, ya cenaron en otro lado.",
         s2="SoyIA responde reservas y consultas al instante, confirma la mesa y te deja la cocina y el salón para lo que importa.",
         s3="El viernes a la noche no espera al lunes."),
    dict(vertical="gimnasio", hashtags="#Gimnasios #Fitness",
         caption="El socio dejó de venir hace tres semanas. Su mensualidad vence pronto. Nadie lo notó.\n\nLa retención no es suerte: es seguimiento. SoyIA detecta al socio que se está enfriando y lo reactiva antes de que cancele.",
         s1="Un socio no aparece hace tres semanas. Su plan vence el viernes. Nadie se dio cuenta. El viernes, cancela.",
         s2="SoyIA detecta al socio que dejó de venir, lo contacta a tiempo y le da una razón para volver antes de que cancele.",
         s3="La renovación no se gana el día que vence. Se gana las semanas de antes."),
    dict(vertical="veterinaria", hashtags="#Veterinaria #Mascotas",
         caption="La vacuna del paciente venció hace dos meses. El dueño no se acordó. La clínica tampoco avisó.\n\nEn una veterinaria, el recordatorio es cuidado y es ingreso recurrente. SoyIA avisa cada vacuna, control y desparasitación en su fecha.",
         s1="La vacuna venció hace dos meses. El dueño lo olvidó. La clínica no avisó. La mascota, sin protección; la clínica, sin la visita.",
         s2="SoyIA lleva el calendario de cada mascota y avisa al dueño cuándo toca vacuna, control o desparasitación. A tiempo.",
         s3="El dueño no es descuidado. Solo nadie le recordó."),
    dict(vertical="abogados", hashtags="#Abogados #ServiciosLegales",
         caption="Un cliente potencial escribió por un caso. Estabas en audiencia. Cuando viste el mensaje, ya tenía abogado.\n\nEn servicios legales, la primera respuesta pesa. SoyIA atiende la consulta inicial, agenda la cita y no deja que un caso se vaya por estar ocupado.",
         s1="Entró una consulta por un caso importante. Estabas en audiencia tres horas. Al salir, el cliente ya había contratado a otro.",
         s2="SoyIA atiende la primera consulta, recoge los datos del caso y agenda la cita, aunque tú estés en tribunal.",
         s3="El caso no se pierde en el juzgado. Se pierde en el mensaje sin responder."),
    dict(vertical="contadores", hashtags="#Contadores #Contabilidad",
         caption="Cada cierre de mes persigues a los clientes por los mismos documentos. Por correo, por WhatsApp, por teléfono.\n\nLa parte cara de la contabilidad no son los números. Es el ir y venir por papeles. SoyIA recuerda, recolecta y ordena lo que cada cliente debe entregar.",
         s1="Fin de mes otra vez. Persiguiendo a quince clientes por las mismas facturas, por tres canales distintos. Cada mes igual.",
         s2="SoyIA le recuerda a cada cliente qué documento falta, lo recibe ordenado y te avisa cuando está completo. Sin perseguir.",
         s3="Lo caro de la contabilidad no son los números. Es perseguir papeles."),
    dict(vertical="clinica-medica", hashtags="#ClinicaMedica #Salud",
         caption="El paciente pidió cita por teléfono, esperó en línea y colgó. No volvió a llamar.\n\nCada llamada sin contestar es un paciente que se atiende en otro lado. SoyIA agenda citas las 24 horas, por el canal que el paciente prefiera, sin dejarlo en espera.",
         s1="El paciente llamó para agendar. Tono de ocupado, luego espera, luego colgó. No volvió a intentarlo. Se atendió en otra clínica.",
         s2="SoyIA agenda citas las 24 horas por WhatsApp, confirma, reagenda y libera la línea para lo que de verdad necesita una persona.",
         s3="La cita no se pierde en la consulta. Se pierde en el teléfono que nadie contestó."),
    dict(vertical="seguros", hashtags="#Seguros #Corredores",
         caption="La póliza del cliente vence en dos semanas. Nadie lo contactó. Renovó con otro corredor.\n\nEn seguros, la renovación es la relación. SoyIA avisa cada vencimiento a tiempo y mantiene el contacto vivo entre pólizas.",
         s1="La póliza vence en dos semanas. El corredor no llamó. Otro sí. El cliente renovó con quien se acordó de él.",
         s2="SoyIA te avisa de cada vencimiento con tiempo, contacta al cliente y mantiene la relación viva, no solo cuando toca cobrar.",
         s3="El cliente no se va por precio. Se va con quien se acuerda de él."),
    dict(vertical="taller-mecanico", hashtags="#TallerMecanico #Automotriz",
         caption="El carro salió del taller hace seis meses. Tocaba mantenimiento. Nadie le escribió al cliente.\n\nEl mantenimiento recurrente es el ingreso más predecible de un taller, si alguien lo sigue. SoyIA recuerda cada servicio en su fecha.",
         s1="El cliente hizo su servicio hace seis meses. Toca el próximo. No se acordó. El taller tampoco avisó. Lo hizo en otro lado.",
         s2="SoyIA lleva el historial de cada vehículo y avisa al cliente cuándo toca el próximo servicio. El taller deja de depender de la memoria.",
         s3="El cliente no cambió de taller. El taller dejó de acordarse de él."),
    dict(vertical="e-commerce", hashtags="#Ecommerce #TiendaOnline",
         caption="El carrito quedó lleno y abandonado. Nadie volvió a escribirle a ese cliente.\n\nLa venta de e-commerce no termina en el carrito. Vive en el seguimiento. SoyIA recupera carritos abandonados y responde dudas antes de que el cliente cierre la pestaña.",
         s1="El cliente llenó el carrito, dudó en el pago y cerró la página. Nadie le escribió. La venta quedó a un clic, sin cerrarse.",
         s2="SoyIA responde la duda en el momento, recuerda el carrito abandonado y acompaña al cliente hasta el pago. Sin perseguir.",
         s3="La venta no se cae en el carrito. Se cae en el silencio que viene después."),
    dict(vertical="educacion", hashtags="#Educacion #Cursos",
         caption="El interesado pidió información del curso. Recibió el PDF y nada más. Se inscribió en otro lado.\n\nMandar el folleto no es vender el curso. SoyIA responde dudas, hace seguimiento y acompaña al interesado hasta la matrícula.",
         s1='Pidió info del programa. Le mandaron un PDF y un "cualquier cosa, avísame". Nadie volvió. Se matriculó en otra parte.',
         s2="SoyIA responde las dudas reales, da seguimiento al interesado y lo acompaña paso a paso hasta cerrar la matrícula.",
         s3="Mandar el folleto no es vender el curso. Acompañar la decisión, sí."),
    dict(vertical="hoteles", hashtags="#Hoteles #Turismo",
         caption="El huésped preguntó disponibilidad por WhatsApp a medianoche. Respondieron al desayuno. Ya reservó en otro hotel.\n\nEl viajero decide cuando pregunta, no cuando tú abres la oficina. SoyIA responde y reserva las 24 horas.",
         s1="Medianoche. Un viajero pregunta si hay habitación para el finde. Responden a las 8 a.m. Ya reservó en otro hotel.",
         s2="SoyIA responde disponibilidad y reserva las 24 horas, en el idioma del huésped, sin que nadie tenga que estar en recepción.",
         s3="El viajero decide cuando pregunta, no cuando abres la oficina."),
    dict(vertical="psicologia", hashtags="#Psicologia #SaludMental",
         caption="Alguien escribió pidiendo una primera cita. Le costó dar el paso. Nadie respondió a tiempo. No volvió a intentarlo.\n\nEn salud mental, la primera respuesta importa el doble. SoyIA atiende con cuidado, agenda la primera sesión y no deja sola a la persona que dio el paso.",
         s1="Alguien reunió el valor para pedir una primera sesión. El mensaje se quedó sin responder dos días. No volvió a escribir.",
         s2="SoyIA responde con calidez, da la información clara y agenda la primera sesión, sin dejar esperando a quien ya dio el paso difícil.",
         s3="Pedir ayuda ya costó. La respuesta no debería costar más."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Cerraste la venta, entregaste las llaves y ahí terminó el contacto. Ese cliente conocía a tres compradores más.\n\nLa venta cerrada es el inicio de las próximas tres. SoyIA mantiene la relación post-venta y activa referidos sin que tengas que acordarte.",
         s1="Entregaste las llaves, cerraste la venta y se acabó el contacto. Ese cliente feliz conocía a tres personas buscando casa. Nunca lo supiste.",
         s2="SoyIA mantiene la relación después del cierre, pide referidos en el momento correcto y te avisa cuándo retomar el contacto.",
         s3="La venta cerrada no es el final. Es el inicio de las próximas tres."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Llegan leads de Instagram, del portal, de la web y de WhatsApp. Cada uno en su lado. Algunos se pierden.\n\nCinco canales sin un solo lugar que los unifique no es estar disponible. Es estar disperso. SoyIA junta todos los leads en un solo flujo.",
         s1="Un lead por Instagram, otro por el portal, otro por la web, otro por WhatsApp. Cuatro bandejas. Para el viernes, dos se perdieron.",
         s2="SoyIA unifica todos los canales en un solo flujo, responde parejo y no deja que ningún lead se quede sin atención.",
         s3="Cinco bandejas abiertas no es disponibilidad. Es dispersión."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption='Hace un año alguien dijo "todavía no es el momento". Hoy quizás sí. Nadie volvió a preguntarle.\n\nEl "no ahora" no es un "no". Es un "después". SoyIA recuerda esos contactos y los retoma cuando el momento llega.',
         s1='"Todavía no es el momento." Eso dijo hace un año. Quizás hoy sí lo es. Pero nadie le volvió a escribir para averiguarlo.',
         s2='SoyIA guarda el contexto de cada "después" y retoma el contacto cuando toca, con la referencia exacta de lo que esa persona buscaba.',
         s3='El "no ahora" no es un "no". Es un "recuérdame después".'),
    dict(vertical="peluqueria-barberia", hashtags="#Barberia #Peluqueria",
         caption="El cliente venía cada tres semanas. Lleva dos meses sin aparecer. Nadie lo notó.\n\nEn una barbería, la frecuencia es el negocio. SoyIA detecta cuándo un cliente se pasa de su ciclo y lo invita a volver antes de que busque otro lugar.",
         s1="Tu cliente fijo venía cada tres semanas. Lleva dos meses sin aparecer. Nadie se dio cuenta. Encontró otra barbería cerca.",
         s2="SoyIA conoce el ciclo de cada cliente y, cuando se pasa de su fecha, le manda un recordatorio para reservar. Antes de que pruebe otro lugar.",
         s3="En la barbería, la frecuencia es el negocio. Y la frecuencia se cuida."),
    dict(vertical="odontologia", hashtags="#Odontologia #Dentista",
         caption="Tres pacientes no llegaron hoy. Ninguno avisó. La agenda se veía llena; la clínica trabajó a medias.\n\nEl no-show no es del paciente olvidadizo. Es del recordatorio que no se mandó. SoyIA confirma cada cita y reacomoda los espacios.",
         s1="La agenda decía lleno. Tres pacientes no llegaron y no avisaron. El día se trabajó a medias con la agenda “completa”.",
         s2="SoyIA confirma cada cita el día antes, reduce los no-shows y, si alguien cancela, ofrece el espacio a otro paciente en lista.",
         s3="El no-show no es descuido del paciente. Es un recordatorio que no se mandó."),
    dict(vertical="restaurante-delivery", hashtags="#Delivery #Restaurantes",
         caption="El pedido entró por mensaje, se traspapeló entre cien chats y salió tarde. El cliente no volvió a pedir.\n\nEn delivery, el caos de pedidos cuesta clientes. SoyIA toma el pedido, confirma y ordena la cola sin que nada se pierda en el chat.",
         s1="Hora pico. Cien mensajes a la vez. Un pedido se traspapeló, salió frío y tarde. Ese cliente no volvió a pedir.",
         s2="SoyIA toma cada pedido, lo confirma, lo ordena por orden de llegada y avisa los tiempos. Nada se pierde en el chat.",
         s3="En delivery no se pierde el cliente por la comida. Se pierde por el desorden."),
    dict(vertical="estetica", hashtags="#Estetica #MedicinaEstetica",
         caption="La paciente hizo la primera sesión del tratamiento. Tocaban cinco más. No volvió y nadie la contactó.\n\nLos paquetes de varias sesiones viven del seguimiento. SoyIA recuerda cada sesión y mantiene el tratamiento en marcha.",
         s1="La paciente compró un paquete de seis sesiones. Hizo una. Tocaba la segunda. Nadie le recordó. El tratamiento quedó a la mitad.",
         s2="SoyIA agenda y recuerda cada sesión del paquete, da seguimiento entre visitas y mantiene a la paciente en su tratamiento.",
         s3="El paquete no se abandona. Se queda esperando el recordatorio que no llegó."),
    dict(vertical="abogados", hashtags="#Abogados #ServiciosLegales",
         caption="Enviaste la propuesta de honorarios. El cliente la leyó. Nadie volvió a tocar el tema. El caso se enfrió.\n\nLa propuesta enviada no es el cierre. El seguimiento sí. SoyIA retoma cada propuesta con criterio, sin que parezca presión.",
         s1='Mandaste la propuesta de honorarios. "La reviso y te confirmo." Pasaron tres semanas. Nadie volvió a tocar el tema.',
         s2="SoyIA da seguimiento a cada propuesta enviada en el momento justo, resuelve la última duda y ayuda a cerrar sin sonar a presión.",
         s3="La propuesta enviada no cierra el caso. El seguimiento, sí."),
    dict(vertical="clinica-salud", hashtags="#Salud #ClinicaMedica",
         caption="El paciente terminó su chequeo. El próximo control es en seis meses. Nadie va a acordarse en seis meses.\n\nLa medicina preventiva depende del recordatorio. SoyIA agenda el seguimiento a futuro y trae de vuelta al paciente en su fecha.",
         s1='"Nos vemos en seis meses para el control." Pasaron ocho. Nadie agendó. El paciente no volvió hasta que algo dolió.',
         s2="SoyIA programa el recordatorio a futuro, contacta al paciente en su fecha y reagenda el control sin que dependa de la memoria de nadie.",
         s3="La prevención no falla por falta de interés. Falla por falta de recordatorio."),
    dict(vertical="real-estate", hashtags="#RealEstate #BienesRaices",
         caption="Pasas el día contestando las mismas cinco preguntas: precio, metraje, si acepta crédito, dónde queda, si hay cita.\n\nTu tiempo debería ir a cerrar, no a repetir. SoyIA responde lo repetitivo al instante y te deja solo las conversaciones que avanzan.",
         s1='"¿Cuánto cuesta? ¿Cuántos metros? ¿Acepta crédito?" Las mismas cinco preguntas, cuarenta veces al día. El día se va en repetir.',
         s2="SoyIA responde al instante todo lo repetitivo, califica al interesado y te pasa solo las conversaciones que de verdad avanzan.",
         s3="Tu tiempo no es para repetir. Es para cerrar."),
]

# ---------------------------------------------------------------------------
# 6. CARRUSELES COMPLEJOS / PREMIUM (10) — Viernes 12:00 — "Carruseles Premium"
#    slug, caption, slides[]
# ---------------------------------------------------------------------------
COMPLEJOS = [
    dict(slug="senales-seguimiento", tag="seguimiento",
         caption="Antes de invertir más en publicidad, revisa estas 5 señales. Si te suenan, el problema no es de leads. Es de seguimiento. Y más leads sobre un proceso roto solo es más fuga, más rápido.",
         slides=[
            "5 señales de que no necesitas más leads. Necesitas mejor seguimiento.",
            "1. Tienes contactos de hace meses que nunca volviste a tocar. La base dormida es venta que ya pagaste y no cobraste.",
            "2. No sabes en qué etapa se cae la gente. Si no puedes nombrar dónde pierdes clientes, no tienes embudo. Tienes esperanza.",
            "3. El seguimiento depende de que alguien se acuerde. La memoria humana falla bajo volumen. El cliente número 50 se pierde.",
            "4. Respondes rápido el primer mensaje y luego, silencio. Casi nadie compra en el primer contacto. Compra a quien siguió ahí.",
            "5. Inviertes más en anuncios pero cierras lo mismo. Más leads sobre un proceso roto no es crecimiento. Es más fuga.",
            "Primero arregla el seguimiento. Después compra más leads. No al revés."]),
    dict(slug="whatsapp-no-es-estrategia", tag="whatsapp",
         caption="WhatsApp es donde el cliente quiere hablar. Pero tener WhatsApp no es tener una estrategia. La diferencia entre un canal y un sistema decide cuántas ventas se te escapan cada semana.",
         slides=[
            "Tener WhatsApp no es tener una estrategia comercial.",
            "WhatsApp es un canal. Un canal te deja conversar. No te deja no perder conversaciones.",
            "Sin un sistema detrás, los mensajes se mezclan, se olvidan y se pierden entre cien chats.",
            "No hay memoria: cada conversación empieza de cero y el cliente lo nota.",
            "No hay seguimiento: el “déjame pensarlo” se queda sin respuesta para siempre.",
            "El canal lo pone el cliente. El sistema lo pones tú. SoyIA convierte WhatsApp en proceso: memoria, seguimiento y orden.",
            "WhatsApp es la puerta. La estrategia es lo que pasa adentro."]),
    dict(slug="que-automatizar-primero", tag="automatizacion",
         caption="No automatices todo de golpe. Empieza por lo que más fricción te quita y más venta te devuelve. Este es el orden que tiene sentido cuando recién arrancas.",
         slides=[
            "Qué automatizar primero en tu pyme (y qué dejar para después).",
            "Regla base: automatiza lo repetitivo y de alto impacto. No lo complejo y excepcional.",
            "1. La primera respuesta. El cliente que escribe hoy no espera a mañana. Responder a tiempo es la venta.",
            "2. El seguimiento. El “déjame pensarlo” necesita un recordatorio, no buena memoria.",
            "3. Los recordatorios de citas y vencimientos. El no-show y la renovación perdida son seguimiento que no pasó.",
            "4. La calificación de leads. Decidir a quién le dedicas tiempo antes de gastarlo.",
            "Lo que NO va primero: lo que ni siquiera deberías estar haciendo. Ordena, después automatiza."]),
    dict(slug="crm-automatizacion-agente", tag="conceptos",
         caption="Tres palabras que se usan como sinónimos y no lo son. Entender qué hace cada una evita comprar la herramienta equivocada para el problema que tienes.",
         slides=[
            "CRM, automatización y agente de IA. No son lo mismo.",
            "CRM: la memoria. Guarda quién es cada cliente y en qué quedaron. Sin él, todo empieza de cero.",
            "Automatización: los reflejos. Hace que las cosas pasen solas (recordatorios, mensajes, tareas) sin que nadie se acuerde.",
            "Agente de IA: el criterio ejecutado. Entiende contexto, responde, califica y decide dentro de las reglas que tú definiste.",
            "El error común: comprar el agente sin tener memoria ni proceso. Es ponerle cerebro a un cuerpo sin esqueleto.",
            "Primero la memoria. Luego los reflejos. Después el criterio a escala. En ese orden."]),
    dict(slug="fugas-silenciosas", tag="conversion",
         caption="No son errores ruidosos. Son fugas silenciosas: nadie las ve, pero cada semana se llevan ventas. Revisa cuáles tienes abiertas.",
         slides=[
            "7 fugas silenciosas que te están costando ventas (y no las ves).",
            "1. El mensaje de fin de semana que se responde el lunes.",
            "2. El “déjame pensarlo” que nadie retoma.",
            "3. La cotización enviada que se quedó sin seguimiento.",
            "4. El cliente que ya compró y nadie volvió a contactar.",
            "5. La cita que nadie confirmó y se volvió no-show.",
            "6. El lead que llegó por un canal que casi no revisas.",
            "7. El contacto de hace un año que dijo “después” y se quedó en después. Cada fuga es silenciosa. Juntas, son tu mayor pérdida."]),
    dict(slug="ventas-o-proceso", tag="proceso",
         caption="Cuando las ventas bajan, el instinto dice “contrata más vendedores” o “invierte más en anuncios”. A veces el problema no está ahí. Está en el proceso que nadie revisó.",
         slides=[
            "Parece problema de ventas. Casi siempre es problema de proceso.",
            "“Vendemos poco” → ¿o respondemos tarde? El tiempo de respuesta es una variable de conversión, no un detalle.",
            "“El equipo no cierra” → ¿o no hay seguimiento? Nadie cierra lo que olvidó seguir.",
            "“Necesitamos más leads” → ¿o perdemos los que ya llegan? Revisa la fuga antes de abrir más el grifo.",
            "“El cliente no decide” → ¿o nadie lo acompañó a decidir? El silencio no es una estrategia de cierre.",
            "Antes de cambiar al equipo o subir el presupuesto, revisa el proceso. Ahí suele estar la respuesta."]),
    dict(slug="ia-sin-contexto", tag="criterio",
         caption="La IA amplifica lo que ya existe. Si lo que existe es orden, acelera resultados. Si es caos, acelera el caos. El contexto es lo que marca la diferencia.",
         slides=[
            "La IA sin contexto no resuelve. Solo acelera el caos.",
            "La IA no adivina tu negocio. Trabaja con lo que le das.",
            "Datos dispersos en cinco lugares → respuestas dispersas, más rápido.",
            "Proceso que solo vive en la cabeza de alguien → nada que la IA pueda seguir.",
            "Sin reglas claras, la IA llena los huecos inventando con seguridad.",
            "El contexto no se compra con la herramienta. Se construye antes. Criterio primero. Automatización después."]),
    dict(slug="operacion-improvisada", tag="proceso",
         caption="La improvisación constante no es agilidad. Es ausencia de sistema. Así se ve la diferencia entre operar al día y operar con proceso.",
         slides=[
            "Operación improvisada vs. operación ordenada. La diferencia se siente en la caja.",
            "Improvisada: los leads viven en cinco bandejas. Ordenada: un solo flujo para todos.",
            "Improvisada: el seguimiento depende de la memoria. Ordenada: el sistema recuerda por ti.",
            "Improvisada: cada quien responde a su manera. Ordenada: criterio claro y parejo.",
            "Improvisada: no sabes dónde pierdes clientes. Ordenada: ves cada etapa del embudo.",
            "Improvisada: si falta una persona, se cae todo. Ordenada: el proceso no depende de nadie en particular.",
            "Lo improvisado aguanta hasta que crece. Lo ordenado crece sin caerse."]),
    dict(slug="mito-vs-realidad", tag="mitos",
         caption="Las objeciones más comunes para no automatizar casi siempre nacen de un malentendido. Mito por mito, esto es lo que de verdad pasa.",
         slides=[
            "Mito vs. realidad: automatizar tu negocio.",
            "Mito: “Es solo para empresas grandes.” Realidad: la IA premia el proceso claro, no el tamaño.",
            "Mito: “Suena frío.” Realidad: lo frío es el silencio de tres días, no la respuesta a tiempo.",
            "Mito: “Reemplaza a mi equipo.” Realidad: reemplaza la tarea repetitiva, no a quien piensa.",
            "Mito: “Pierdo el control.” Realidad: sin sistema no tienes control, tienes suerte.",
            "Mito: “Necesito todo perfecto primero.” Realidad: necesitas un proceso claro, no diez perfectos.",
            "La objeción casi siempre es un mito. La oportunidad casi siempre es el proceso."]),
    dict(slug="del-lead-al-cierre", tag="proceso",
         caption="Un proceso comercial no tiene que ser complicado. Tiene que ser claro. Este es el mapa simple, de la primera respuesta al cierre, donde cada etapa tiene un dueño y un seguimiento.",
         slides=[
            "Del lead al cierre: el mapa simple que la mayoría no tiene escrito.",
            "1. Llega el lead. Un solo lugar lo recibe, venga del canal que venga.",
            "2. Primera respuesta, a tiempo. Aquí se gana o se pierde la ventaja.",
            "3. Calificación. ¿Tiene presupuesto, plazo e intención? Decides dónde poner tu tiempo.",
            "4. Seguimiento. El “déjame pensarlo” se retoma en el momento correcto, sin olvidos.",
            "5. Cierre. La última duda resuelta, con el contexto de toda la conversación.",
            "6. Post-venta. El cliente cerrado es el inicio de los próximos tres. Cada etapa, un dueño y un seguimiento. Eso es un proceso."]),
]

# ---------------------------------------------------------------------------
# Hashtags variables por tipo (los 2 fijos van primero, ver build_caption)
# ---------------------------------------------------------------------------
VAR_TAGS = {
    "frase": "#AutomatizacionConCriterio #IAaplicada #AutomatizacionSinHumo #PymesPanama #NegociosLATAM #ProcesoPrimero #MenosFriccion",
    "mito":  "#MitosDeIA #AutomatizacionConCriterio #IAparaPymes #PymesPanama #NegociosLATAM #AutomatizacionSinHumo #IAaplicada",
    "dato":  "#AutomatizacionConCriterio #SeguimientoComercial #IAaplicada #PymesPanama #NegociosLATAM #VentasConProceso #ProcesoPrimero",
    "cifra": "#DatosDeIA #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #TransformacionDigital #ProductividadConCriterio",
    "complejo": "#AutomatizacionConCriterio #SeguimientoComercial #VentasConProceso #PymesPanama #NegociosLATAM #IAaplicada #ProcesoPrimero",
}


def caption_with_tags(body, variable_tags):
    return body + "\n\n" + FIXED_TAGS + " " + variable_tags


# ---------------------------------------------------------------------------
# Construcción de las filas de contenido (en orden de planificación)
# Cada item: dict con date, content, imageUrls, tags, category
# ---------------------------------------------------------------------------
def img(name):
    return REPO + "/" + name


def carousel_imgs(prefix, n):
    return ", ".join(img(f"{prefix}-slide-{i}.png") for i in range(1, n + 1))


# Construir los pools por tipo
frase_rows = []
for i, (hook, ctx) in enumerate(FRASES, 1):
    frase_rows.append(dict(
        body=hook + "\n\n" + ctx, tagset="frase",
        images=img(f"frase-{i:02d}.png"),
        tags="soyia,frase", category="Frases ADN", kind="Frase"))

mito_rows = []
for i, (m, r) in enumerate(MITOS, 1):
    mito_rows.append(dict(
        body=m + "\n\n" + r, tagset="mito",
        images=img(f"mito-{i:02d}.png"),
        tags="soyia,mito", category="Mitos IA", kind="Mito"))

dato_rows = []
for i, (v, c) in enumerate(DATOS, 1):
    dato_rows.append(dict(
        body=v + "\n\n" + c, tagset="dato",
        images=img(f"dato-{i:02d}.png"),
        tags="soyia,dato", category="Datos IA", kind="Dato"))

cifra_rows = []
for i, (line, ang, src) in enumerate(CIFRAS, 1):
    body = line + "\n\n" + ang + "\n\n[FUENTE: " + src + "]"
    cifra_rows.append(dict(
        body=body, tagset="cifra",
        images=img(f"cifra-{i:02d}.png"),
        tags="soyia,cifra", category="Cifras IA", kind="Cifra"))

caso_rows = []
for i, c in enumerate(CASOS, 1):
    variable = c["hashtags"] + " #AutomatizacionConCriterio #SeguimientoComercial #PymesPanama #NegociosLATAM #IAaplicada"
    caso_rows.append(dict(
        body=c["caption"], tagset=None, variable_tags=variable,
        images=carousel_imgs(f"caso-{i:02d}", 3),
        tags=f"soyia,carrusel,{c['vertical']}", category="Casos por vertical",
        kind="Caso", idx=i, vertical=c["vertical"], slides=[c["s1"], c["s2"], c["s3"]]))

complejo_rows = []
for i, c in enumerate(COMPLEJOS, 1):
    n = len(c["slides"])
    complejo_rows.append(dict(
        body=c["caption"], tagset="complejo",
        images=carousel_imgs(f"complejo-{i:02d}", n),
        tags=f"soyia,carrusel,premium,{c['tag']}", category="Carruseles Premium",
        kind="Complejo", idx=i, slug=c["slug"], slides=c["slides"]))


def finalize_caption(row):
    if row.get("tagset"):
        return caption_with_tags(row["body"], VAR_TAGS[row["tagset"]])
    return caption_with_tags(row["body"], row["variable_tags"])


# ---------------------------------------------------------------------------
# Calendario: 32 semanas. Lunes inicio = 2026-06-08.
# Fórmula L-V: Frase / Mito / Dato / Cifra / Carrusel.
# Semanas 1-8: fechas reales. Semanas 9+: placeholder 2050-01-01.
# Friday carousel plan (ver README, opción c).
# ---------------------------------------------------------------------------
START = date(2026, 6, 8)  # lunes
TIMES = {0: "08:30:00", 1: "11:30:00", 2: "08:30:00", 3: "11:30:00", 4: "12:00:00"}

# Opción A · cadencia intacta · 40 semanas · TODAS las fechas reales.
# Semanas 1-30: Lun Frase / Mar Mito / Mié Dato / Jue Cifra / Vie Carrusel.
# Semanas 31-40: solo Vie Carrusel (los carruseles restantes).
TOTAL_WEEKS = 40

# Viernes con carrusel premium (el resto = carrusel de caso). Premium intercalado,
# no agrupado: fundamentos (sem 2-8), dolor operativo (sem 10-16), diagnóstico (18, 22).
PREMIUM_WEEKS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 22]

# Asignar los 40 carruseles a los 40 viernes en orden cronológico.
friday_plan = {}
caso_i = 0
for week in range(1, TOTAL_WEEKS + 1):
    if week in PREMIUM_WEEKS:
        friday_plan[week] = ("complejo", PREMIUM_WEEKS.index(week) + 1)
    else:
        caso_i += 1
        friday_plan[week] = ("caso", caso_i)
assert caso_i == 30, f"Se asignaron {caso_i} casos, esperaba 30"


def date_for(week, weekday):
    """week 1-based, weekday 0=Lun..4=Vie. Todas las fechas son reales."""
    d = START + timedelta(days=(week - 1) * 7 + weekday)
    return f"{d.isoformat()} {TIMES[weekday]}"


# Ensamblar filas en orden cronológico (todas con fecha real).
schedule = []  # cada item: (postAt, row, week, label)
for week in range(1, TOTAL_WEEKS + 1):
    if week <= 30:
        schedule.append((date_for(week, 0), frase_rows[week - 1], week, f"S{week} Lun · Frase"))
        schedule.append((date_for(week, 1), mito_rows[week - 1], week, f"S{week} Mar · Mito"))
        schedule.append((date_for(week, 2), dato_rows[week - 1], week, f"S{week} Mié · Dato"))
        schedule.append((date_for(week, 3), cifra_rows[week - 1], week, f"S{week} Jue · Cifra"))
    kind, idx = friday_plan[week]
    row = caso_rows[idx - 1] if kind == "caso" else complejo_rows[idx - 1]
    schedule.append((date_for(week, 4), row, week, f"S{week} Vie · {row['kind']}"))

assert len(schedule) == 160, f"Esperaba 160 filas, hay {len(schedule)}"

# ---------------------------------------------------------------------------
# Encabezados EXACTOS del sample (40 columnas, 2 filas)
# ---------------------------------------------------------------------------
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
assert len(HEADER_1) == 40 and len(HEADER_2) == 40


def build_csv_row(post_at, row):
    cols = [""] * 40
    cols[0] = post_at
    cols[1] = finalize_caption(row)
    cols[3] = row["images"]
    cols[7] = "TRUE"    # mediaOptimization
    cols[8] = "FALSE"   # applyWatermark
    cols[9] = row["tags"]
    cols[10] = row["category"]
    cols[12] = "post"   # Facebook
    cols[13] = "post"   # Instagram
    return cols


# ---------------------------------------------------------------------------
# Escribir CSV (CRLF, UTF-8)
# ---------------------------------------------------------------------------
def write_csv(fname, chunk):
    with open(fname, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER_1)
        w.writerow(HEADER_2)
        for post_at, row, week, label in chunk:
            w.writerow(build_csv_row(post_at, row))


# Archivo completo (160 posts) — referencia / respaldo.
write_csv("soyia-calendario-completo.csv", schedule)

# Social Planner importa máx. 90 posts por archivo → calendario partido en dos.
# Corte cronológico en 90 (justo el borde de la semana 18: 18 × 5 = 90).
SPLIT = 90
write_csv("soyia-calendario-parte-1.csv", schedule[:SPLIT])   # 90 posts
write_csv("soyia-calendario-parte-2.csv", schedule[SPLIT:])   # 70 posts

# ---------------------------------------------------------------------------
# Escribir guiones de carruseles (.md)
# ---------------------------------------------------------------------------
SLIDE_ROLE_CASO = ["Slide 1 · Dolor", "Slide 2 · Solución", "Slide 3 · ADN"]

with open("soyia-guiones-carruseles.md", "w", encoding="utf-8") as f:
    f.write("# Guiones de carruseles · SoyIA\n\n")
    f.write("Texto que va en cada slide del arte. El **caption** completo (con hashtags) vive en el CSV; "
            "aquí está el contenido visual de cada lámina.\n\n")
    f.write("- Carruseles de caso: 3 slides (Dolor → Solución → ADN).\n")
    f.write("- Carruseles premium: 5–8 slides (portada → desarrollo → cierre ADN).\n\n")
    f.write("---\n\n## Carruseles de caso (30) — `Casos por vertical`\n\n")
    for i, c in enumerate(CASOS, 1):
        f.write(f"### caso-{i:02d} · {c['vertical']}\n\n")
        f.write("**Caption (CSV):**\n\n")
        for para in c["caption"].split("\n\n"):
            f.write(f"> {para}\n>\n")
        f.write("\n**Slides:**\n\n")
        for role, text in zip(SLIDE_ROLE_CASO, [c["s1"], c["s2"], c["s3"]]):
            f.write(f"- **{role}** (`caso-{i:02d}-slide-{SLIDE_ROLE_CASO.index(role)+1}.png`): {text}\n")
        f.write("\n")
    f.write("---\n\n## Carruseles premium (10) — `Carruseles Premium`\n\n")
    for i, c in enumerate(COMPLEJOS, 1):
        n = len(c["slides"])
        f.write(f"### complejo-{i:02d} · {c['slug']} ({n} slides)\n\n")
        f.write("**Caption (CSV):**\n\n")
        f.write(f"> {c['caption']}\n\n")
        f.write("**Slides:**\n\n")
        for j, text in enumerate(c["slides"], 1):
            role = "Portada" if j == 1 else ("Cierre ADN" if j == n else f"Desarrollo {j-1}")
            f.write(f"- **Slide {j} · {role}** (`complejo-{i:02d}-slide-{j}.png`): {text}\n")
        f.write("\n")

# ---------------------------------------------------------------------------
# Escribir manifiesto del repo (.md)
# ---------------------------------------------------------------------------
filenames = []
for i in range(1, 31):
    filenames.append(f"frase-{i:02d}.png")
for i in range(1, 31):
    filenames.append(f"mito-{i:02d}.png")
for i in range(1, 31):
    filenames.append(f"dato-{i:02d}.png")
for i in range(1, 31):
    filenames.append(f"cifra-{i:02d}.png")
for i in range(1, 31):
    for s in range(1, 4):
        filenames.append(f"caso-{i:02d}-slide-{s}.png")
for i, c in enumerate(COMPLEJOS, 1):
    for s in range(1, len(c["slides"]) + 1):
        filenames.append(f"complejo-{i:02d}-slide-{s}.png")

total_images = len(filenames)

with open("soyia-repo-manifiesto.md", "w", encoding="utf-8") as f:
    f.write("# Manifiesto del repositorio de imágenes · SoyIA\n\n")
    f.write(f"Total de archivos a subir: **{total_images}**.\n\n")
    f.write(f"Sube los archivos con **exactamente estos nombres** a la carpeta `images/` del repo. "
            f"Las URLs del CSV los esperan así (`{REPO}/<nombre>`). "
            f"Cualquier diferencia de nombre rompe la imagen en Social Planner.\n\n")
    f.write("Convención de slides en carruseles: el orden del nombre = el orden de aparición.\n\n")

    def block(title, names):
        f.write(f"## {title} ({len(names)})\n\n")
        for nm in names:
            f.write(f"- `{nm}`\n")
        f.write("\n")

    block("Frases — `Frases ADN`", [f"frase-{i:02d}.png" for i in range(1, 31)])
    block("Mitos — `Mitos IA`", [f"mito-{i:02d}.png" for i in range(1, 31)])
    block("Datos — `Datos IA`", [f"dato-{i:02d}.png" for i in range(1, 31)])
    block("Cifras — `Cifras IA`", [f"cifra-{i:02d}.png" for i in range(1, 31)])
    f.write("## Carruseles de caso — `Casos por vertical` (90 archivos · 30 × 3 slides)\n\n")
    for i, c in enumerate(CASOS, 1):
        f.write(f"- **caso-{i:02d}** ({c['vertical']}): "
                f"`caso-{i:02d}-slide-1.png`, `caso-{i:02d}-slide-2.png`, `caso-{i:02d}-slide-3.png`\n")
    f.write("\n## Carruseles premium — `Carruseles Premium` (slides variables 5–8)\n\n")
    cplx_count = 0
    for i, c in enumerate(COMPLEJOS, 1):
        n = len(c["slides"])
        cplx_count += n
        slides = ", ".join(f"`complejo-{i:02d}-slide-{s}.png`" for s in range(1, n + 1))
        f.write(f"- **complejo-{i:02d}** ({c['slug']}, {n} slides): {slides}\n")
    f.write(f"\n**Subtotales:** Frases 30 · Mitos 30 · Datos 30 · Cifras 30 · "
            f"Casos 90 · Premium {cplx_count} = **{total_images} imágenes**.\n")

# ---------------------------------------------------------------------------
# Resumen en consola
# ---------------------------------------------------------------------------
real = sum(1 for p, r, w, l in schedule if p != PLACEHOLDER)
placeholder = sum(1 for p, r, w, l in schedule if p == PLACEHOLDER)
print(f"Filas de contenido: {len(schedule)} (reales: {real}, placeholder: {placeholder})")
print(f"Primera fecha: {schedule[0][0]}  ·  Última fecha: {schedule[-1][0]}")
print(f"Imágenes en manifiesto: {total_images}")
by_cat = {}
for _, r, _, _ in schedule:
    by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
for k, v in by_cat.items():
    print(f"  {k}: {v}")
print(f"Partido para importación: parte-1 = {len(schedule[:SPLIT])} posts "
      f"({schedule[0][0]} → {schedule[SPLIT-1][0]}), "
      f"parte-2 = {len(schedule[SPLIT:])} posts "
      f"({schedule[SPLIT][0]} → {schedule[-1][0]})")
print("Archivos generados: soyia-calendario-completo.csv, "
      "soyia-calendario-parte-1.csv, soyia-calendario-parte-2.csv, "
      "soyia-guiones-carruseles.md, soyia-repo-manifiesto.md")
