// 30 placas de dato · SoyIA
// bg codifica el TIPO de dato (no la fuente):
//   "black"  → la brecha / advertencia   · cifra amarilla, texto blanco
//   "yellow" → la oportunidad            · cifra negra, texto negro
//   "white"  → el contexto / línea base  · cifra negra, texto grafito, amarillo puntual
// kicker: lectura pequeña sobre la cifra (opcional)
// fig + unit: la cifra protagonista (unit = sufijo % / × más pequeño)
// caption: la bajada — frase completa que contextualiza el dato
// angle: la lectura editorial de SoyIA
// source: la fuente, al pie
window.DATOS_DATA = [
  { n: 1,  bg: "white",  kicker: "",            fig: "88",   unit: "%",
    caption: "de las organizaciones ya usa IA regularmente en al menos una función del negocio.",
    angle: "La IA ya no es novedad. La diferencia está en cómo la conectas al negocio.",
    source: "McKinsey" },

  { n: 2,  bg: "black",  kicker: "Solo cerca de", fig: "1/3", unit: "",
    caption: "de las empresas ha empezado a escalar sus programas de IA a nivel organizacional.",
    angle: "Muchos usan IA. Pocos la convierten en sistema.",
    source: "McKinsey" },

  { n: 3,  bg: "white",  kicker: "",            fig: "62",   unit: "%",
    caption: "de las organizaciones ya experimenta con agentes de IA: 23% los escala y 39% explora.",
    angle: "Los agentes ya entraron al juego. El reto es que no jueguen solos.",
    source: "McKinsey" },

  { n: 4,  bg: "black",  kicker: "No más del",  fig: "10",   unit: "%",
    caption: "de las empresas está escalando agentes de IA en funciones específicas.",
    angle: "Mucho discurso de agentes. Todavía poca implementación seria.",
    source: "McKinsey" },

  { n: 5,  bg: "yellow", kicker: "Más de",      fig: "2/3",  unit: "",
    caption: "de las empresas usa IA en más de una función — y la mitad, en tres o más.",
    angle: "La IA deja de ser herramienta cuando empieza a conectar áreas.",
    source: "McKinsey" },

  { n: 6,  bg: "black",  kicker: "Solo",        fig: "39",   unit: "%",
    caption: "reporta impacto de la IA en el EBIT a nivel empresa, y la mayoría lo cifra por debajo del 5%.",
    angle: "La IA sin proceso puede impresionar, pero no necesariamente mueve el negocio.",
    source: "McKinsey" },

  { n: 7,  bg: "black",  kicker: "",            fig: "51",   unit: "%",
    caption: "de las organizaciones que usa IA ya vio al menos una consecuencia negativa; casi un tercio, por inexactitud.",
    angle: "La IA sin criterio no es ventaja. Es riesgo con buena interfaz.",
    source: "McKinsey" },

  { n: 8,  bg: "black",  kicker: "Solo",        fig: "5",    unit: "%",
    caption: "de las empresas es considerada \u201Cfuture-built\u201D en IA; 35% la escala y 60% casi no captura valor.",
    angle: "El problema no es tener IA. Es saber convertirla en capacidad operativa.",
    source: "BCG" },

  { n: 9,  bg: "yellow", kicker: "",            fig: "5",    unit: "\u00D7",
    caption: "más de incremento de ingresos logran las empresas \u201Cfuture-built\u201D — y 3\u00D7 más reducción de costos.",
    angle: "La ventaja no está en el prompt. Está en el modelo operativo.",
    source: "BCG" },

  { n: 10, bg: "yellow", kicker: "Hacia 2028",  fig: "29",   unit: "%",
    caption: "del valor total de IA representarán los agentes; hoy ya rondan el 17%.",
    angle: "Los agentes no son moda: son una nueva capa de operación.",
    source: "BCG" },

  { n: 11, bg: "white",  kicker: "",            fig: "+50",  unit: "%",
    caption: "creció el acceso de los trabajadores a la IA durante 2025.",
    angle: "La adopción sube más rápido que la madurez de muchas empresas.",
    source: "Deloitte" },

  { n: 12, bg: "black",  kicker: "Solo",        fig: "34",   unit: "%",
    caption: "de las empresas está realmente reimaginando el negocio con IA.",
    angle: "Automatizar lo mismo de siempre no es transformación. Es maquillar el desorden.",
    source: "Deloitte" },

  { n: 13, bg: "black",  kicker: "Solo",        fig: "1/5",  unit: "",
    caption: "empresas tiene un modelo maduro de gobernanza para agentes autónomos.",
    angle: "Antes de soltar agentes, hay que definir límites, contexto y responsabilidad.",
    source: "Deloitte" },

  { n: 14, bg: "black",  kicker: "",            fig: "42",   unit: "%",
    caption: "de las empresas cree que su estrategia está lista para IA — pero menos en infraestructura, datos, riesgo y talento.",
    angle: "La estrategia suena bien hasta que toca conectarla con la operación.",
    source: "Deloitte" },

  { n: 15, bg: "white",  kicker: "",            fig: "82",   unit: "%",
    caption: "de los líderes ve este año como clave para repensar estrategia y operaciones; 81% integrará agentes en 12–18 meses.",
    angle: "El momento no es \u201Cprobar IA\u201D. Es rediseñar cómo trabaja la empresa.",
    source: "Microsoft Work Trend Index" },

  { n: 16, bg: "black",  kicker: "",            fig: "80",   unit: "%",
    caption: "de la fuerza laboral dice no tener tiempo ni energía para su trabajo, mientras 53% de líderes exige más productividad.",
    angle: "El cuello de botella no es la gente. Es el sistema donde trabaja la gente.",
    source: "Microsoft Work Trend Index" },

  { n: 17, bg: "black",  kicker: "",            fig: "275",  unit: "",
    caption: "interrupciones al día recibe cada empleado: una cada 2 minutos durante la jornada.",
    angle: "No necesitas más apps. Necesitas menos fricción.",
    source: "Microsoft Work Trend Index" },

  { n: 18, bg: "yellow", kicker: "",            fig: "46",   unit: "%",
    caption: "de los líderes dice que su empresa ya usa agentes para automatizar workflows completos.",
    angle: "La automatización ya no es \u201Crecordatorio y correo\u201D. Es flujo completo.",
    source: "Microsoft Work Trend Index" },

  { n: 19, bg: "white",  kicker: "La razón #1", fig: "42",   unit: "%",
    caption: "acude a la IA antes que a un colega por su disponibilidad 24/7; le siguen velocidad (30%) e ideas ilimitadas (28%).",
    angle: "La IA no reemplaza al humano. Cubre lo que el humano no debería cargar solo.",
    source: "Microsoft Work Trend Index" },

  { n: 20, bg: "white",  kicker: "",            fig: "52",   unit: "%",
    caption: "todavía ve la IA como herramienta de comandos; solo 46% la trata como \u201Csocio de pensamiento\u201D.",
    angle: "La diferencia está entre pedirle cosas a la IA y pensar con ella.",
    source: "Microsoft Work Trend Index" },

  { n: 21, bg: "yellow", kicker: "",            fig: "66",   unit: "%",
    caption: "de los usuarios de IA gana tiempo para trabajo de alto valor; 58% produce lo que no podía hace un año.",
    angle: "La IA bien usada no abarata el trabajo humano. Lo sube de nivel.",
    source: "Microsoft Work Trend Index 2026" },

  { n: 22, bg: "white",  kicker: "",            fig: "49",   unit: "%",
    caption: "de las conversaciones en Copilot apoyan trabajo cognitivo: análisis, decisiones y pensamiento creativo.",
    angle: "La IA ya no es solo \u201Cescríbeme un texto\u201D. Está entrando en decisiones.",
    source: "Microsoft Work Trend Index 2026" },

  { n: 23, bg: "white",  kicker: "",            fig: "15",   unit: "\u00D7",
    caption: "crecieron los agentes activos en Microsoft 365 año contra año; en grandes empresas, 18\u00D7.",
    angle: "La adopción de agentes se acelera. La pregunta es quién los gobierna.",
    source: "Microsoft Work Trend Index 2026" },

  { n: 24, bg: "yellow", kicker: "",            fig: "60",   unit: "%",
    caption: "de su semana dedican los vendedores a tareas que no son vender; solo 40% va a vender.",
    angle: "El problema comercial no suele ser falta de talento. Es exceso de fricción.",
    source: "Salesforce · State of Sales 2026" },

  { n: 25, bg: "white",  kicker: "",            fig: "69",   unit: "%",
    caption: "de los profesionales de ventas dice que el cliente exige más ROI medible; 67%, más personalización.",
    angle: "El cliente no quiere presión. Quiere claridad, contexto y seguimiento.",
    source: "Salesforce · State of Sales 2026" },

  { n: 26, bg: "yellow", kicker: "",            fig: "94",   unit: "%",
    caption: "de los líderes de ventas con agentes los considera críticos para responder a las demandas del negocio.",
    angle: "Los agentes no son adorno tecnológico. Son capacidad comercial.",
    source: "Salesforce · State of Sales 2026" },

  { n: 27, bg: "yellow", kicker: "",            fig: "90",   unit: "%",
    caption: "de los vendedores con agentes entiende mejor a sus clientes; 88% se acerca más a sus metas.",
    angle: "El agente correcto no reemplaza al vendedor. Le da memoria, contexto y velocidad.",
    source: "Salesforce · State of Sales 2026" },

  { n: 28, bg: "yellow", kicker: "",            fig: "73.3", unit: "%",
    caption: "de los consumidores prefiere la mensajería para hablar con negocios; 72.4% compra más a quien la ofrece.",
    angle: "WhatsApp no es un canal secundario. Para muchos clientes, es la puerta principal.",
    source: "WhatsApp Business · Kantar" },

  { n: 29, bg: "white",  kicker: "",            fig: "74.6", unit: "%",
    caption: "de los consumidores confía más en un negocio si puede escribirle; 66.8% se frustra si no puede.",
    angle: "La confianza también se construye respondiendo donde el cliente ya conversa.",
    source: "WhatsApp Business · Kantar" },

  { n: 30, bg: "black",  kicker: "",            fig: "82",   unit: "%",
    caption: "de los líderes de soporte invirtió en IA este año; 87% lo hará en 2026, pero solo 10% llegó a un despliegue maduro.",
    angle: "Todos quieren IA en atención. Pocos tienen el proceso listo para que funcione.",
    source: "Intercom · 2026" },
];
