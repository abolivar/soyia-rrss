# -*- coding: utf-8 -*-
"""
Generador del calendario editorial SoyIA (Instagram + Facebook).
Reconstruido sobre el ARTE REAL del directorio (5 series, 130 posts):

  Biblioteca (libros)     30 · 1 imagen   · libro-NN.png       <- biblioteca/
  Términos (diccionario)  30 · 1 imagen   · termino-NN.png     <- terminos/
  Datos (cifras)          30 · 1 imagen   · dato-NN.png        <- datos/  (data.jsx)
  Mitos                   10 · carrusel 8 · mito-NN-slide-K    <- mitos/
  Casos por vertical      30 · carrusel 3 · caso-NN-slide-K    <- Carruseles SoyIA PNG/

Salidas:
  - soyia-calendario-completo.csv   (130 posts · formato Social Planner · CRLF)
  - soyia-calendario-parte-1.csv    (90 posts — Social Planner importa máx. 90)
  - soyia-calendario-parte-2.csv    (40 posts)
  - soyia-guiones-carruseles.md
  - soyia-repo-manifiesto.md
"""

import csv
from datetime import date, timedelta

REPO = "https://raw.githubusercontent.com/abolivar/soyia-rrss/main/images"
FIXED_TAGS = "#SoyIA #CriterioPrimero"
PLACEHOLDER = "2050-01-01 00:00:00"  # no se usa: todas las fechas son reales

# ---------------------------------------------------------------------------
# 1. BIBLIOTECA (30) — Miércoles — "Biblioteca"  (título, autor, categoría, bajada)
# ---------------------------------------------------------------------------
LIBROS = [
    ("Co-Intelligence", "Ethan Mollick", "Negocios, tecnología e IA",
     "La IA no vale por parecer inteligente. Vale cuando te ayuda a pensar, decidir y actuar mejor."),
    ("The AI-Savvy Leader", "David De Cremer", "Liderazgo y estrategia de IA",
     "La IA no se delega “a la tecnología”. Se lidera, o se sufre."),
    ("Competing in the Age of AI", "Marco Iansiti y Karim R. Lakhani", "Estrategia y operación digital",
     "Las empresas que ganan no tienen más IA. Tienen mejor operación debajo."),
    ("All-In on AI", "Thomas H. Davenport y Nitin Mittal", "IA en estrategia y cultura",
     "Integrar IA no es comprar herramientas sueltas. Es rediseñar cómo trabaja la empresa."),
    ("The AI Advantage", "Thomas H. Davenport", "IA aplicada al negocio",
     "La ventaja no está en tener IA. Está en llevarla al proceso donde sí genera valor."),
    ("Working with AI", "Thomas H. Davenport y Steven M. Miller", "Colaboración humano-máquina",
     "La IA no reemplaza empleos. Reorganiza tareas. La diferencia importa."),
    ("Human + Machine", "Paul R. Daugherty y H. James Wilson", "Rediseño del trabajo con IA",
     "No se trata de poner IA encima. Se trata de rediseñar el proceso debajo."),
    ("Prediction Machines", "Ajay Agrawal, Joshua Gans y Avi Goldfarb", "La economía de la IA",
     "La IA baja el costo de predecir. El criterio decide dónde eso vale la pena."),
    ("Power and Prediction", "Ajay Agrawal, Joshua Gans y Avi Goldfarb", "La economía disruptiva de la IA",
     "Usar IA en tareas impresiona. Rediseñar tus decisiones es lo que cambia el negocio."),
    ("The AI-First Company", "Ash Fontana", "Empresas construidas desde los datos",
     "Antes de construir IA, hay que construir el dato que la alimenta."),
    ("The AI-Powered Enterprise", "Seth Earley", "Conocimiento estructurado y ontología",
     "La IA no ordena tu desorden. Lo amplifica. El orden es trabajo previo."),
    ("The AI-Centered Enterprise", "Ram Bala, Natarajan Balasubramanian y Amit Joshi", "Organizaciones rediseñadas con IA",
     "Añadir IA aislada no transforma nada. La operación se rediseña alrededor del contexto."),
    ("Generative AI in Practice", "Bernard Marr", "Casos de uso de IA generativa",
     "Los casos de uso inspiran. El criterio decide cuáles son tuyos."),
    ("Generative AI", "Tom Taulli", "Guía de IA generativa para tu negocio",
     "Entender la herramienta es el primer paso. Saber dónde aplicarla, el que cuenta."),
    ("HBR Guide to AI Basics for Managers", "Harvard Business Review", "Manual de IA para managers",
     "No necesitas programar IA. Necesitas saber qué pedirle y a quién."),
    ("Data Science for Business", "Foster Provost y Tom Fawcett", "Pensamiento analítico para negocio",
     "Antes de prometer IA seria, hace falta pensar con datos en serio."),
    ("Competing on Analytics", "Thomas H. Davenport y Jeanne G. Harris", "Cultura analítica y decisiones con datos",
     "Decidir con datos no es una moda nueva. Es la base que muchos todavía se saltan."),
    ("Designed for Digital", "Jeanne W. Ross, Cynthia M. Beath y Martin Mocker", "Arquitectura empresarial para lo digital",
     "La tecnología sin arquitectura se desordena caro. El diseño viene primero."),
    ("The Technology Fallacy", "Gerald C. Kane y otros", "Personas y transformación digital",
     "La transformación no es software. Es personas, procesos y criterio."),
    ("The Digital Transformation Playbook", "David L. Rogers", "Estrategia para la era digital",
     "Transformarse no es digitalizar lo de siempre. Es repensar para qué lo haces."),
    ("Machine, Platform, Crowd", "Andrew McAfee y Erik Brynjolfsson", "Plataformas y futuro digital",
     "La ventaja ya no está en una herramienta. Está en el sistema que la conecta."),
    ("Weapons of Math Destruction", "Cathy O’Neil", "Sesgo, algoritmos y datos",
     "Un algoritmo no es neutral solo porque venga vestido de matemática."),
    ("The Coming Wave", "Mustafa Suleyman y Michael Bhaskar", "Tecnología, poder y contención",
     "El poder de la IA obliga a algo incómodo: pensar antes de soltarla."),
    ("The Age of AI", "Henry Kissinger, Eric Schmidt y Daniel Huttenlocher", "IA, geopolítica y futuro humano",
     "La IA no es solo una herramienta de trabajo. Es una capa nueva de cómo decidimos."),
    ("AI Superpowers", "Kai-Fu Lee", "China, Silicon Valley y la nueva economía",
     "La carrera por la IA no es técnica. Es de poder, talento y contexto."),
    ("Human Compatible", "Stuart Russell", "Control y alineación de la IA",
     "El problema no es que la máquina sea inteligente. Es que optimice lo incorrecto muy bien."),
    ("The Alignment Problem", "Brian Christian", "Machine learning y valores humanos",
     "Enseñarle patrones a una máquina es fácil. Enseñarle qué valoras, no tanto."),
    ("The Ethical Algorithm", "Michael Kearns y Aaron Roth", "Diseño algorítmico responsable",
     "La responsabilidad no se programa al final. Se diseña desde el principio."),
    ("Unmasking AI", "Joy Buolamwini", "Sesgo, daño algorítmico y responsabilidad",
     "La IA hereda los sesgos de quien la construye. Por eso la mirada humana no es opcional."),
    ("Atlas of AI", "Kate Crawford", "Poder, política y costos reales de la IA",
     "La IA no vive en una nube mágica. Consume datos, energía, trabajo y decisiones."),
]

# ---------------------------------------------------------------------------
# 2. TÉRMINOS (30) — Lunes — "Términos"  (término, definición, cierre)
# ---------------------------------------------------------------------------
TERMINOS = [
    ("Modelo", "programa entrenado con muchos datos para reconocer patrones, predecir o asistir decisiones",
     "No necesitas saber cómo vive el modelo por dentro. Necesitas saber qué problema le estás pidiendo resolver."),
    ("Inteligencia artificial", "tecnología que hace tareas antes exclusivas de humanos: entender lenguaje, analizar, reconocer patrones y generar contenido",
     "La IA no es magia. Es capacidad aumentada cuando hay criterio detrás."),
    ("Prompt", "la instrucción que le das a una IA; puede ser una pregunta simple o una guía con tono, contexto y objetivo",
     "La IA responde mejor cuando tú piensas mejor lo que le pides."),
    ("Contexto", "toda la información que ayuda a una IA a entender qué pasa: quién eres, qué negocio tienes, qué quieres lograr y bajo qué reglas responder",
     "Sin contexto, la IA adivina. Con contexto, empieza a trabajar."),
    ("LLM", "Large Language Model: modelo entrenado con enormes cantidades de texto para entender y generar lenguaje; la base de asistentes como ChatGPT, Claude o Gemini",
     "Un LLM no es un oráculo. Es una herramienta poderosa que necesita dirección."),
    ("Token", "la unidad mínima con la que un modelo procesa texto: una palabra, parte de una palabra o un signo",
     "Para la IA, el lenguaje también tiene costo, peso y límite. Por eso el contexto importa."),
    ("Dataset", "conjunto de datos usado para entrenar, evaluar o alimentar un sistema de IA",
     "La IA aprende de datos. Si los datos son basura, el resultado viene con perfume, pero sigue siendo basura."),
    ("Entrenamiento", "proceso en el que un modelo aprende patrones a partir de muchos datos",
     "Entrenar una IA no es enseñarle valores. Es enseñarle patrones. Ahí empieza la responsabilidad humana."),
    ("Inferencia", "el momento en que la IA usa lo aprendido para responder, generar o sugerir una acción",
     "La inferencia es donde la IA deja de “aprender” y empieza a actuar. Conviene saber qué le estás pidiendo."),
    ("Multimodal", "que una IA puede trabajar con varios tipos de información a la vez: texto, imagen, audio, video o datos",
     "La próxima IA no solo leerá lo que dices. También entenderá lo que muestras, envías y haces."),
    ("Agente de IA", "IA diseñada para hacer más que responder: conversa, consulta información, sigue instrucciones y ejecuta tareas dentro de un proceso",
     "Un agente sin proceso es un empleado nuevo sin entrenamiento. Simpático, pero peligroso."),
    ("Automatización", "usar tecnología para que tareas repetitivas ocurran sin depender del tiempo de una persona: seguimientos, alertas, registros o respuestas",
     "Automatizar no es agotar humanidad. Es dejar de desperdiciarla en tareas que una máquina puede hacer mejor."),
    ("Workflow", "camino ordenado que sigue una tarea de principio a fin: pasos, responsables, condiciones y resultados esperados",
     "Si tu proceso vive solo en la cabeza de alguien, todavía no tienes proceso. Tienes fe."),
    ("CRM", "sistema donde se ordenan contactos, oportunidades, conversaciones, seguimientos y ventas; bien usado, es la memoria comercial de la empresa",
     "Un CRM no sirve por tener contactos guardados. Sirve cuando evita que las oportunidades se pierdan."),
    ("Pipeline", "vista del recorrido comercial: desde que alguien muestra interés hasta que compra, se enfría o necesita seguimiento",
     "El pipeline te muestra la verdad incómoda: dónde se está fugando el negocio."),
    ("Lead", "persona o empresa que mostró interés en lo que ofreces; puede venir de una campaña, una web, WhatsApp o una recomendación",
     "Un lead no es una venta. Es una conversación que puedes cuidar o desperdiciar."),
    ("Lead scoring", "forma de asignar prioridad a los prospectos según señales como interés, perfil, urgencia o presupuesto",
     "No todos los leads merecen la misma energía. El criterio también se automatiza."),
    ("RAG", "Retrieval-Augmented Generation: técnica que permite a la IA buscar información en tus documentos o datos propios antes de responder",
     "RAG es una forma elegante de decirle a la IA: responde con base, no con imaginación."),
    ("Embedding", "forma de convertir texto, imágenes o datos en representaciones numéricas para que la IA compare significados, no solo palabras",
     "Cuando la IA entiende similitud, deja de buscar palabras y empieza a encontrar intención."),
    ("Base vectorial", "base de datos diseñada para encontrar información parecida por significado; útil cuando quieres que una IA consulte tus documentos o conocimiento interno",
     "La información no sirve por estar guardada. Sirve cuando puedes encontrarla en el momento correcto."),
    ("Fine-tuning", "ajustar un modelo ya existente con datos específicos para que responda mejor en un tema, estilo o tarea concreta",
     "No todo se arregla con fine-tuning. A veces lo que falta no es más IA, sino mejor proceso."),
    ("API", "Application Programming Interface: puente que permite que dos sistemas se comuniquen y se envíen información",
     "La automatización empieza cuando las herramientas dejan de vivir como islas."),
    ("Guardrails", "reglas, límites y controles que ayudan a una IA a no salirse del tono, el objetivo, la información permitida o su responsabilidad",
     "Darle IA a un negocio sin límites es como darle llaves a alguien que no sabe dónde queda la casa."),
    ("Human-in-the-loop", "diseño donde la IA ayuda, pero una persona valida, supervisa o decide en los momentos importantes",
     "La IA puede acelerar el trabajo. El humano debe seguir cuidando el significado."),
    ("Alucinación", "cuando una IA inventa información o responde algo falso con mucha seguridad",
     "La IA también se equivoca. La diferencia es que a veces lo hace con una confianza admirablemente peligrosa."),
    ("Copiloto", "IA que acompaña a una persona en su trabajo: redacta, resume, analiza o sugiere, pero no debería operar sin dirección",
     "Un copiloto no reemplaza al piloto. Pero un buen piloto sí aprende a usarlo."),
    ("Claude", "familia de modelos de IA conversacional (de Anthropic) útil para analizar documentos, escribir, razonar y trabajar con contexto amplio",
     "Claude no es “mejor” por nombre. Es útil cuando el trabajo exige lectura, criterio y profundidad."),
    ("ChatGPT", "asistente de IA conversacional (de OpenAI) que responde preguntas, crea textos, analiza información y apoya tareas de trabajo",
     "ChatGPT no reemplaza tu pensamiento. Lo revela: si preguntas mal, responde bonito y flojo."),
    ("Gemini", "familia de modelos de IA (de Google DeepMind) pensada para trabajar con distintos formatos: texto, imagen, código, audio y video",
     "La IA multimodal importa porque el trabajo real no vive solo en texto. Vive en imágenes, llamadas, datos y conversaciones."),
    ("Llama", "familia de modelos de lenguaje abiertos (de Meta) usada para construir soluciones de IA más personalizadas o controladas",
     "No todo tiene que vivir en una app cerrada. A veces la ventaja está en construir sobre modelos abiertos."),
]

# ---------------------------------------------------------------------------
# 3. DATOS (30) — Martes — "Datos IA"  (de datos/data.jsx → dato-NN.png)
#    (línea de cifra, ángulo editorial, fuente)
# ---------------------------------------------------------------------------
DATOS = [
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
# 4. MITOS (10) — Viernes (carrusel 8 slides) — "Mitos IA"
#    Arte ya diseñado (mitos/). (gancho slide 1, línea de desarrollo para caption)
# ---------------------------------------------------------------------------
MITOS = [
    ("Le pusiste IA a tu negocio. Y todo sigue igual de roto.",
     "La IA amplifica lo que ya existe: orden o caos. Sin proceso debajo, automatizas el desorden y lo haces más rápido."),
    ("La IA no vino a reemplazar a tu equipo. Vino a devolverle el tiempo.",
     "Saca a tu gente de la tarea repetitiva y déjala donde se necesita criterio. Eso no es reemplazar. Es liberar."),
    ("Cuatro herramientas de IA. Y sigues sin saber qué pasó con ese lead.",
     "No necesitas más apps. Necesitas un proceso que conecte lo que ya tienes. La herramienta no es la estrategia."),
    ("La IA no es un lujo de empresas grandes. Es cosa de orden.",
     "La IA no pregunta cuántos empleados tienes. Pregunta si tu proceso está claro. Una pyme ordenada le saca más provecho que una corporación caótica."),
    ("La IA no es objetiva. Aprendió de tus datos.",
     "Si los datos vienen sesgados o sucios, la IA repite el sesgo con seguridad. La objetividad no viene en el modelo: viene del criterio con que lo alimentas."),
    ("Implementar IA no es un proyecto de tecnología. Es una decisión de negocio.",
     "La pregunta no es qué herramienta comprar. Es qué proceso quieres mejorar y por qué. Primero el criterio, después la herramienta."),
    ("Pusiste un chatbot. No tienes IA. Tienes un contestador caro.",
     "Un bot sin contexto ni proceso responde rápido y mal. La diferencia entre un contestador y un agente es el criterio detrás."),
    ("La IA no da resultados inmediatos. Da velocidad.",
     "Velocidad sobre un proceso bueno acelera resultados. Sobre un proceso roto, acelera el problema. Ordena primero."),
    ("Automatizaste todo lo que pudiste. Y ya no sabes qué está pasando.",
     "Automatizar sin visibilidad no es control: es perder el rastro más rápido. El sistema tiene que mostrarte dónde está cada cosa."),
    ("La IA no es un tren que se va. Es una decisión que se piensa.",
     "El miedo a “quedarse atrás” empuja a comprar sin criterio. Mejor entrar tarde y ordenado que temprano y a ciegas."),
]

# ---------------------------------------------------------------------------
# 5. CASOS POR VERTICAL (30) — Jueves (carrusel 3 slides) — "Casos por vertical"
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
# Hashtags variables por serie
# ---------------------------------------------------------------------------
VAR = {
    "libro":   "#BibliotecaSoyIA #LecturasDeIA #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #LiderazgoYDatos",
    "termino": "#DiccionarioIA #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #AprenderIA #ProcesoPrimero",
    "dato":    "#DatosDeIA #IAaplicada #AutomatizacionConCriterio #PymesPanama #NegociosLATAM #TransformacionDigital #ProductividadConCriterio",
    "mito":    "#MitosDeIA #AutomatizacionConCriterio #IAparaPymes #PymesPanama #NegociosLATAM #AutomatizacionSinHumo #IAaplicada",
}


def cap(body, variable):
    return body + "\n\n" + FIXED_TAGS + " " + variable


def img(name):
    return REPO + "/" + name


def carousel(prefix, n):
    return ", ".join(img(f"{prefix}-slide-{i}.png") for i in range(1, n + 1))


# ---------------------------------------------------------------------------
# Construir los pools de filas por serie
# ---------------------------------------------------------------------------
termino_rows = []
for i, (term, defi, closing) in enumerate(TERMINOS, 1):
    defi_cap = defi[0].upper() + defi[1:]
    body = f"{term}: {defi_cap}.\n\n{closing}"
    termino_rows.append(dict(content=cap(body, VAR["termino"]), images=img(f"termino-{i:02d}.png"),
                             tags="soyia,termino,diccionario", category="Términos", kind="Término"))

dato_rows = []
for i, (line, ang, src) in enumerate(DATOS, 1):
    body = f"{line}\n\n{ang}\n\n[FUENTE: {src}]"
    dato_rows.append(dict(content=cap(body, VAR["dato"]), images=img(f"dato-{i:02d}.png"),
                          tags="soyia,dato,cifra", category="Datos IA", kind="Dato"))

libro_rows = []
for i, (title, author, catl, take) in enumerate(LIBROS, 1):
    body = f"{take}\n\nEn la Biblioteca SoyIA: «{title}», de {author}. {catl}."
    libro_rows.append(dict(content=cap(body, VAR["libro"]), images=img(f"libro-{i:02d}.png"),
                           tags="soyia,biblioteca,libro", category="Biblioteca", kind="Libro"))

caso_rows = []
for i, c in enumerate(CASOS, 1):
    variable = c["hashtags"] + " #AutomatizacionConCriterio #SeguimientoComercial #PymesPanama #NegociosLATAM #IAaplicada"
    caso_rows.append(dict(content=cap(c["caption"], variable), images=carousel(f"caso-{i:02d}", 3),
                          tags=f"soyia,carrusel,{c['vertical']}", category="Casos por vertical",
                          kind="Caso", idx=i, vertical=c["vertical"], slides=[c["s1"], c["s2"], c["s3"]]))

mito_rows = []
for i, (hook, dev) in enumerate(MITOS, 1):
    body = f"{hook}\n\n{dev}\n\nCarrusel. Deslízalo."
    mito_rows.append(dict(content=cap(body, VAR["mito"]), images=carousel(f"mito-{i:02d}", 8),
                          tags="soyia,carrusel,mito", category="Mitos IA", kind="Mito", idx=i, hook=hook))

# ---------------------------------------------------------------------------
# Calendario · 30 semanas · arranca lunes 2026-06-08 · todas las fechas reales
#   Lun Término · Mar Dato · Mié Libro · Jue Caso · Vie Mito (cada 3 semanas)
# ---------------------------------------------------------------------------
START = date(2026, 6, 8)  # lunes
TIMES = {0: "08:30:00", 1: "11:30:00", 2: "08:30:00", 3: "11:30:00", 4: "12:00:00"}
WEEKS = 30
MITO_EVERY = 3  # mito en el viernes de las semanas 3, 6, 9, ... 30


def date_for(week, weekday):
    d = START + timedelta(days=(week - 1) * 7 + weekday)
    return f"{d.isoformat()} {TIMES[weekday]}"


schedule = []  # (postAt, row)
for week in range(1, WEEKS + 1):
    schedule.append((date_for(week, 0), termino_rows[week - 1]))
    schedule.append((date_for(week, 1), dato_rows[week - 1]))
    schedule.append((date_for(week, 2), libro_rows[week - 1]))
    schedule.append((date_for(week, 3), caso_rows[week - 1]))
    if week % MITO_EVERY == 0:
        schedule.append((date_for(week, 4), mito_rows[week // MITO_EVERY - 1]))

assert len(schedule) == 130, f"Esperaba 130 filas, hay {len(schedule)}"

# ---------------------------------------------------------------------------
# Encabezados EXACTOS del sample (40 columnas)
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


def build_row(post_at, row):
    c = [""] * 40
    c[0] = post_at
    c[1] = row["content"]
    c[3] = row["images"]
    c[7] = "TRUE"
    c[8] = "FALSE"
    c[9] = row["tags"]
    c[10] = row["category"]
    c[12] = "post"
    c[13] = "post"
    return c


def write_csv(fname, chunk):
    with open(fname, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER_1)
        w.writerow(HEADER_2)
        for post_at, row in chunk:
            w.writerow(build_row(post_at, row))


write_csv("soyia-calendario-completo.csv", schedule)
SPLIT = 90  # Social Planner importa máx. 90 por archivo
write_csv("soyia-calendario-parte-1.csv", schedule[:SPLIT])
write_csv("soyia-calendario-parte-2.csv", schedule[SPLIT:])

# ---------------------------------------------------------------------------
# Guiones de carruseles (.md) — Casos (3 slides, texto) + Mitos (8 slides, arte ya hecho)
# ---------------------------------------------------------------------------
with open("soyia-guiones-carruseles.md", "w", encoding="utf-8") as f:
    f.write("# Guiones de carruseles · SoyIA\n\n")
    f.write("El **caption** completo (con hashtags) vive en el CSV. Aquí, el contenido visual.\n\n")
    f.write("- **Casos** (30): 3 slides — Dolor → Solución → ADN.\n")
    f.write("- **Mitos** (10): 8 slides — **arte ya diseñado** en `mitos/`. Se incluye el gancho del slide 1 como referencia.\n\n")
    f.write("---\n\n## Casos por vertical (30)\n\n")
    roles = ["Slide 1 · Dolor", "Slide 2 · Solución", "Slide 3 · ADN"]
    for i, c in enumerate(CASOS, 1):
        f.write(f"### caso-{i:02d} · {c['vertical']}\n\n")
        for para in c["caption"].split("\n\n"):
            f.write(f"> {para}\n>\n")
        f.write("\n")
        for j, (role, text) in enumerate(zip(roles, [c["s1"], c["s2"], c["s3"]]), 1):
            f.write(f"- **{role}** (`caso-{i:02d}-slide-{j}.png`): {text}\n")
        f.write("\n")
    f.write("---\n\n## Mitos (10) — carrusel de 8 slides (arte existente)\n\n")
    for i, (hook, dev) in enumerate(MITOS, 1):
        f.write(f"### mito-{i:02d} (`mito-{i:02d}-slide-1.png` … `mito-{i:02d}-slide-8.png`)\n\n")
        f.write(f"- **Slide 1 · Gancho:** {hook}\n")
        f.write(f"- **Caption (resumen):** {dev}\n\n")

# ---------------------------------------------------------------------------
# Manifiesto del repo (.md)
# ---------------------------------------------------------------------------
def names_all():
    out = []
    out += [f"libro-{i:02d}.png" for i in range(1, 31)]
    out += [f"termino-{i:02d}.png" for i in range(1, 31)]
    out += [f"dato-{i:02d}.png" for i in range(1, 31)]
    for i in range(1, 11):
        out += [f"mito-{i:02d}-slide-{s}.png" for s in range(1, 9)]
    for i in range(1, 31):
        out += [f"caso-{i:02d}-slide-{s}.png" for s in range(1, 4)]
    return out


all_imgs = names_all()
with open("soyia-repo-manifiesto.md", "w", encoding="utf-8") as f:
    f.write("# Manifiesto del repositorio de imágenes · SoyIA\n\n")
    f.write(f"Total: **{len(all_imgs)} imágenes** en `images/` — todas ya subidas y servidas en\n")
    f.write(f"`{REPO}/<nombre>`.\n\n")
    f.write("| Serie | Origen | Convención | Cant. |\n|---|---|---|---|\n")
    f.write("| Biblioteca | `biblioteca/biblioteca_NN.png` | `libro-01..30.png` | 30 |\n")
    f.write("| Términos | `terminos/NN-termino.png` | `termino-01..30.png` | 30 |\n")
    f.write("| Datos | `datos/NN-dato.png` | `dato-01..30.png` | 30 |\n")
    f.write("| Mitos | `mitos/Mito NN PNG/SoyIA_MitoNN_0K.png` | `mito-NN-slide-1..8.png` | 80 |\n")
    f.write("| Casos | `Carruseles SoyIA PNG/NN-*/{1-dolor,2-solucion,3-adn}.png` | `caso-NN-slide-1..3.png` | 90 |\n")
    f.write(f"| **Total** | | | **{len(all_imgs)}** |\n\n")
    f.write("Lista completa de archivos:\n\n")
    for n in all_imgs:
        f.write(f"- `{n}`\n")

# ---------------------------------------------------------------------------
# Resumen
# ---------------------------------------------------------------------------
from collections import Counter
by = Counter(r["category"] for _, r in schedule)
print(f"Posts: {len(schedule)} | imágenes: {len(all_imgs)}")
for k, v in by.items():
    print(f"  {k}: {v}")
print(f"Fechas: {schedule[0][0]} → {schedule[-1][0]}")
print(f"parte-1: {len(schedule[:SPLIT])} ({schedule[0][0]} → {schedule[SPLIT-1][0]})")
print(f"parte-2: {len(schedule[SPLIT:])} ({schedule[SPLIT][0]} → {schedule[-1][0]})")
print("Generados: completo, parte-1, parte-2, guiones, manifiesto")
