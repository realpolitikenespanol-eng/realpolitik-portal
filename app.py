import streamlit as st
import os
import json
import time
from urllib.parse import quote
from google import genai
from google.genai import types

# =========================================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================================
st.set_page_config(
    page_title="REALPOLITIK",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================================
# GESTIÓN DE BASE DE DATOS LOCAL
# =========================================================================
DB_FILE = "articulos.json"

ARTICULOS_SEMILLA = {
    "Art_Petrodolar": {
        "titulo": "La Trampa del Petrodólar y las Reservas del BRICS+",
        "fecha": "MAYO 2026",
        "categoria": "Geopolítica Monetaria & Mercados",
        "sinopsis": "Un análisis profundo sobre los flujos de liquidez global, los mecanismos de compensación alternativos y la fragmentación estratégica de las reservas de los bancos centrales en el contexto de un sistema multilateral en transición.",
        "imagen": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop",
        "contenido": "Aquí se desarrollará el cuerpo completo del ensayo analítico sobre la geopolítica del petrodólar, desglosando los agregados monetarios y los vectores de diversificación de los bancos centrales."
    },
    "Art_BrettonWoods": {
        "titulo": "El U.S. Dollar: Cómo el Greenback Conquistó el Mundo",
        "fecha": "MAYO 2026",
        "categoria": "Geopolítica Monetaria & Mercados",
        "sinopsis": "Análisis estructural sobre la transición del poder financiero global en 1944. La capitulación de la libra esterlina ante el peso aplastante del modelo oro-dólar de Harry Dexter White.",
        "imagen": "https://live.staticflickr.com/5030/5856660723_ef2b89a8e6_b.jpg",
        "datos_grafica": "Año,Reservas de Oro de EE.UU. (Toneladas)\n1944,18000\n1950,20200\n1955,19500\n1960,15800\n1965,12100\n1970,9800\n1971,9000",
        "contenido": "El Omni Washington de Bretton Woods puede verse como otro hotel lujoso en el campo estadounidense para el visitante común.\n\nSin embargo, este complejo hostelero representa en gran manera el inicio de la dominancia geoeconómica actual de los Estados Unidos. En 1944, las principales Potencias Aliadas de la Segunda Guerra Mundial, junto al bloque soviético, se reunieron en este pomposo edificio ubicado en las faldas del Monte Washington para negociar qué tipo de sistema económico podría regir en el devastado mundo que quedó después del arrasador conflicto que estaba terminando en Europa y Asia. Los máximos representantes de la teoría económica moderna estaban presentes, entre ellos destacando John Maynard Keynes para el bando británico y Henry Dexter White por el lado estadounidense.\n\nMuchos verían esta reunión como una lucha entre el modelo soviético y el occidental, pero en este hotel no se fraguó una guerra entre comunistas y capitalistas, sino entre el dólar estadounidense y la libra esterlina. Desde 1920 la competencia entre la moneda británica y el dólar se volvió acérrima, con ambas representado el 97% de las reservas internacionales de todos los países del mundo (Eichengreen, Flandreau, 2008). A mediados de esa década el dólar oficialmente sobrepasó a la libra en las reservas internacionales del mundo, sin embargo, perdería brevemente su posición en la década de los años 30. No obstante, el Reino Unido se estancó — con mucho sentido — después de la Segunda Guerra Mundial. Sus deudas e industrias paralizadas, aunado a la falta de personal laboral adulto (el cual estaba desplegado en las fuerzas armadas) hicieron que el Reino Unido no pudiera enfocar sus esfuerzos en exportaciones, sino en la reconstrucción de su propia economía interna.\n\nEn este momento Estados Unidos toma la delantera otra vez. En Bretton Woods los dos ingenieros fundamentales de los acuerdos finales fueron Keynes y White, a quienes ya habíamos mencionado anteriormente. Por el lado de Keynes se proponía un sistema monetario internacional muy globalizado. Proponía la creación de la Unión Internacional de Compensación (UIC), un organismo internacional que emitiera una nueva moneda de reserva internacional llamada el \"Bancor\". Este medio de cambio sería usado para estabilizar el precio de las mercancías básicas (oro, petróleo, gas, etc.) con el del valor del medio internacional de intercambios y acumulación de riqueza. La UIC se encargaría de la creación del Bancor y de llevar el control del intercambio monetario asociado al comercio entre países. El mecanismo que proponía era el siguiente:\n\n* **La UIC emite determinada cantidad de Bancor** y las naciones fijan el valor de sus monedas a dicho medio de intercambio.\n* **El organismo se encarga de distribuir** una cantidad definida de Bancor a cada país.\n* **Cada nación que adopte el mecanismo** acepta llevar a cabo todo su comercio internacional por medio de esta moneda.\n* **Se incentivaría que cada país** mantenga sus reservas de Bancor cercanas a cero. Si una nación tiene un excedente de Bancor en su balanza de pagos, la UIC colocará una carga impositiva sobre dicho monto, colocando dichos fondos en una reserva de la institución.\n* **Si un país termina con una balanza de Bancor negativa**, se devaluará su moneda con relación al Bancor, para que los demás países se vean incentivados a adquirir más bienes desde dicha nación.\n* **De esta manera se centralizaba el poder de devaluación** en un solo organismo, pudiendo de dicha manera prevenir devaluaciones competitivas e incentivar al desarrollo comercial de todas las naciones involucradas.\n\nInicialmente parecía que todos estaban de acuerdo con este plan. Es más, Estados Unidos había llegado con una idea extremadamente similar: una moneda de reserva internacional llamada \"Unitas\". Sin embargo, el enviado de EE. UU, Harry White, cambió repentinamente de opinión en la conferencia. Se introdujo la idea de que no se creara ninguna moneda de reserva internacional novedosa, en cambio, el medio de cambio mundial sería el dólar estadounidense. El mecanismo sería el siguiente:\n\n* **Estados Unidos emite dólares** y las demás naciones lo adquieren.\n* **El valor del dólar** estaría fijado a 35$ por onza de oro.\n* **Las demás naciones fijarían su tasa de cambio** al dólar, el cual está respaldado por el oro como lo vimos anteriormente.\n* **Las naciones portadoras de dólares** tendrían derecho de canjear sus dólares por reservas de oro de los Estados Unidos.\n\nEl plan de White prevaleció. El proyecto de Keynes, incluso a simple vista, se ve más elaborado y justo, promoviendo el desarrollo integral de cada país del mundo con un ente central que los ayude a hacer sus exportaciones igual de atractivas que las de las mayores superpotencias. No obstante, toda propuesta utópica cambia cuando la ves con otros lentes. El modelo de Keynes se veía como un castigo a los países más exportadores (es decir, los más ricos e industrializados) ya que te dictaba qué debías hacer con tus ganancias comerciales, impidiendo que las reservaras en tu propia alcancía. Además, no tenía el enorme respaldo real en oro que tenía el dólar. Había que enfrentar la realidad: el único país que salió rico de la guerra fue Estados Unidos. Era la única potencia en guerra que no vio ninguna bomba caer sobre su territorio y terminó con una industria más grande, eficiente y avanzada al culminar el conflicto. Casi todos los países contaban con reservas en dólares y confiaban en el patrón oro que se les estaba proponiendo. Hay que recordar que en aquella época el dinero no era tan popular como ahora, ya que experiencias como la Gran Depresión de 1929 habían drenado la confianza del público en el papel moneda. Por esta misma razón resultaba tan popular que los países pudieran tener un respaldo en oro indirecto al acumular dólares en sus reservas.\n\n[GRAFICO_INTERACTIVO_RESERVAS]\n\nEl pacto se firmó. Se llegó a un punto medio entre las propuestas de Keynes y White. Aunque el mundo no alcanzó a ver una moneda internacional como el Bancor, si se logró la conformación del Fondo Monetario Internacional (FMI) como ente de supervisión, apoyo y acompañamiento económico mundial, apoyando a la estabilidad fiscal y monetaria de sus miembros. Asimismo, se consolidó la existencia del Banco Mundial, como un ente asociado al FMI que ayudase con el financiamiento de la reconstrucción de Europa y posteriormente para asegurar el pleno empleo y desarrollo económico de sus integrantes.\n\nBretton Woods fue el comienzo de la hegemonía geoeconómica de EE.UU. A pesar de ello, este pacto no fue permanente. En 1971 Estados Unidos estaba en crisis. El mundo tenía 50.000 millones de dólares en forma de efectivo, mientras que EE.UU. tenía únicamente 10.000 millones de oro en sus reservas. Sencillamente no podían respaldar la cantidad de dólares que había en el mundo. Y la situación estaba empeorando. La guerra de Vietnam estaba siendo brutalmente costosa, y para poder financiarla, EE.UU. debía de emitir muchos más dólares para poder cubrir los gastos. Esto, aunado a los costos de los recientes programas Medicare y Medicaid creados bajo el mandato de Lyndon B. Johnson, generó un aumento estratosférico de la inflación por la excesiva oferta de dólares.\n\nJustamente en esa misma época, los países europeos y Japón estaban experimentando booms económicos e industriales, por lo que ya no eran excesivamente dependientes de las exportaciones de Estados Unidos, en cambio, empezaron a inundar el propio mercado de los americanos. Los productores estadounidenses, además, estaban perdiendo competitividad en los mercados internacionales debido a que sus costos de producción se mantenían elevados debido a su propia inflación interna. Pero el velo no cayó por completo hasta que el Reino Unido, percatándose de la evidente incapacidad de Estados Unidos de respaldar todo su papel moneda con oro, decidió canjear 3.000 millones de dólares por oro de la reserva federal. En este contexto, Nixon enfrentaba dos opciones, o dejaba que Estados Unidos avanzara hacia el colapso económico, asegurándose perder las elecciones de 1972, o usar el poder comercial de EE.UU. para obligar al mundo a negociar un acuerdo que salvase a los norteamericanos de un desastre mayor. Nixon, lógicamente, se decidió por la segunda opción.\n\nEn Camp David, la casa de campo privada del presidente se reunió con su equipo de asesores económicos de mayor confianza. Allí decidieron dar un shock repentino al mundo. Anunció el cese inmediato de la libre convertibilidad del dólar con el oro y aranceles de 10%, forzando así a los países a revaluar sus monedas, devaluando temporalmente el atractivo de las exportaciones del resto del mundo mientras se forzaba a todos los aliados importantes de EE.UU. a negociar un acuerdo más justo para ellos. Este evento se llamó el Nixon Shock y, en la práctica, fue el fin del acuerdo Bretton Woods.\n\nSin embargo, esto no resolvió el problema estructural de la moneda estadounidense, en cambio, fue más un parche temporal para evitar una corrida de oro de las reservas federal. Los países empezaron a desconfiar del dólar, y poco a poco este iba perdiendo su valor, ya que no había una razón tan fuerte — como lo era el respaldo en oro — para mantenerla como reserva internacional. Para esto, Henry Kissinger tenía un plan. El asesor de Seguridad Nacional y secretario de Estado se percató en 1974 de que el oro ya no era el bien básico más demandado del mundo como lo era en los 1700´s, en cambio era uno que literalmente, movía al mundo: el petróleo. En secreto, Kissinger viaja a Arabia Saudita (el mayor exportador de crudo de la OPEP) con una oferta: tranza todas tus transacciones petroleras en dólares estadounidenses y a cambio, recibe la bendición de los Estados Unidos, así como su perpetua protección militar y económica en Medio Oriente. El apretón de manos fue inmediato: nació el petrodólar.\n\nEl anuncio de Arabia Saudita de que ahora todo su petróleo se negociaría en dólares significó que ahora el mundo entero tendría que volver a demandar dólares para suplir a sus países de energía. Nuevamente el valor del dólar se disparó y con él, su posición como hegemón económico mundial fue cimentada. Este sistema todavía rige hoy en día, aunque aún más solidificado ya que el mercado de deuda de Estados Unidos ha hecho que no haya una opción más rentable, líquida y estable que el dólar para mantener los ahorros internacionales de los países del mundo entero.\n\nEstados Unidos no tiene ninguna razón para abandonar este sistema pronto. Su existencia le ha otorgado un poder absoluto en términos económicos y comerciales. Cada vez que un país del mundo decide tomar un camino geopolítico opuesto a los estadounidenses, estos pueden cortarles efectivamente su suministro de dólares, y con él, su acceso a los mercados globales. Han existido propuestas de alternativa al dólar como reserva mundial, algunos abogan por una moneda conjunta del bloque de los BRICS, otros reviven la idea del Bancor de Keynes, sin embargo, la realidad inmediata es que ningún país del mundo tiene la capacidad de otorgar la misma predictibilidad, estabilidad y rentabilidad monetaria que los Estados Unidos. Solo el tiempo dictará si algún día la hegemonía del dólar acabará. Por ahora, hay que adaptarse a ella para no ser excluido del juego económico global."
    }
}

def cargar_articulos():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(ARTICULOS_SEMILLA, f, ensure_ascii=False, indent=4)
        return ARTICULOS_SEMILLA
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return ARTICULOS_SEMILLA

def guardar_articulos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

ARTICULOS_DB = cargar_articulos()

# =========================================================================
# FUNCIONES AUXILIARES — IA (Gemini)
# =========================================================================
def _get_api_key():
    return st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")

def generar_briefing_diario(api_key):
    """Genera contexto actual + sucesos de la semana + hotspots geopolíticos del día.
    Devuelve (contexto, semana, lista_paises) o lanza excepción."""
    client = genai.Client(api_key=api_key)
    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    resp_contexto = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Resume en un párrafo denso (máx. 120 palabras) el contexto geopolítico, geoeconómico y político global ACTUAL. Tono frío, analítico y objetivo, como un brief de inteligencia. No uses títulos ni listas, solo prosa corrida.",
        config=types.GenerateContentConfig(tools=[grounding_tool], temperature=0.3)
    )
    contexto = resp_contexto.text.strip()

    resp_semana = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Resume en un párrafo denso (máx. 120 palabras) los acontecimientos geopolíticos, geoeconómicos y políticos más relevantes de ESTA SEMANA a nivel global. Tono frío, analítico y objetivo, como un brief de inteligencia. No uses títulos ni listas, solo prosa corrida.",
        config=types.GenerateContentConfig(tools=[grounding_tool], temperature=0.3)
    )
    semana = resp_semana.text.strip()

    resp_hotspots = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="¿Cuáles son los 4 a 7 países que hoy representan los principales focos de tensión o relevancia geopolítica, geoeconómica o política a nivel mundial? Responde ÚNICAMENTE con sus nombres en inglés, separados por coma, sin explicaciones ni texto adicional. Ejemplo de formato: United States, China, Russia, Ukraine",
        config=types.GenerateContentConfig(tools=[grounding_tool], temperature=0.2)
    )
    paises_raw = resp_hotspots.text.strip()
    hotspots = [p.strip() for p in paises_raw.split(",") if p.strip()]

    return contexto, semana, hotspots

def generar_briefing_pais(api_key, pais_nombre):
    """Genera un mini-briefing específico de un país."""
    client = genai.Client(api_key=api_key)
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Genera un briefing breve (máx. 70 palabras) sobre la situación geopolítica, geoeconómica y política ACTUAL de {pais_nombre}. Tono frío, analítico y objetivo. Solo prosa corrida, sin títulos.",
        config=types.GenerateContentConfig(tools=[grounding_tool], temperature=0.3)
    )
    return resp.text.strip()

def render_texto_tipeo(texto, contenedor_css_class="rp-intel-body", velocidad_ms=12, altura=None, key=""):
    """Renderiza texto con efecto de tipeo (typewriter) usando un componente HTML.
    El texto llega completo desde Gemini; el efecto es puramente visual del lado del cliente."""
    texto_escapado = json.dumps(texto)
    altura_css = f"height:{altura}px; overflow-y:auto;" if altura else ""
    html_tipeo = f"""
<div id="typewrap-{key}" class="{contenedor_css_class}" style="{altura_css} font-family:'Inter',sans-serif;"></div>
<style>
  body {{ margin:0; padding:0; background: transparent; }}
  .{contenedor_css_class} {{
    font-size: 0.88rem;
    color: #B0AEA9;
    line-height: 1.75;
  }}
</style>
<script>
const fullText_{key} = {texto_escapado};
const el_{key} = document.getElementById('typewrap-{key}');
let i_{key} = 0;
function typeNext_{key}() {{
  if (i_{key} <= fullText_{key}.length) {{
    el_{key}.innerHTML = fullText_{key}.substring(0, i_{key}) + '<span class="rp-typing-cursor"></span>';
    i_{key}++;
    setTimeout(typeNext_{key}, {velocidad_ms});
  }} else {{
    el_{key}.innerHTML = fullText_{key};
  }}
}}
typeNext_{key}();
</script>
<style>
.rp-typing-cursor {{
    display: inline-block;
    width: 6px;
    height: 0.95em;
    background: #C8A96E;
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blink-cursor 0.9s step-end infinite;
}}
@keyframes blink-cursor {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
</style>
"""
    n_chars = max(len(texto), 1)
    altura_calc = altura if altura else min(400, max(80, int(n_chars * 0.45) + 40))
    st.components.v1.html(html_tipeo, height=altura_calc, scrolling=bool(altura))

# =========================================================================
# CONTROL DE ESTADO DE NAVEGACIÓN
# =========================================================================
if "nav" in st.query_params:
    st.session_state.pagina_actual = st.query_params["nav"]
elif "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

if "editorial_autenticado" not in st.session_state:
    st.session_state.editorial_autenticado = False

if "historial_ia" not in st.session_state:
    st.session_state.historial_ia = []

if "globe_countries" not in st.session_state:
    st.session_state.globe_countries = []

if "filtro_articulos" not in st.session_state:
    st.session_state.filtro_articulos = "Todos los Reportes"

if "fuente_ia" not in st.session_state:
    st.session_state.fuente_ia = "Corpus + Web"

if "briefing_contexto" not in st.session_state:
    st.session_state.briefing_contexto = None

if "briefing_semana" not in st.session_state:
    st.session_state.briefing_semana = None

if "briefing_timestamp" not in st.session_state:
    st.session_state.briefing_timestamp = 0

if "hotspots_diarios" not in st.session_state:
    st.session_state.hotspots_diarios = []

if "foco_activo" not in st.session_state:
    # "hotspots" = focos del briefing diario, "consulta" = focos de la última pregunta del usuario
    st.session_state.foco_activo = "hotspots"

if "pais_tooltip_cache" not in st.session_state:
    st.session_state.pais_tooltip_cache = {}

if "pais_click_pendiente" in st.query_params:
    st.session_state["_pais_click_pendiente"] = st.query_params["pais_click_pendiente"]
    del st.query_params["pais_click_pendiente"]

CACHE_BRIEFING_SEGUNDOS = 3600  # 1 hora

if "briefing_auto_generado" not in st.session_state:
    st.session_state.briefing_auto_generado = False

if "hotspots_dia" not in st.session_state:
    st.session_state.hotspots_dia = []

if "modo_hotspots" not in st.session_state:
    # "dia" = mostrando hotspots automáticos del día | "consulta" = mostrando países de la última consulta
    st.session_state.modo_hotspots = "dia"

if "pais_briefings_cache" not in st.session_state:
    st.session_state.pais_briefings_cache = {}

if "pais_seleccionado" not in st.session_state:
    st.session_state.pais_seleccionado = None

# Si llega un click de país desde el globo (query param)
if "pais_click" in st.query_params:
    st.session_state.pais_seleccionado = st.query_params["pais_click"]
    del st.query_params["pais_click"]

# Si llega una solicitud de filtro vía query param (desde las tarjetas de Inicio)
if "filtro" in st.query_params:
    st.session_state.filtro_articulos = st.query_params["filtro"]
    del st.query_params["filtro"]


# =========================================================================
# UTILIDAD: ANIMACIÓN DE TIPEO PARA TEXTOS GENERADOS POR IA
# =========================================================================
def render_texto_animado(texto, contenedor_class="rp-intel-body", velocidad_ms=10, altura=None):
    """Renderiza un bloque de texto con efecto de tipeo estilo chatbot, vía componente HTML."""
    texto_json = json.dumps(texto)
    h = altura if altura else (max(90, min(260, 28 + len(texto) // 3)))
    html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; }}
  #txt {{
    font-family:'Inter',sans-serif;
    font-size:0.88rem;
    line-height:1.75;
    color:#B0AEA9;
  }}
  #txt strong {{ color:#C8A96E; font-weight:600; }}
  .cursor {{
    display:inline-block;
    width:6px; height:1em;
    background:#C8A96E;
    margin-left:2px;
    vertical-align:text-bottom;
    animation: blink 0.9s step-end infinite;
  }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
</style>
</head>
<body>
<div id="txt"></div>
<script>
const fullText = {texto_json};
const el = document.getElementById('txt');
let i = 0;
const speed = {velocidad_ms};
function tick() {{
  if (i <= fullText.length) {{
    el.innerHTML = fullText.slice(0, i).replace(/\\n/g, '<br>') + '<span class="cursor"></span>';
    i += 2;
    setTimeout(tick, speed);
  }} else {{
    el.innerHTML = fullText.replace(/\\n/g, '<br>');
  }}
}}
tick();
</script>
</body>
</html>
"""
    st.components.v1.html(html_code, height=h)


# =========================================================================
# SISTEMA DE DISEÑO — REALPOLITIK v3
# Paleta: Fondo abismal · Ámbar diplomático · Pergamino frío
# =========================================================================

pagina = st.session_state.pagina_actual

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ── */
[data-testid="stToolbar"], footer, [data-testid="stDecoration"],
[data-testid="stSidebarNav"], [data-testid="collapsedControl"] {{
    visibility: hidden !important;
    display: none !important;
}}
[data-testid="stSidebar"] {{ display: none !important; }}

.stApp {{
    background-color: #080A0F !important;
    color: #E8E6E1;
}}
[data-testid="stHeader"] {{ background-color: transparent !important; }}
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    padding-left: 3.5rem !important;
    padding-right: 3.5rem !important;
    max-width: 1180px !important;
    margin: 0 auto !important;
}}
/* El hero y el masthead necesitan escapar del padding del block-container para ser full-bleed */
.rp-masthead-wrap, .rp-hero {{
    margin-left: calc(-1 * (50vw - 50%)) !important;
    width: 100vw !important;
    max-width: 100vw !important;
}}
.rp-content {{
    max-width: 100%;
}}

html, body, p, li, span {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 400;
    line-height: 1.7;
    color: #E8E6E1;
}}

/* ── MASTHEAD ── */
.rp-masthead {{
    max-width: 1180px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.8rem 3.5rem 1.2rem 3.5rem;
    border-bottom: 1px solid #1A1F2E;
}}
.rp-wordmark {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    color: #E8E6E1 !important;
    text-decoration: none !important;
}}
.rp-wordmark:hover {{ color: #C8A96E !important; }}

/* ── BARRA DE NAVEGACIÓN ── */
.rp-nav {{
    display: flex;
    gap: 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}}
.rp-nav::-webkit-scrollbar {{ display: none; }}
.rp-nav-link {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B7280 !important;
    text-decoration: none !important;
    padding: 0.5rem 1.1rem;
    border-radius: 3px;
    transition: color 0.2s ease, background 0.2s ease;
    white-space: nowrap;
    display: inline-block;
}}
.rp-nav-link:hover {{ color: #E8E6E1 !important; }}
.rp-nav-link.activo {{
    color: #C8A96E !important;
    background: rgba(200,169,110,0.08);
}}

/* ── ETIQUETA DE SECCIÓN ── */
.rp-seccion-label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem;
    color: #4A5568;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    display: block;
}}
.rp-seccion-title {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 3rem;
    font-weight: 400;
    color: #E8E6E1;
    line-height: 1.1;
    margin-top: 0;
    margin-bottom: 2.5rem;
}}

/* ── HERO FULL-BLEED ── */
.rp-hero {{
    position: relative;
    width: 100vw;
    margin-left: 50%;
    transform: translateX(0%);
    min-height: 88vh;
    background-image:
        linear-gradient(to bottom, rgba(8,10,15,0.25) 0%, rgba(8,10,15,0.55) 55%, rgba(8,10,15,1) 100%),
        url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1800&auto=format&fit=crop');
    background-size: cover;
    background-position: center 40%;
    background-attachment: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 3rem 1.5rem;
    overflow: hidden;
}}
.rp-hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #C8A96E;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}
.rp-pulse-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #C8A96E;
    display: inline-block;
    animation: pulse-dot 2.5s ease-in-out infinite;
}}
@keyframes pulse-dot {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.3; transform: scale(0.6); }}
}}
.rp-hero-title {{
    font-family: 'Instrument Serif', serif !important;
    font-size: clamp(4rem, 11vw, 9rem);
    font-weight: 400;
    color: #FFFFFF;
    line-height: 0.95;
    letter-spacing: 0.01em;
    margin: 0 0 1.2rem 0;
    text-shadow: 0 4px 60px rgba(0,0,0,0.7);
    white-space: nowrap;
}}
.rp-hero-tagline {{
    font-family: 'Inter', sans-serif !important;
    font-size: clamp(0.95rem, 1.6vw, 1.2rem);
    font-weight: 400;
    letter-spacing: 0.04em;
    color: #C5C2BB;
    margin: 0 0 3rem 0;
    max-width: 560px;
}}
.rp-scroll-cue {{
    position: absolute;
    bottom: 2.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
    animation: float-cue 2.4s ease-in-out infinite;
}}
.rp-scroll-cue span {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #94A3B8;
}}
.rp-scroll-cue svg {{ width: 16px; height: 24px; }}
@keyframes float-cue {{
    0%, 100% {{ transform: translate(-50%, 0); opacity: 0.6; }}
    50% {{ transform: translate(-50%, 8px); opacity: 1; }}
}}

/* ── REVEAL AL HACER SCROLL ── */
.rp-reveal {{
    animation: rise-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
}}
@keyframes rise-in {{
    from {{ opacity: 0; transform: translateY(28px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* ── MANIFIESTO ── */
.rp-manifiesto {{
    font-size: 1.1rem;
    font-weight: 300;
    line-height: 1.85;
    color: #94A3B8;
    border-left: 2px solid #C8A96E;
    padding-left: 1.5rem;
    margin-bottom: 3rem;
}}

/* ── CITA EDITORIAL ── */
.rp-cita {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 2.2rem;
    font-style: italic;
    color: #E8E6E1;
    line-height: 1.25;
    margin: 2rem 0;
    padding: 1.5rem 0;
    border-top: 1px solid #1A1F2E;
    border-bottom: 1px solid #1A1F2E;
}}

/* ── TARJETAS DE INVESTIGACIÓN (con foto de fondo, clicables) ── */
.rp-linea-card-link {{
    text-decoration: none !important;
    display: block;
    margin-bottom: 1rem;
}}
.rp-linea-card {{
    position: relative;
    border: 1px solid #1A1F2E;
    border-radius: 4px;
    padding: 2.2rem;
    min-height: 190px;
    background-size: cover;
    background-position: center;
    overflow: hidden;
    transition: border-color 0.25s ease, transform 0.25s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}
.rp-linea-card:hover {{
    border-color: #C8A96E;
    transform: translateY(-3px);
}}
.rp-linea-numero {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #C8A96E;
    letter-spacing: 0.2em;
    margin-bottom: 0.6rem;
    display: block;
    position: relative;
    z-index: 2;
}}
.rp-linea-card h4 {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.6rem;
    color: #FFFFFF;
    margin: 0 0 0.4rem 0;
    font-weight: 400;
    position: relative;
    z-index: 2;
}}
.rp-linea-card p {{
    font-size: 0.85rem;
    color: #C5C2BB;
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 2;
    max-width: 90%;
}}

/* ── PUBLICACIONES RECIENTES ── */
.rp-reciente {{
    padding: 1.2rem 0;
    border-bottom: 1px solid #1A1F2E;
    text-decoration: none !important;
    display: block;
    transition: padding-left 0.2s ease;
}}
.rp-reciente:hover {{ padding-left: 0.5rem; }}
.rp-reciente-meta {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #4A5568;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}}
.rp-reciente-titulo {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.1rem;
    color: #E8E6E1 !important;
    line-height: 1.3;
    margin: 0;
}}

/* ── EXTENSIÓN BRIEFING ROOM EN INICIO ── */
.rp-briefing-promo {{
    position: relative;
    border-radius: 4px;
    border: 1px solid #1A1F2E;
    margin: 4rem 0 2rem 0;
    padding: 4rem 3rem;
    background:
        radial-gradient(ellipse at top left, rgba(200,169,110,0.07) 0%, transparent 55%),
        #0D1117;
    overflow: hidden;
}}
.rp-briefing-promo-grid {{
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(200,169,110,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(200,169,110,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
}}
.rp-briefing-promo-inner {{ position: relative; z-index: 2; }}
.rp-briefing-promo h3 {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 2.6rem;
    color: #FFFFFF;
    font-weight: 400;
    margin: 0.6rem 0 1rem 0;
    max-width: 600px;
}}
.rp-briefing-promo p {{
    font-size: 0.95rem;
    color: #94A3B8;
    max-width: 540px;
    line-height: 1.75;
    margin-bottom: 0;
}}
.rp-briefing-feature-row {{
    display: flex;
    gap: 2.5rem;
    margin-top: 2.2rem;
    flex-wrap: wrap;
}}
.rp-briefing-feature {{
    flex: 1;
    min-width: 180px;
}}
.rp-briefing-feature-num {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem;
    color: #C8A96E;
    letter-spacing: 0.15em;
}}
.rp-briefing-feature h5 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem;
    font-weight: 600;
    color: #E8E6E1;
    margin: 0.4rem 0 0.3rem 0;
}}
.rp-briefing-feature p {{
    font-size: 0.8rem;
    color: #4A5568;
    line-height: 1.6;
}}

/* ── BRIEFING ROOM — COLUMNAS DE INTELIGENCIA ── */
.rp-intel-col {{
    border: 1px solid #1A1F2E;
    border-radius: 3px;
    background: #0D1117;
    padding: 1.5rem;
    height: 100%;
}}
.rp-intel-header {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid #1A1F2E;
}}
.rp-intel-title {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #E8E6E1;
}}
.rp-intel-body {{
    font-size: 0.88rem;
    color: #B0AEA9;
    line-height: 1.75;
}}
.rp-intel-body strong {{ color: #C8A96E; font-weight: 600; }}
.rp-intel-empty {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    color: #2D3748;
    letter-spacing: 0.05em;
    line-height: 1.8;
}}
.rp-typing-cursor {{
    display: inline-block;
    width: 7px;
    height: 1em;
    background: #C8A96E;
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blink-cursor 0.9s step-end infinite;
}}
@keyframes blink-cursor {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}

/* ── BRIEFING ROOM (CHAT) ── */
.rp-briefing-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}}
.rp-online-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #C8A96E;
    display: inline-block;
    animation: pulse-dot 2s ease-in-out infinite;
}}
.rp-chat-bubble-user {{
    background: #0D1117;
    border: 1px solid #2D3748;
    padding: 1rem 1.2rem;
    border-radius: 2px 12px 12px 12px;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #E8E6E1;
}}
.rp-chat-bubble-ai {{
    background: #080A0F;
    border: 1px solid #1A1F2E;
    border-left: 3px solid #C8A96E;
    padding: 1rem 1.2rem;
    border-radius: 12px 2px 12px 12px;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #94A3B8;
}}
.rp-chat-label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #4A5568;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}}

/* ── CONTACTO ── */
.rp-contacto-info {{
    padding: 2rem;
    border: 1px solid #1A1F2E;
    border-radius: 3px;
    background: #0D1117;
}}
.rp-contacto-info h4 {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.4rem;
    color: #E8E6E1;
    margin-top: 0;
    font-weight: 400;
}}
.rp-contacto-info p {{
    font-size: 0.85rem;
    color: #4A5568;
    line-height: 1.7;
}}

/* ── ARTÍCULO (LECTURA) ── */
.rp-lectura-meta {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem;
    color: #C8A96E;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}}
.rp-lectura-titulo {{
    font-family: 'Instrument Serif', serif !important;
    font-size: clamp(2rem, 4.5vw, 3.2rem);
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1.1;
    margin-bottom: 2rem;
}}
.rp-lectura-body {{
    font-size: 1.1rem;
    color: #B0AEA9;
    line-height: 1.9;
    text-align: justify;
    max-width: 760px;
    margin-left: auto;
    margin-right: auto;
}}
.rp-lectura-body strong {{ color: #E8E6E1; font-weight: 600; }}

/* ── LISTA DE ARTÍCULOS (BROADSHEET) ── */
.rp-articulo-fila {{
    display: grid;
    grid-template-columns: 1fr 260px;
    gap: 2.5rem;
    padding: 2.5rem 0;
    border-bottom: 1px solid #1A1F2E;
    align-items: center;
}}
.rp-articulo-meta {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #4A5568;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}}
.rp-articulo-titulo {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.9rem;
    color: #E8E6E1 !important;
    line-height: 1.15;
    margin: 0 0 0.75rem 0;
    text-decoration: none !important;
    display: block;
}}
.rp-articulo-titulo:hover {{ color: #C8A96E !important; transition: color 0.2s; }}
.rp-articulo-sinopsis {{
    font-size: 0.875rem;
    color: #4A5568;
    line-height: 1.65;
    margin: 0 0 1rem 0;
}}
.rp-leer-link {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem;
    color: #C8A96E !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-decoration: none !important;
    border-bottom: 1px solid #C8A96E;
    padding-bottom: 1px;
    transition: opacity 0.2s;
}}
.rp-leer-link:hover {{ opacity: 0.7; }}
.rp-articulo-img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 2px;
    border: 1px solid #1A1F2E;
    filter: grayscale(20%);
    transition: filter 0.3s ease;
}}
.rp-articulo-fila:hover .rp-articulo-img {{ filter: grayscale(0%); }}

/* ── PIE DE PÁGINA ── */
.rp-footer {{
    max-width: 1180px;
    margin: 4rem auto 0 auto;
    padding: 1.5rem 0 0 0;
    border-top: 1px solid #1A1F2E;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.rp-footer-copy {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #2D3748;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

/* ── BOTONES STREAMLIT ── */
.stButton > button {{
    background: transparent !important;
    border: 1px solid #2D3748 !important;
    color: #94A3B8 !important;
    border-radius: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s, color 0.2s !important;
}}
.stButton > button:hover {{
    border-color: #C8A96E !important;
    color: #C8A96E !important;
    background: transparent !important;
}}
.rp-btn-grande button {{
    border: 1px solid #C8A96E !important;
    color: #C8A96E !important;
    padding: 0.95rem 1.5rem !important;
    font-size: 0.75rem !important;
}}
.rp-btn-grande button:hover {{
    background: #C8A96E !important;
    color: #080A0F !important;
}}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {{
    background: #0D1117 !important;
    border-color: #1A1F2E !important;
    color: #E8E6E1 !important;
    border-radius: 2px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}}
.stChatInput > div {{
    background: #0D1117 !important;
    border-color: #2D3748 !important;
    border-radius: 2px !important;
}}
.stChatInput textarea {{
    color: #E8E6E1 !important;
    font-family: 'Inter', sans-serif !important;
}}

/* ── PILLS ── */
.stPills [data-testid="stPillsButton"] {{
    background: transparent !important;
    border: 1px solid #2D3748 !important;
    color: #4A5568 !important;
    border-radius: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
}}
.stPills [aria-selected="true"] {{
    background: #0D1117 !important;
    border-color: #C8A96E !important;
    color: #C8A96E !important;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid #1A1F2E !important;
    gap: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #4A5568 !important;
    padding: 0.75rem 1.5rem !important;
    background: transparent !important;
    border: none !important;
}}
.stTabs [aria-selected="true"] {{
    color: #C8A96E !important;
    border-bottom: 2px solid #C8A96E !important;
}}

/* ── RADIO (fuente IA) ── */
.stRadio > div {{ gap: 0.4rem !important; }}
.stRadio label {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    color: #94A3B8 !important;
}}

/* ── CONTAINER CHAT ── */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: #0D1117 !important;
    border-color: #1A1F2E !important;
    border-radius: 3px !important;
}}

/* ── LABELS & MISC ── */
.stSelectbox label, .stTextInput label, .stTextArea label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    color: #4A5568 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}}
h2, h3 {{
    font-family: 'Instrument Serif', serif !important;
    color: #E8E6E1 !important;
    font-weight: 400 !important;
}}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {{
    .block-container {{ padding-left: 1.2rem !important; padding-right: 1.2rem !important; }}
    .rp-masthead {{ padding: 1.8rem 1.2rem 1.2rem 1.2rem; flex-direction: row; align-items: center; }}
    .rp-hero {{ padding: 2rem 1.2rem; min-height: 78vh; background-attachment: scroll; }}
    .rp-hero-title {{ font-size: 3.4rem; white-space: normal; }}
    .rp-articulo-fila {{ grid-template-columns: 1fr; }}
    .rp-articulo-img {{ height: 200px; }}
    .rp-nav-link {{ font-size: 0.66rem !important; padding: 0.4rem 0.7rem; }}
    .rp-cita {{ font-size: 1.6rem; }}
    .rp-lectura-body {{ font-size: 1rem; }}
    .rp-briefing-promo {{ padding: 2.5rem 1.5rem; }}
    .rp-briefing-promo h3 {{ font-size: 1.9rem; }}
}}
</style>
""", unsafe_allow_html=True)

# =========================================================================
# MASTHEAD + NAVEGACIÓN
# =========================================================================
paginas = {
    "Inicio": "Inicio",
    "Articulos": "Archivo",
    "AuditoriaIA": "Briefing Room",
    "Contacto": "Contacto",
    "MesaEditorial": "Editorial",
}

nav_links = ""
for key, label in paginas.items():
    css_activo = "activo" if st.session_state.pagina_actual == key or (key == "Articulos" and st.session_state.pagina_actual in ARTICULOS_DB) else ""
    nav_links += f'<a href="?nav={key}" target="_self" class="rp-nav-link {css_activo}">{label}</a>'

st.markdown(f"""
<div class="rp-masthead-wrap">
    <div class="rp-masthead">
        <a href="?nav=Inicio" target="_self" class="rp-wordmark">REALPOLITIK</a>
        <nav class="rp-nav">{nav_links}</nav>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================================
# VISTA 1: INICIO
# =========================================================================
if st.session_state.pagina_actual == "Inicio":

    st.markdown("""
    <div class="rp-hero">
        <p class="rp-hero-eyebrow"><span class="rp-pulse-dot"></span> Análisis en tiempo real · Edición 2026</p>
        <h1 class="rp-hero-title">REALPOLITIK</h1>
        <p class="rp-hero-tagline">Economía, Geopolítica & Análisis de Poder</p>
        <div class="rp-scroll-cue">
            <span>Desplázate</span>
            <svg viewBox="0 0 16 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="1" y="1" width="14" height="22" rx="7" stroke="#C8A96E" stroke-width="1"/>
                <circle cx="8" cy="7" r="2" fill="#C8A96E"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rp-content rp-reveal">', unsafe_allow_html=True)

    col_izq, col_der = st.columns([1.35, 1], gap="large")

    with col_izq:
        st.markdown("""
        <div class="rp-manifiesto">
            En un entorno global definido por la volatilidad sistémica y la saturación de ruido informativo,
            la comprensión del poder requiere un método riguroso. <strong style="color:#E8E6E1;">RealPolitik</strong>
            no es un espacio de opinión — mostramos datos y análisis objetivos para que construyas
            tus propias perspectivas. Abordamos la intersección donde los mercados financieros
            chocan con la arquitectura del Estado y las instituciones del poder.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="rp-cita">"Las ideas guían el debate, pero las instituciones y los flujos de capital determinan el desenlace."</div>', unsafe_allow_html=True)

        if st.button("→ Explorar Archivo Completo", use_container_width=True):
            st.session_state.pagina_actual = "Articulos"
            st.query_params["nav"] = "Articulos"
            st.rerun()

    with col_der:
        st.markdown('<span class="rp-seccion-label">Publicaciones Recientes</span>', unsafe_allow_html=True)
        claves = list(ARTICULOS_DB.keys())[-4:]
        for k in claves:
            art = ARTICULOS_DB[k]
            st.markdown(f"""
            <a href="?nav={k}" target="_self" class="rp-reciente">
                <div class="rp-reciente-meta">{art['fecha']} &nbsp;·&nbsp; {art['categoria'][:28]}…</div>
                <p class="rp-reciente-titulo">{art['titulo']}</p>
            </a>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="rp-seccion-label">Líneas de Investigación</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <a href="?nav=Articulos&filtro={quote('Geopolítica Monetaria & Mercados')}" target="_self" class="rp-linea-card-link">
            <div class="rp-linea-card" style="background-image: linear-gradient(to top, rgba(8,10,15,0.95) 10%, rgba(8,10,15,0.35) 100%), url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop');">
                <span class="rp-linea-numero">ÁREA I</span>
                <h4>Geopolítica Monetaria & Mercados</h4>
                <p>Hegemonía del dólar, mecánicas de mercado y bancos centrales.</p>
            </div>
        </a>
        <a href="?nav=Articulos&filtro={quote('Weltpolitik & Teoría del Estado')}" target="_self" class="rp-linea-card-link">
            <div class="rp-linea-card" style="background-image: linear-gradient(to top, rgba(8,10,15,0.95) 10%, rgba(8,10,15,0.35) 100%), url('https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=800&auto=format&fit=crop');">
                <span class="rp-linea-numero">ÁREA II</span>
                <h4>Weltpolitik & Teoría del Estado</h4>
                <p>Análisis de riesgo y proyecciones de poder bajo la óptica de la estabilidad institucional.</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    # ── EXTENSIÓN: PROMOCIÓN DEL BRIEFING ROOM ──
    st.markdown("""
    <div class="rp-briefing-promo">
        <div class="rp-briefing-promo-grid"></div>
        <div class="rp-briefing-promo-inner">
            <span class="rp-seccion-label">Laboratorio de Inteligencia Artificial</span>
            <h3>The Briefing Room</h3>
            <p>
                Una terminal de análisis geopolítico en tiempo real. Consulta nuestro corpus editorial
                o deja que la inteligencia artificial explore la web abierta, visualiza los focos de
                tensión en un globo terráqueo interactivo, y recibe briefings diarios sobre el estado
                del tablero global — generados y actualizados por IA.
            </p>
            <div class="rp-briefing-feature-row">
                <div class="rp-briefing-feature">
                    <span class="rp-briefing-feature-num">01</span>
                    <h5>Globo Interactivo</h5>
                    <p>Visualiza en 3D los países involucrados en cada consulta analítica.</p>
                </div>
                <div class="rp-briefing-feature">
                    <span class="rp-briefing-feature-num">02</span>
                    <h5>Briefings Automatizados</h5>
                    <p>Contexto global y sucesos de la semana, sintetizados por IA.</p>
                </div>
                <div class="rp-briefing-feature">
                    <span class="rp-briefing-feature-num">03</span>
                    <h5>Fuentes Configurables</h5>
                    <p>Elige si la IA responde solo con nuestro corpus o explora la web.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rp-btn-grande">', unsafe_allow_html=True)
    if st.button("→ Entrar al Briefing Room", use_container_width=True, key="btn_briefing_inicio"):
        st.session_state.pagina_actual = "AuditoriaIA"
        st.query_params["nav"] = "AuditoriaIA"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # cierre rp-content


# =========================================================================
# VISTA 2: ARCHIVO DE ARTÍCULOS
# =========================================================================
elif st.session_state.pagina_actual == "Articulos":
    st.markdown('<div class="rp-content">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="rp-seccion-label">Archivo Global</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="rp-seccion-title">Reportes & Análisis</h2>', unsafe_allow_html=True)

    categorias = ["Todos los Reportes", "Geopolítica Monetaria & Mercados", "Weltpolitik & Teoría del Estado"]
    idx_filtro = categorias.index(st.session_state.filtro_articulos) if st.session_state.filtro_articulos in categorias else 0
    filtro = st.pills("Filtrar por área:", categorias, default=categorias[idx_filtro])
    st.session_state.filtro_articulos = filtro

    for art_id, info in ARTICULOS_DB.items():
        if filtro != "Todos los Reportes" and info["categoria"] != filtro:
            continue
        cat_corta = info["categoria"]
        st.markdown(f"""
        <div class="rp-articulo-fila">
            <div>
                <div class="rp-articulo-meta">{info['fecha']} &nbsp;·&nbsp; {cat_corta}</div>
                <a href="?nav={art_id}" target="_self" class="rp-articulo-titulo">{info['titulo']}</a>
                <p class="rp-articulo-sinopsis">{info['sinopsis']}</p>
                <a href="?nav={art_id}" target="_self" class="rp-leer-link">Leer reporte completo →</a>
            </div>
            <img src="{info['imagen']}" class="rp-articulo-img" alt="">
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# VISTA 3: BRIEFING ROOM (REESTRUCTURADO)
# =========================================================================
elif st.session_state.pagina_actual == "AuditoriaIA":
    st.markdown('<div class="rp-content">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="rp-seccion-label">Inteligencia Artificial · Sala de Mando</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="rp-briefing-header">
        <span class="rp-online-dot"></span>
        <h2 class="rp-seccion-title" style="margin:0;">The Briefing Room</h2>
    </div>
    """, unsafe_allow_html=True)

    api_key = _get_api_key()

    # =====================================================================
    # AUTO-GENERACIÓN DE BRIEFING DIARIO (cacheado 1 hora)
    # =====================================================================
    cache_vencido = (time.time() - st.session_state.briefing_timestamp) > CACHE_BRIEFING_SEGUNDOS
    necesita_generar = api_key and (st.session_state.briefing_contexto is None or cache_vencido)

    if necesita_generar:
        try:
            with st.spinner("Generando briefing diario y localizando focos geopolíticos..."):
                contexto, semana, hotspots = generar_briefing_diario(api_key)
                st.session_state.briefing_contexto = contexto
                st.session_state.briefing_semana = semana
                st.session_state.hotspots_diarios = hotspots
                st.session_state.briefing_timestamp = time.time()
                # Si no hay una consulta activa del usuario, los hotspots del día toman el globo
                if st.session_state.foco_activo == "hotspots" or not st.session_state.historial_ia:
                    st.session_state.globe_countries = hotspots
                    st.session_state.foco_activo = "hotspots"
        except Exception as e:
            st.warning(f"⚠️ No fue posible generar el briefing automático: {str(e)}")

    # =====================================================================
    # PROCESAR CLIC EN PAÍS DEL GLOBO (llega vía query param desde el iframe)
    # =====================================================================
    if "_pais_click_pendiente" in st.session_state and st.session_state["_pais_click_pendiente"]:
        pais_click = st.session_state.pop("_pais_click_pendiente")
        if api_key and pais_click not in st.session_state.pais_tooltip_cache:
            try:
                with st.spinner(f"Generando briefing de {pais_click}..."):
                    texto_pais = generar_briefing_pais(api_key, pais_click)
                    st.session_state.pais_tooltip_cache[pais_click] = texto_pais
            except Exception as e:
                st.session_state.pais_tooltip_cache[pais_click] = f"⚠️ No se pudo generar el briefing: {str(e)}"
        st.session_state["_pais_activo_tooltip"] = pais_click

    # =====================================================================
    # FILA SUPERIOR: GLOBO (izquierda) + DOS COLUMNAS DE INTELIGENCIA (derecha)
    # =====================================================================
    col_globo, col_intel = st.columns([1, 1.15], gap="large")

    with col_globo:
        st.markdown('<span class="rp-seccion-label">Mapa Geopolítico · Vista 3D</span>', unsafe_allow_html=True)

        paises_js = json.dumps(st.session_state.globe_countries)
        foco_label = "Hotspots del Día" if st.session_state.foco_activo == "hotspots" else "Foco de tu Consulta"

        # Tooltip de país (si hay uno activo)
        pais_activo_tooltip = st.session_state.get("_pais_activo_tooltip", None)
        tooltip_texto = ""
        if pais_activo_tooltip and pais_activo_tooltip in st.session_state.pais_tooltip_cache:
            tooltip_texto = st.session_state.pais_tooltip_cache[pais_activo_tooltip]
        tooltip_js = json.dumps({"pais": pais_activo_tooltip, "texto": tooltip_texto} if pais_activo_tooltip else None)

        globo_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #080A0F; overflow: hidden; font-family: 'Inter', sans-serif; }}
  canvas {{ display: block; }}
  #globe-container {{ width: 100%; height: 540px; position: relative; cursor: grab; }}
  #globe-container:active {{ cursor: grabbing; }}
  #status {{
    position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%);
    font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4A5568;
    letter-spacing: 0.1em; text-transform: uppercase; white-space: nowrap; pointer-events: none;
  }}
  #countries-label {{
    position: absolute; top: 10px; left: 12px;
    font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #C8A96E;
    letter-spacing: 0.12em; text-transform: uppercase; pointer-events: none;
    line-height: 1.6; max-width: 220px;
  }}
  #zoom-hint {{
    position: absolute; top: 10px; right: 12px;
    font-family: 'JetBrains Mono', monospace; font-size: 8px; color: #2D3748;
    letter-spacing: 0.1em; text-transform: uppercase; pointer-events: none; text-align: right;
  }}
  #country-tooltip {{
    position: absolute;
    display: none;
    max-width: 240px;
    background: #0D1117;
    border: 1px solid #C8A96E;
    border-radius: 3px;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    z-index: 10;
    pointer-events: auto;
  }}
  #country-tooltip .tt-header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.5rem;
  }}
  #country-tooltip .tt-title {{
    font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.78rem;
    color: #C8A96E; letter-spacing: 0.04em; text-transform: uppercase;
  }}
  #country-tooltip .tt-close {{
    cursor: pointer; color: #4A5568; font-size: 0.9rem; line-height: 1;
    padding: 2px 5px;
  }}
  #country-tooltip .tt-close:hover {{ color: #E8E6E1; }}
  #country-tooltip .tt-body {{
    font-family: 'Inter', sans-serif; font-size: 0.78rem; color: #B0AEA9;
    line-height: 1.6;
  }}
  #country-tooltip .tt-loading {{
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #4A5568;
    letter-spacing: 0.08em;
  }}
</style>
</head>
<body>
<div id="globe-container">
  <canvas id="globe"></canvas>
  <div id="countries-label"></div>
  <div id="zoom-hint">Click en un país<br>para ver su briefing</div>
  <div id="status">Arrastra para rotar · Scroll para zoom</div>
  <div id="country-tooltip">
    <div class="tt-header">
      <span class="tt-title" id="tt-title"></span>
      <span class="tt-close" onclick="closeTooltip()">✕</span>
    </div>
    <div class="tt-body" id="tt-body"></div>
  </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js"></script>
<script>
const canvas = document.getElementById('globe');
const ctx = canvas.getContext('2d');
const container = document.getElementById('globe-container');
const tooltip = document.getElementById('country-tooltip');

const HIGHLIGHT_COUNTRIES = {paises_js};
const FOCO_LABEL = {json.dumps(foco_label)};
const TOOLTIP_DATA = {tooltip_js};

const COUNTRY_COORDS = {{
  "United States": [37.09, -95.71], "Russia": [61.52, 105.31], "China": [35.86, 104.19],
  "Germany": [51.16, 10.45], "United Kingdom": [55.37, -3.43], "France": [46.22, 2.21],
  "Japan": [36.20, 138.25], "Saudi Arabia": [23.88, 45.07], "Brazil": [-14.23, -51.92],
  "India": [20.59, 78.96], "Venezuela": [6.42, -66.58], "Iran": [32.42, 53.68],
  "Turkey": [38.96, 35.24], "Ukraine": [48.37, 31.16], "Israel": [31.04, 34.85],
  "South Africa": [-30.55, 22.93], "Argentina": [-38.41, -63.61], "Mexico": [23.63, -102.55],
  "Canada": [56.13, -106.34], "Australia": [-25.27, 133.77], "Spain": [40.46, -3.74],
  "Italy": [41.87, 12.56], "Netherlands": [52.13, 5.29], "Switzerland": [46.81, 8.22],
  "Egypt": [26.82, 30.80], "Nigeria": [9.08, 8.67], "Qatar": [25.35, 51.18],
  "United Arab Emirates": [23.42, 53.84], "South Korea": [35.90, 127.76], "Indonesia": [-0.78, 113.92],
  "Pakistan": [30.37, 69.34], "Poland": [51.91, 19.14], "Colombia": [4.57, -74.29],
}};

let W, H, R;
let rotX = 0.25, rotY = -0.5;
let isDragging = false, lastX, lastY, dragMoved = false;
let scale = 1.0;
let autoRotate = true;
let landFeatures = null;
let countryFeatures = null;

function resize() {{
  W = container.offsetWidth;
  H = container.offsetHeight;
  canvas.width = W;
  canvas.height = H;
  R = Math.min(W, H) * 0.42 * scale;
}}

function rotatePoint(x0, y0, z0) {{
  const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
  const x1 = x0 * cosY + z0 * sinY;
  const z1 = -x0 * sinY + z0 * cosY;
  const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
  const y2 = y0 * cosX - z1 * sinX;
  const z2 = y0 * sinX + z1 * cosX;
  return [x1, y2, z2];
}}

function project(lat, lon) {{
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lon + 180) * Math.PI / 180;
  const x0 = -Math.sin(phi) * Math.cos(theta);
  const y0 = Math.cos(phi);
  const z0 = Math.sin(phi) * Math.sin(theta);
  const [x1, y2, z2] = rotatePoint(x0, y0, z0);
  return {{ x: W / 2 + R * x1, y: H / 2 - R * y2, z: z2, visible: z2 > -0.05 }};
}}

function unprojectToSphere(px, py) {{
  // Aproxima si un punto de pantalla cae dentro del disco del globo, y devuelve lat/lon aproximado
  const dx = (px - W / 2) / R;
  const dy = -(py - H / 2) / R;
  const distSq = dx * dx + dy * dy;
  if (distSq > 1) return null;
  const dz = Math.sqrt(1 - distSq);
  // Deshacer rotación
  const cosX = Math.cos(-rotX), sinX = Math.sin(-rotX);
  const y1 = dy * cosX - dz * sinX;
  const z1 = dy * sinX + dz * cosX;
  const cosY = Math.cos(-rotY), sinY = Math.sin(-rotY);
  const x2 = dx * cosY + z1 * sinY;
  const z2 = -dx * sinY + z1 * cosY;
  const lat = Math.asin(Math.max(-1, Math.min(1, y1))) * 180 / Math.PI;
  let lon = Math.atan2(z2, x2) * 180 / Math.PI - 180;
  if (lon < -180) lon += 360;
  if (lon > 180) lon -= 360;
  return {{ lat, lon: -lon }};
}}

function pointInRing(lon, lat, ring) {{
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {{
    const xi = ring[i][0], yi = ring[i][1];
    const xj = ring[j][0], yj = ring[j][1];
    const intersect = ((yi > lat) !== (yj > lat)) &&
      (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }}
  return inside;
}}

function findCountryAt(lat, lon) {{
  if (!countryFeatures) return null;
  for (const feature of countryFeatures) {{
    const geom = feature.geometry;
    if (!geom) continue;
    const polygons = geom.type === 'Polygon' ? [geom.coordinates] : (geom.type === 'MultiPolygon' ? geom.coordinates : []);
    for (const polygon of polygons) {{
      if (polygon.length > 0 && pointInRing(lon, lat, polygon[0])) {{
        return feature.properties && (feature.properties.name || feature.properties.NAME);
      }}
    }}
  }}
  return null;
}}

function drawGlobe() {{
  ctx.clearRect(0, 0, W, H);

  const grd = ctx.createRadialGradient(W/2, H/2, R*0.3, W/2, H/2, R*1.1);
  grd.addColorStop(0, 'rgba(200,169,110,0.04)');
  grd.addColorStop(1, 'rgba(8,10,15,0)');
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, W, H);

  const sphereGrad = ctx.createRadialGradient(W/2 - R*0.25, H/2 - R*0.25, R*0.05, W/2, H/2, R);
  sphereGrad.addColorStop(0, '#0E1320');
  sphereGrad.addColorStop(0.6, '#080D14');
  sphereGrad.addColorStop(1, '#04060A');
  ctx.beginPath();
  ctx.arc(W/2, H/2, R, 0, Math.PI * 2);
  ctx.fillStyle = sphereGrad;
  ctx.fill();
  ctx.save();
  ctx.beginPath();
  ctx.arc(W/2, H/2, R, 0, Math.PI * 2);
  ctx.clip();

  ctx.strokeStyle = 'rgba(200,169,110,0.05)';
  ctx.lineWidth = 0.5;
  for (let lon = -180; lon <= 180; lon += 20) {{
    ctx.beginPath();
    let first = true;
    for (let lat = -90; lat <= 90; lat += 2) {{
      const p = project(lat, lon);
      if (p.visible) {{ if (first) {{ ctx.moveTo(p.x, p.y); first = false; }} else ctx.lineTo(p.x, p.y); }}
      else first = true;
    }}
    ctx.stroke();
  }}
  for (let lat = -60; lat <= 60; lat += 20) {{
    ctx.beginPath();
    let first = true;
    for (let lon = -180; lon <= 180; lon += 2) {{
      const p = project(lat, lon);
      if (p.visible) {{ if (first) {{ ctx.moveTo(p.x, p.y); first = false; }} else ctx.lineTo(p.x, p.y); }}
      else first = true;
    }}
    ctx.stroke();
  }}

  // Continentes (relleno)
  if (landFeatures) {{
    ctx.fillStyle = 'rgba(180,178,172,0.13)';
    landFeatures.forEach(feature => {{
      const geom = feature.geometry;
      if (!geom) return;
      const polygons = geom.type === 'Polygon' ? [geom.coordinates] : (geom.type === 'MultiPolygon' ? geom.coordinates : []);
      polygons.forEach(polygon => {{
        polygon.forEach(ring => {{
          ctx.beginPath();
          let started = false, lastVisible = false;
          ring.forEach(([lon, lat]) => {{
            const p = project(lat, lon);
            if (p.visible) {{
              if (!started || !lastVisible) {{ ctx.moveTo(p.x, p.y); started = true; }}
              else ctx.lineTo(p.x, p.y);
              lastVisible = true;
            }} else {{ lastVisible = false; }}
          }});
          ctx.closePath();
          ctx.fill();
        }});
      }});
    }});
  }}

  // Fronteras de países (trazo)
  if (countryFeatures) {{
    ctx.strokeStyle = 'rgba(200,169,110,0.32)';
    ctx.lineWidth = 0.7;
    countryFeatures.forEach(feature => {{
      const geom = feature.geometry;
      if (!geom) return;
      const polygons = geom.type === 'Polygon' ? [geom.coordinates] : (geom.type === 'MultiPolygon' ? geom.coordinates : []);
      polygons.forEach(polygon => {{
        polygon.forEach(ring => {{
          ctx.beginPath();
          let started = false, lastVisible = false;
          ring.forEach(([lon, lat]) => {{
            const p = project(lat, lon);
            if (p.visible) {{
              if (!started || !lastVisible) {{ ctx.moveTo(p.x, p.y); started = true; }}
              else ctx.lineTo(p.x, p.y);
              lastVisible = true;
            }} else {{ lastVisible = false; }}
          }});
          ctx.closePath();
          ctx.stroke();
        }});
      }});
    }});
  }}

  // Etiquetas de países al hacer zoom (solo cuando scale es alto)
  if (countryFeatures && scale > 1.5) {{
    ctx.font = '500 9px Inter, sans-serif';
    ctx.fillStyle = 'rgba(200,169,110,0.85)';
    ctx.textAlign = 'center';
    countryFeatures.forEach(feature => {{
      const name = feature.properties && (feature.properties.name || feature.properties.NAME);
      if (!name) return;
      // Centroide aproximado del primer anillo del primer polígono
      const geom = feature.geometry;
      const polygons = geom.type === 'Polygon' ? [geom.coordinates] : (geom.type === 'MultiPolygon' ? geom.coordinates : []);
      if (!polygons.length || !polygons[0].length) return;
      const ring = polygons[0][0];
      let sx = 0, sy = 0, n = 0;
      ring.forEach(([lon, lat]) => {{ sx += lon; sy += lat; n++; }});
      if (n === 0) return;
      const p = project(sy / n, sx / n);
      if (p.visible) {{
        ctx.fillText(name, p.x, p.y);
      }}
    }});
    ctx.textAlign = 'left';
  }}

  // Ecuador
  ctx.strokeStyle = 'rgba(200,169,110,0.1)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  let firstEq = true;
  for (let lon = -180; lon <= 180; lon += 1) {{
    const p = project(0, lon);
    if (p.visible) {{ if (firstEq) {{ ctx.moveTo(p.x, p.y); firstEq = false; }} else ctx.lineTo(p.x, p.y); }}
    else firstEq = true;
  }}
  ctx.stroke();

  ctx.restore();

  ctx.beginPath();
  ctx.arc(W/2, H/2, R, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(200,169,110,0.18)';
  ctx.lineWidth = 1;
  ctx.stroke();

  // Puntos de países resaltados (hotspots o foco de consulta)
  if (HIGHLIGHT_COUNTRIES.length > 0) {{
    HIGHLIGHT_COUNTRIES.forEach(country => {{
      const coords = COUNTRY_COORDS[country];
      if (!coords) return;
      const p = project(coords[0], coords[1]);
      if (!p.visible) return;

      const halo = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 20);
      halo.addColorStop(0, 'rgba(200,169,110,0.3)');
      halo.addColorStop(1, 'rgba(200,169,110,0)');
      ctx.fillStyle = halo;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 20, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#C8A96E';
      ctx.fill();

      const t = Date.now() / 1000;
      const pulse = 0.4 + 0.6 * Math.sin(t * 2);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 8 + 4 * Math.sin(t * 2), 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(200,169,110,${{pulse * 0.5}})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = 'rgba(232,230,225,0.95)';
      ctx.font = '600 10px Inter, sans-serif';
      ctx.fillText(country.toUpperCase(), p.x + 10, p.y - 6);
    }});
  }}
}}

function animate() {{
  if (autoRotate && !isDragging) {{ rotY += 0.0022; }}
  drawGlobe();
  requestAnimationFrame(animate);
}}

canvas.addEventListener('mousedown', e => {{
  isDragging = true; autoRotate = false; dragMoved = false;
  lastX = e.clientX; lastY = e.clientY; e.preventDefault();
}});
canvas.addEventListener('mousemove', e => {{
  if (!isDragging) return;
  const dx = e.clientX - lastX, dy = e.clientY - lastY;
  if (Math.abs(dx) > 2 || Math.abs(dy) > 2) dragMoved = true;
  rotY += dx * 0.005; rotX += dy * 0.005;
  rotX = Math.max(-Math.PI/2, Math.min(Math.PI/2, rotX));
  lastX = e.clientX; lastY = e.clientY;
}});
canvas.addEventListener('mouseup', e => {{
  isDragging = false;
  if (!dragMoved) handleClick(e.offsetX, e.offsetY, e.clientX, e.clientY);
}});
canvas.addEventListener('mouseleave', () => {{ isDragging = false; }});
canvas.addEventListener('wheel', e => {{
  scale *= e.deltaY > 0 ? 0.93 : 1.07;
  scale = Math.max(0.5, Math.min(3.5, scale));
  R = Math.min(W, H) * 0.42 * scale;
  e.preventDefault();
}}, {{ passive: false }});
canvas.addEventListener('touchstart', e => {{
  isDragging = true; autoRotate = false; dragMoved = false;
  lastX = e.touches[0].clientX; lastY = e.touches[0].clientY; e.preventDefault();
}}, {{ passive: false }});
canvas.addEventListener('touchmove', e => {{
  if (!isDragging) return;
  const dx = e.touches[0].clientX - lastX, dy = e.touches[0].clientY - lastY;
  if (Math.abs(dx) > 2 || Math.abs(dy) > 2) dragMoved = true;
  rotY += dx * 0.005; rotX += dy * 0.005;
  rotX = Math.max(-Math.PI/2, Math.min(Math.PI/2, rotX));
  lastX = e.touches[0].clientX; lastY = e.touches[0].clientY;
  e.preventDefault();
}}, {{ passive: false }});
canvas.addEventListener('touchend', () => {{ isDragging = false; }});

function handleClick(offsetX, offsetY, clientX, clientY) {{
  const sphere = unprojectToSphere(offsetX, offsetY);
  if (!sphere) return;
  const countryName = findCountryAt(sphere.lat, sphere.lon);
  if (!countryName) return;
  showTooltip(countryName, offsetX, offsetY);
  // Mostrar el tooltip inmediatamente; si ya tenemos el texto en caché (TOOLTIP_DATA), no recargar.
  if (TOOLTIP_DATA && TOOLTIP_DATA.pais === countryName) {{ return; }}
  try {{
    const url = new URL(window.parent.location.href);
    url.searchParams.set('pais_click_pendiente', countryName);
    url.searchParams.set('nav', 'AuditoriaIA');
    window.parent.location.href = url.toString();
  }} catch (e) {{
    document.getElementById('tt-body').innerHTML = '<span class="tt-loading">No se pudo conectar con el servidor.</span>';
  }}
}}

function showTooltip(name, x, y) {{
  document.getElementById('tt-title').textContent = name;
  const cached = (TOOLTIP_DATA && TOOLTIP_DATA.pais === name) ? TOOLTIP_DATA.texto : null;
  document.getElementById('tt-body').innerHTML = cached
    ? cached
    : '<span class="tt-loading">Generando briefing del país…</span>';
  tooltip.style.display = 'block';
  let left = x + 16, top = y - 10;
  if (left + 250 > W) left = x - 260;
  if (top + 120 > H) top = H - 130;
  tooltip.style.left = left + 'px';
  tooltip.style.top = Math.max(10, top) + 'px';
}}
function closeTooltip() {{ tooltip.style.display = 'none'; }}

// Si ya tenemos datos de tooltip desde Streamlit (tras recargar), mostrarlo automáticamente
if (TOOLTIP_DATA && TOOLTIP_DATA.pais) {{
  const coords = COUNTRY_COORDS[TOOLTIP_DATA.pais];
  setTimeout(() => {{
    if (coords) {{
      const p = project(coords[0], coords[1]);
      showTooltip(TOOLTIP_DATA.pais, p.x, p.y);
    }} else {{
      showTooltip(TOOLTIP_DATA.pais, W/2, H/2);
    }}
  }}, 300);
}}

const label = document.getElementById('countries-label');
if (HIGHLIGHT_COUNTRIES.length > 0) {{
  label.innerHTML = '<span style="color:#4A5568;">' + FOCO_LABEL + ':</span><br>' + HIGHLIGHT_COUNTRIES.join('<br>');
}} else {{
  label.innerHTML = '<span style="color:#2D3748;">Sin foco activo</span>';
}}

resize();
window.addEventListener('resize', () => {{ resize(); }});

fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json')
  .then(r => r.json())
  .then(data => {{ landFeatures = topojson.feature(data, data.objects.land).features; }})
  .catch(() => {{ landFeatures = null; }});

fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
  .then(r => r.json())
  .then(data => {{ countryFeatures = topojson.feature(data, data.objects.countries).features; }})
  .catch(() => {{ countryFeatures = null; }});

animate();
</script>
</body>
</html>
"""
        st.components.v1.html(globo_html, height=540)
        st.markdown(f"""
        <span class="rp-seccion-label">
            {f"{foco_label}: {', '.join(st.session_state.globe_countries)}" if st.session_state.globe_countries else "Generando localizador geopolítico…"}
        </span>
        """, unsafe_allow_html=True)

    with col_intel:
        st.markdown('<span class="rp-seccion-label">Inteligencia Automatizada</span>', unsafe_allow_html=True)

        sub_col1, sub_col2 = st.columns(2, gap="medium")

        with sub_col1:
            st.markdown('<div class="rp-intel-col">', unsafe_allow_html=True)
            st.markdown("""
            <div class="rp-intel-header">
                <span class="rp-online-dot"></span>
                <span class="rp-intel-title">Resumen del Contexto Actual</span>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.briefing_contexto:
                clave_tipeo = f"ctx_{int(st.session_state.briefing_timestamp)}"
                render_texto_tipeo(st.session_state.briefing_contexto, velocidad_ms=10, key=clave_tipeo)
            else:
                st.markdown('<div class="rp-intel-empty">Generando briefing automáticamente…</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sub_col2:
            st.markdown('<div class="rp-intel-col">', unsafe_allow_html=True)
            st.markdown("""
            <div class="rp-intel-header">
                <span class="rp-online-dot"></span>
                <span class="rp-intel-title">Sucesos de esta Semana</span>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.briefing_semana:
                clave_tipeo = f"sem_{int(st.session_state.briefing_timestamp)}"
                render_texto_tipeo(st.session_state.briefing_semana, velocidad_ms=10, key=clave_tipeo)
            else:
                st.markdown('<div class="rp-intel-empty">Generando briefing automáticamente…</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        minutos_restantes = max(0, int((CACHE_BRIEFING_SEGUNDOS - (time.time() - st.session_state.briefing_timestamp)) / 60))
        col_refresh, col_cache_info = st.columns([1, 1.4])
        with col_refresh:
            if st.button("⟳ Forzar Actualización", use_container_width=True, key="btn_gen_briefing"):
                if not api_key:
                    st.error("Falta la API Key en el entorno del servidor.")
                else:
                    try:
                        with st.spinner("Regenerando briefing e identificando hotspots..."):
                            contexto, semana, hotspots = generar_briefing_diario(api_key)
                            st.session_state.briefing_contexto = contexto
                            st.session_state.briefing_semana = semana
                            st.session_state.hotspots_diarios = hotspots
                            st.session_state.briefing_timestamp = time.time()
                            st.session_state.globe_countries = hotspots
                            st.session_state.foco_activo = "hotspots"
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ No fue posible generar el briefing automatizado: {str(e)}")
        with col_cache_info:
            if st.session_state.briefing_contexto:
                st.markdown(f'<div class="rp-intel-empty" style="padding-top:0.7rem;">Próxima actualización automática en ~{minutos_restantes} min</div>', unsafe_allow_html=True)

    st.markdown("<br><hr style='border-top: 1px solid #1A1F2E; margin: 1rem 0 2.5rem 0;'><br>", unsafe_allow_html=True)

    # =====================================================================
    # TERMINAL DE CONSULTA — chat con selector de fuentes
    # =====================================================================
    st.markdown('<span class="rp-seccion-label">Terminal de Consulta</span>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#4A5568; font-size:0.85rem; margin-bottom:1.5rem;">
        Formula una consulta — el sistema identificará los países involucrados y los resaltará en el globo,
        reemplazando temporalmente los hotspots del día.
    </p>
    """, unsafe_allow_html=True)

    col_config1, col_config2 = st.columns([1, 1], gap="large")

    with col_config1:
        titulos_articulos = [info["titulo"] for info in ARTICULOS_DB.values()]
        articulo_seleccionado = st.selectbox(
            "Contexto de análisis:",
            ["Todo el Corpus Disponible"] + titulos_articulos
        )

    with col_config2:
        fuente_opciones = ["Solo Corpus", "Solo Web", "Corpus + Web"]
        idx_fuente = fuente_opciones.index(st.session_state.fuente_ia) if st.session_state.fuente_ia in fuente_opciones else 2
        fuente_seleccionada = st.radio(
            "Fuente de información de la IA:",
            fuente_opciones,
            index=idx_fuente,
            horizontal=True
        )
        st.session_state.fuente_ia = fuente_seleccionada

    contenedor_chat = st.container(height=400, border=True)
    with contenedor_chat:
        if not st.session_state.historial_ia:
            st.markdown(f"""
            <div class="rp-chat-label">Sistema</div>
            <div class="rp-chat-bubble-ai">
                <strong>[REALAI v3.0]</strong> &nbsp;·&nbsp; Gemini 2.5 Flash<br>
                Corpus activo: <em>{articulo_seleccionado}</em> &nbsp;·&nbsp; Fuente: <em>{fuente_seleccionada}</em><br>
                <span style="color:#4A5568; font-size:0.8rem;">Los países mencionados en tu consulta se resaltarán automáticamente en el globo.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for idx, msg in enumerate(st.session_state.historial_ia):
                if msg["rol"] == "usuario":
                    st.markdown(f'<div class="rp-chat-label">Analista</div><div class="rp-chat-bubble-user">{msg["texto"]}</div>', unsafe_allow_html=True)
                else:
                    es_ultimo = (idx == len(st.session_state.historial_ia) - 1)
                    st.markdown('<div class="rp-chat-label">RealPolitik AI</div>', unsafe_allow_html=True)
                    if es_ultimo and not msg.get("ya_tipeado", False):
                        render_texto_tipeo(msg["texto"], contenedor_css_class="rp-chat-bubble-ai", velocidad_ms=8, key=f"chat_{idx}")
                        msg["ya_tipeado"] = True
                    else:
                        st.markdown(f'<div class="rp-chat-bubble-ai">{msg["texto"]}</div>', unsafe_allow_html=True)

    col_input_btn, col_clear = st.columns([3, 1])
    with col_clear:
        if st.button("Limpiar Chat", use_container_width=True):
            st.session_state.historial_ia = []
            st.session_state.globe_countries = st.session_state.hotspots_diarios
            st.session_state.foco_activo = "hotspots"
            st.session_state.pop("_pais_activo_tooltip", None)
            st.rerun()

    prompt_usuario = st.chat_input("Escriba su consulta geopolítica...")

    if prompt_usuario:
        if not api_key:
            st.error("Falta la API Key en el entorno del servidor.")
            st.stop()

        st.session_state.historial_ia.append({"rol": "usuario", "texto": prompt_usuario})

        if articulo_seleccionado == "Todo el Corpus Disponible":
            contexto_documento = "\n\n".join([f"Articulo: {a['titulo']}\nContenido: {a['contenido']}" for a in ARTICULOS_DB.values()])
        else:
            id_art = [k for k, v in ARTICULOS_DB.items() if v["titulo"] == articulo_seleccionado][0]
            contexto_documento = f"Articulo: {articulo_seleccionado}\nContenido: {ARTICULOS_DB[id_art]['contenido']}"

        if fuente_seleccionada == "Solo Corpus":
            restriccion = "Debes responder ÚNICAMENTE con base en el corpus documental provisto abajo. No utilices conocimiento externo ni busques en la web. Si la respuesta no está en el corpus, indícalo explícitamente."
            usar_grounding = False
        elif fuente_seleccionada == "Solo Web":
            restriccion = "Ignora el corpus documental provisto y responde únicamente con información actual obtenida de la búsqueda web."
            usar_grounding = True
        else:
            restriccion = "Puedes combinar el corpus documental provisto con búsquedas web para enriquecer tu respuesta con información actual."
            usar_grounding = True

        instrucciones = f"""Actúas como el consultor/analista en jefe de REALPOLITIK.
Tono frío, analítico, profundo y absolutamente objetivo.

{restriccion}

CORPUS:
{contexto_documento}

INSTRUCCIÓN ESPECIAL: Al final de tu respuesta, añade siempre una línea con el formato exacto:
PAÍSES_MAPA: [lista de países relevantes separados por coma en inglés, ej: United States, Russia, China]
Si no hay países relevantes, escribe: PAÍSES_MAPA: ninguno"""

        try:
            client = genai.Client(api_key=api_key)
            config_kwargs = {"system_instruction": instrucciones, "temperature": 0.3}
            if usar_grounding:
                config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_usuario,
                config=types.GenerateContentConfig(**config_kwargs)
            )
            respuesta_completa = response.text

            if "PAÍSES_MAPA:" in respuesta_completa:
                partes = respuesta_completa.split("PAÍSES_MAPA:")
                respuesta_ia = partes[0].strip()
                paises_raw = partes[1].strip()
                if paises_raw.lower() != "ninguno":
                    st.session_state.globe_countries = [p.strip() for p in paises_raw.split(",") if p.strip()]
                    st.session_state.foco_activo = "consulta"
                else:
                    st.session_state.globe_countries = []
                    st.session_state.foco_activo = "consulta"
            else:
                respuesta_ia = respuesta_completa
                st.session_state.globe_countries = []
                st.session_state.foco_activo = "consulta"

        except Exception as e:
            respuesta_ia = f"⚠️ Error del Sistema: {str(e)}"
            st.session_state.globe_countries = []
            st.session_state.foco_activo = "consulta"

        st.session_state.historial_ia.append({"rol": "sistema", "texto": respuesta_ia})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)



# =========================================================================
# VISTA 4: CONTACTO
# =========================================================================
elif st.session_state.pagina_actual == "Contacto":
    st.markdown('<div class="rp-content">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="rp-seccion-label">Comunicación Institucional</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="rp-seccion-title">Oficina de Enlace</h2>', unsafe_allow_html=True)

    col_form, col_info = st.columns([1.4, 0.9], gap="large")

    with col_form:
        with st.form("formulario_contacto", clear_on_submit=True):
            tipo_enlace = st.selectbox("Naturaleza del Requerimiento:", [
                "Consulta Académica / Proyectos de Investigación",
                "Propuesta de Colaboración Editorial"
            ])
            nombre = st.text_input("Nombre Completo:")
            correo = st.text_input("Dirección de Correo Electrónico:")
            asunto = st.text_input("Asunto:")
            mensaje = st.text_area("Mensaje:", height=160)
            if st.form_submit_button("→ Enviar Mensaje", use_container_width=True):
                st.success("Requerimiento recibido. El equipo editorial se pondrá en contacto a la brevedad.")

    with col_info:
        st.markdown("""
        <div class="rp-contacto-info">
            <h4>RealPolitik Network</h4>
            <p>
                Plataforma de análisis estratégico independiente. Aceptamos propuestas
                de colaboración editorial, consultas académicas y proyectos de investigación
                alineados con nuestras líneas de trabajo.
            </p>
            <br>
            <p>
                <span style="color:#C8A96E; font-family:'JetBrains Mono',monospace; font-size:0.7rem; letter-spacing:0.1em;">
                    INSTAGRAM
                </span><br>
                @es.realpolitik
            </p>
            <br>
            <p style="color:#2D3748; font-size:0.75rem;">
                Todas las comunicaciones son tratadas con carácter confidencial.
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# VISTA 5: MESA EDITORIAL
# =========================================================================
elif st.session_state.pagina_actual == "MesaEditorial":
    st.markdown('<div class="rp-content">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="rp-seccion-label">Acceso Restringido · Panel de Control</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="rp-seccion-title">Mesa Editorial</h2>', unsafe_allow_html=True)

    if not st.session_state.editorial_autenticado:
        st.markdown("<p style='color:#4A5568; font-size:0.9rem;'>Ingrese las credenciales del panel de control para continuar.</p>", unsafe_allow_html=True)
        col_login, _ = st.columns([1, 1.5])
        with col_login:
            with st.form("credenciales_editor"):
                input_user = st.text_input("Usuario:")
                input_pass = st.text_input("Contraseña:", type="password")
                if st.form_submit_button("→ Autenticar", use_container_width=True):
                    if input_user == "admin" and input_pass == "realpolitik2026":
                        st.session_state.editorial_autenticado = True
                        st.success("Acceso concedido.")
                        st.rerun()
                    else:
                        st.error("Credenciales inválidas.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    col_cierre, _ = st.columns([1, 3])
    with col_cierre:
        if st.button("🔒 Cerrar Sesión", use_container_width=True):
            st.session_state.editorial_autenticado = False
            st.session_state.pagina_actual = "Inicio"
            st.rerun()

    tab_crear, tab_editar = st.tabs(["Publicar Nuevo Ensayo", "Modificar / Eliminar"])

    with tab_crear:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("nuevo_articulo_form"):
            new_title = st.text_input("Título del Reporte:")
            new_date = st.text_input("Fecha (Ej: JUNIO 2026):", value="MAYO 2026")
            new_cat = st.selectbox("Línea de Investigación:", [
                "Geopolítica Monetaria & Mercados",
                "Weltpolitik & Teoría del Estado"
            ])
            new_sinopsis = st.text_area("Sinopsis (máx. 350 caracteres):", max_chars=350)
            new_img = st.text_input("URL de Imagen de Portada:", value="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop")
            new_content = st.text_area("Cuerpo del Ensayo:", height=300)

            if st.form_submit_button("→ Publicar Reporte", use_container_width=True):
                if not new_title or not new_content:
                    st.error("El título y el contenido son obligatorios.")
                else:
                    nuevo_id = "Art_" + "".join(e for e in new_title.title() if e.isalnum())[:15]
                    ARTICULOS_DB[nuevo_id] = {
                        "titulo": new_title,
                        "fecha": new_date.upper(),
                        "categoria": new_cat,
                        "sinopsis": new_sinopsis,
                        "imagen": new_img,
                        "contenido": new_content
                    }
                    guardar_articulos(ARTICULOS_DB)
                    st.success(f"'{new_title}' publicado exitosamente.")
                    st.rerun()

    with tab_editar:
        st.markdown("<br>", unsafe_allow_html=True)
        if not ARTICULOS_DB:
            st.info("No hay artículos en la base de datos.")
        else:
            art_a_editar = st.selectbox(
                "Seleccionar ensayo:",
                list(ARTICULOS_DB.keys()),
                format_func=lambda x: ARTICULOS_DB[x]["titulo"]
            )

            if st.button("🚨 Eliminar Artículo Definitivamente", use_container_width=True):
                del ARTICULOS_DB[art_a_editar]
                guardar_articulos(ARTICULOS_DB)
                st.warning("Artículo eliminado del registro.")
                st.rerun()

            st.markdown("<hr style='border-top: 1px solid #1A1F2E; margin: 1.5rem 0;'>", unsafe_allow_html=True)

            with st.form("editar_articulo_form"):
                edit_title = st.text_input("Título:", value=ARTICULOS_DB[art_a_editar]["titulo"])
                edit_date = st.text_input("Fecha:", value=ARTICULOS_DB[art_a_editar]["fecha"])
                edit_cat = st.selectbox("Categoría:", [
                    "Geopolítica Monetaria & Mercados",
                    "Weltpolitik & Teoría del Estado"
                ], index=0 if ARTICULOS_DB[art_a_editar]["categoria"] == "Geopolítica Monetaria & Mercados" else 1)
                edit_sinopsis = st.text_area("Sinopsis:", value=ARTICULOS_DB[art_a_editar]["sinopsis"])
                edit_img = st.text_input("URL Imagen:", value=ARTICULOS_DB[art_a_editar]["imagen"])
                edit_content = st.text_area("Contenido:", value=ARTICULOS_DB[art_a_editar]["contenido"], height=250)

                if st.form_submit_button("→ Guardar Cambios", use_container_width=True):
                    ARTICULOS_DB[art_a_editar] = {
                        "titulo": edit_title,
                        "fecha": edit_date.upper(),
                        "categoria": edit_cat,
                        "sinopsis": edit_sinopsis,
                        "imagen": edit_img,
                        "contenido": edit_content
                    }
                    guardar_articulos(ARTICULOS_DB)
                    st.success("Cambios guardados.")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# VISTAS DINÁMICAS DE ARTÍCULOS INDIVIDUALES
# =========================================================================
elif st.session_state.pagina_actual in ARTICULOS_DB:
    art_info = ARTICULOS_DB[st.session_state.pagina_actual]

    st.markdown('<div class="rp-content">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f'<p class="rp-lectura-meta">{art_info["fecha"]} &nbsp;·&nbsp; {art_info["categoria"].upper()}</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="rp-lectura-titulo">{art_info["titulo"]}</h1>', unsafe_allow_html=True)

    st.image(art_info["imagen"], use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    contenido_completo = art_info["contenido"]

    if "[GRAFICO_INTERACTIVO_RESERVAS]" in contenido_completo and "datos_grafica" in art_info and art_info["datos_grafica"].strip():
        import pandas as pd
        import plotly.express as px
        import io

        parte_alta, parte_baja = contenido_completo.split("[GRAFICO_INTERACTIVO_RESERVAS]")
        st.markdown(f'<div class="rp-lectura-body">{parte_alta}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        try:
            data_stream = io.StringIO(art_info["datos_grafica"].strip())
            df = pd.read_csv(data_stream)

            fig = px.line(df, x=df.columns[0], y=df.columns[1],
                          template="plotly_dark",
                          color_discrete_sequence=["#C8A96E"])

            fig.update_traces(line_width=2.5)
            fig.update_layout(
                paper_bgcolor="#0D1117",
                plot_bgcolor="#080A0F",
                font_family="Inter",
                font_color="#94A3B8",
                hovermode="x unified",
                margin=dict(l=30, r=20, t=30, b=30),
                showlegend=False
            )
            fig.update_xaxes(showgrid=True, gridcolor="#1A1F2E", linecolor="#2D3748")
            fig.update_yaxes(showgrid=True, gridcolor="#1A1F2E", linecolor="#2D3748")

            st.markdown('<span class="rp-seccion-label" style="text-align:center; display:block;">INDICADOR CRÍTICO · RESERVAS DE ORO EE.UU. (1944–1971)</span>', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error en la carga del gráfico: {e}")

        st.markdown(f'<div class="rp-lectura-body">{parte_baja}</div>', unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="rp-lectura-body">{contenido_completo}</div>', unsafe_allow_html=True)

    st.markdown("<br><hr style='border-top: 1px solid #1A1F2E;'><br>", unsafe_allow_html=True)

    if st.button("← Volver al Archivo", use_container_width=False):
        st.session_state.pagina_actual = "Articulos"
        st.query_params["nav"] = "Articulos"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# PIE DE PÁGINA
# =========================================================================
st.markdown(f"""
<div class="rp-footer">
    <span class="rp-footer-copy">Realpolitik Intelligence Network © 2026</span>
    <span class="rp-footer-copy">Documento de Acceso Abierto</span>
</div>
""", unsafe_allow_html=True)
