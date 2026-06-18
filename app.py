import streamlit as st
import os
import json
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

# =========================================================================
# SISTEMA DE DISEÑO — REALPOLITIK v2
# Paleta: Fondo abismal · Ámbar diplomático · Pergamino frío
# Firma: Coordenadas geográficas como localizador de análisis
# =========================================================================

COORDS_POR_SECCION = {
    "Inicio":         "38°53'N · 77°02'O",   # Washington D.C.
    "Articulos":      "51°30'N · 00°07'O",   # Londres / The Economist
    "AuditoriaIA":    "48°51'N · 02°21'E",   # París / análisis estratégico
    "Contacto":       "40°25'N · 03°41'O",   # Madrid
    "MesaEditorial":  "00°00'N · 00°00'E",   # Origen
}

pagina = st.session_state.pagina_actual
coord_display = COORDS_POR_SECCION.get(pagina, "00°00'N · 00°00'E")
if pagina in ARTICULOS_DB:
    coord_display = "Análisis en curso · Documento Clasificado"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

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
    max-width: 1100px !important;
}}

html, body, p, li, span {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 400;
    line-height: 1.7;
    color: #E8E6E1;
}}

/* ── MASTHEAD ── */
.rp-masthead {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 2.2rem 0 1.2rem 0;
    border-bottom: 1px solid #1A1F2E;
    margin-bottom: 0;
}}
.rp-wordmark {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #E8E6E1;
    text-decoration: none;
}}
.rp-coords {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem;
    color: #C8A96E;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding-bottom: 0.15rem;
}}

/* ── BARRA DE NAVEGACIÓN ── */
.rp-nav {{
    display: flex;
    gap: 0;
    border-bottom: 1px solid #1A1F2E;
    margin-bottom: 3.5rem;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}}
.rp-nav::-webkit-scrollbar {{ display: none; }}
.rp-nav-link {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4A5568 !important;
    text-decoration: none !important;
    padding: 1rem 1.5rem;
    border-bottom: 2px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
    white-space: nowrap;
    display: inline-block;
}}
.rp-nav-link:hover {{ color: #E8E6E1 !important; }}
.rp-nav-link.activo {{
    color: #C8A96E !important;
    border-bottom: 2px solid #C8A96E;
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

/* ── HERO ── */
.rp-hero {{
    position: relative;
    width: 100%;
    min-height: 52vh;
    background-image:
        linear-gradient(to bottom, rgba(8,10,15,0.35) 0%, rgba(8,10,15,0.75) 60%, rgba(8,10,15,1) 100%),
        url('https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Bucarest_-_Palau_del_Parlament.png/960px-Bucarest_-_Palau_del_Parlament.png');
    background-size: cover;
    background-position: center 30%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 3rem 3.5rem;
    margin-bottom: 3.5rem;
    border-radius: 4px;
    border: 1px solid #1A1F2E;
    overflow: hidden;
}}
.rp-hero::before {{
    content: '';
    position: absolute;
    top: 1.2rem; left: 1.5rem;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #C8A96E;
    animation: pulse-dot 2.5s ease-in-out infinite;
}}
@keyframes pulse-dot {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.3; transform: scale(0.6); }}
}}
.rp-hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #C8A96E;
    text-transform: uppercase;
    margin-bottom: 1rem;
}}
.rp-hero-title {{
    font-family: 'Instrument Serif', serif !important;
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 400;
    color: #FFFFFF;
    line-height: 0.95;
    letter-spacing: -0.01em;
    margin: 0 0 1rem 0;
    text-shadow: 0 4px 40px rgba(0,0,0,0.6);
}}
.rp-hero-tagline {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.3rem;
    font-style: italic;
    color: #94A3B8;
    margin: 0;
    max-width: 520px;
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

/* ── TARJETAS DE INVESTIGACIÓN ── */
.rp-linea-card {{
    border: 1px solid #1A1F2E;
    border-radius: 3px;
    padding: 2rem;
    margin-bottom: 1rem;
    background: #0D1117;
    transition: border-color 0.25s ease, transform 0.25s ease;
    cursor: default;
}}
.rp-linea-card:hover {{
    border-color: #2D3748;
    transform: translateY(-2px);
}}
.rp-linea-numero {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem;
    color: #C8A96E;
    letter-spacing: 0.2em;
    margin-bottom: 0.75rem;
    display: block;
}}
.rp-linea-card h4 {{
    font-family: 'Instrument Serif', serif !important;
    font-size: 1.5rem;
    color: #E8E6E1;
    margin: 0 0 0.5rem 0;
    font-weight: 400;
}}
.rp-linea-card p {{
    font-size: 0.85rem;
    color: #4A5568;
    margin: 0;
    line-height: 1.6;
}}

/* ── PUBLICACIONES RECIENTES (SIDEBAR) ── */
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

/* ── BRIEFING ROOM (CHAT + GLOBO) ── */
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
    max-width: 720px;
}}
.rp-lectura-body strong {{ color: #E8E6E1; font-weight: 600; }}

/* ── PIE DE PÁGINA ── */
.rp-footer {{
    border-top: 1px solid #1A1F2E;
    padding-top: 1.5rem;
    margin-top: 4rem;
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
.stRadio label {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    color: #94A3B8 !important;
}}
h2, h3 {{
    font-family: 'Instrument Serif', serif !important;
    color: #E8E6E1 !important;
    font-weight: 400 !important;
}}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {{
    .rp-hero {{ padding: 2rem 1.5rem; min-height: 40vh; }}
    .rp-hero-title {{ font-size: 2.8rem; }}
    .rp-articulo-fila {{ grid-template-columns: 1fr; }}
    .rp-articulo-img {{ height: 200px; }}
    .rp-masthead {{ flex-direction: column; align-items: flex-start; gap: 0.5rem; }}
    .rp-cita {{ font-size: 1.6rem; }}
    .rp-lectura-body {{ font-size: 1rem; }}
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
<div class="rp-masthead">
    <a href="?nav=Inicio" target="_self" class="rp-wordmark">Realpolitik</a>
    <span class="rp-coords">{coord_display}</span>
</div>
<nav class="rp-nav">{nav_links}</nav>
""", unsafe_allow_html=True)


# =========================================================================
# VISTA 1: INICIO
# =========================================================================
if st.session_state.pagina_actual == "Inicio":

    st.markdown("""
    <div class="rp-hero">
        <p class="rp-hero-eyebrow">⬤ &nbsp; Análisis en tiempo real · Edición 2026</p>
        <h1 class="rp-hero-title">REAL<br>POLITIK</h1>
        <p class="rp-hero-tagline">Economía, Geopolítica & Análisis de Poder</p>
    </div>
    """, unsafe_allow_html=True)

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

        st.markdown("""
        <div class="rp-linea-card">
            <span class="rp-linea-numero">ÁREA I</span>
            <h4>Geopolítica Monetaria & Mercados</h4>
            <p>Hegemonía del dólar, mecánicas de mercado y bancos centrales.</p>
        </div>
        <div class="rp-linea-card">
            <span class="rp-linea-numero">ÁREA II</span>
            <h4>Weltpolitik & Teoría del Estado</h4>
            <p>Análisis de riesgo y proyecciones de poder bajo la óptica de la estabilidad institucional.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("→ Iniciar Briefing Room (IA)", use_container_width=True):
            st.session_state.pagina_actual = "AuditoriaIA"
            st.query_params["nav"] = "AuditoriaIA"
            st.rerun()


# =========================================================================
# VISTA 2: ARCHIVO DE ARTÍCULOS
# =========================================================================
elif st.session_state.pagina_actual == "Articulos":
    st.markdown('<span class="rp-seccion-label">Archivo Global</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="rp-seccion-title">Reportes & Análisis</h2>', unsafe_allow_html=True)

    categorias = ["Todos los Reportes", "Geopolítica Monetaria & Mercados", "Weltpolitik & Teoría del Estado"]
    filtro = st.pills("Filtrar por área:", categorias, default="Todos los Reportes")

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


# =========================================================================
# VISTA 3: BRIEFING ROOM (IA + GLOBO 3D)
# =========================================================================
elif st.session_state.pagina_actual == "AuditoriaIA":

    st.markdown('<span class="rp-seccion-label">Inteligencia Artificial · Corpus RealPolitik</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="rp-briefing-header">
        <span class="rp-online-dot"></span>
        <h2 class="rp-seccion-title" style="margin:0;">The Briefing Room</h2>
    </div>
    <p style="color:#4A5568; font-size:0.85rem; margin-bottom:2rem;">
        Terminal de análisis geopolítico potenciada por IA. Formula una consulta —
        el sistema identificará los países involucrados y los resaltará en el globo terrestre.
    </p>
    """, unsafe_allow_html=True)

    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")

    col_chat, col_globo = st.columns([1.1, 1], gap="large")

    with col_chat:
        st.markdown('<span class="rp-seccion-label">Consola de Análisis</span>', unsafe_allow_html=True)

        titulos_articulos = [info["titulo"] for info in ARTICULOS_DB.values()]
        articulo_seleccionado = st.selectbox(
            "Contexto de análisis:",
            ["Todo el Corpus Disponible"] + titulos_articulos
        )

        contenedor_chat = st.container(height=400, border=True)
        with contenedor_chat:
            if not st.session_state.historial_ia:
                st.markdown(f"""
                <div class="rp-chat-label">Sistema</div>
                <div class="rp-chat-bubble-ai">
                    <strong>[REALAI v3.0]</strong> &nbsp;·&nbsp; Gemini 2.5 Flash<br>
                    Corpus activo: <em>{articulo_seleccionado}</em><br>
                    <span style="color:#4A5568; font-size:0.8rem;">Los países mencionados en tu consulta se resaltarán automáticamente en el globo.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.historial_ia:
                    if msg["rol"] == "usuario":
                        st.markdown(f'<div class="rp-chat-label">Analista</div><div class="rp-chat-bubble-user">{msg["texto"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="rp-chat-label">RealPolitik AI</div><div class="rp-chat-bubble-ai">{msg["texto"]}</div>', unsafe_allow_html=True)

        col_input_btn, col_clear = st.columns([3, 1])
        with col_clear:
            if st.button("Limpiar", use_container_width=True):
                st.session_state.historial_ia = []
                st.session_state.globe_countries = []
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

            instrucciones = f"""Actúas como el consultor/analista en jefe de REALPOLITIK.
Tono frío, analítico, profundo y absolutamente objetivo.
Usa el corpus documental provisto como fuente primaria.

CORPUS:
{contexto_documento}

INSTRUCCIÓN ESPECIAL: Al final de tu respuesta, añade siempre una línea con el formato exacto:
PAÍSES_MAPA: [lista de países relevantes separados por coma en inglés, ej: United States, Russia, China]
Si no hay países relevantes, escribe: PAÍSES_MAPA: ninguno"""

            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_usuario,
                    config=types.GenerateContentConfig(system_instruction=instrucciones, temperature=0.3)
                )
                respuesta_completa = response.text

                # Extraer países del mapa
                if "PAÍSES_MAPA:" in respuesta_completa:
                    partes = respuesta_completa.split("PAÍSES_MAPA:")
                    respuesta_ia = partes[0].strip()
                    paises_raw = partes[1].strip()
                    if paises_raw.lower() != "ninguno":
                        st.session_state.globe_countries = [p.strip() for p in paises_raw.split(",") if p.strip()]
                    else:
                        st.session_state.globe_countries = []
                else:
                    respuesta_ia = respuesta_completa
                    st.session_state.globe_countries = []

            except Exception as e:
                respuesta_ia = f"⚠️ Error del Sistema: {str(e)}"
                st.session_state.globe_countries = []

            st.session_state.historial_ia.append({"rol": "sistema", "texto": respuesta_ia})
            st.rerun()

    with col_globo:
        st.markdown('<span class="rp-seccion-label">Mapa Geopolítico · Vista 3D</span>', unsafe_allow_html=True)

        paises_js = json.dumps(st.session_state.globe_countries)

        globo_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #080A0F; overflow: hidden; }}
  canvas {{ display: block; }}
  #globe-container {{ width: 100%; height: 430px; position: relative; cursor: grab; }}
  #globe-container:active {{ cursor: grabbing; }}
  #status {{
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #4A5568;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    white-space: nowrap;
    pointer-events: none;
  }}
  #countries-label {{
    position: absolute;
    top: 10px;
    left: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #C8A96E;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    pointer-events: none;
    line-height: 1.6;
    max-width: 200px;
  }}
</style>
</head>
<body>
<div id="globe-container">
  <canvas id="globe"></canvas>
  <div id="countries-label"></div>
  <div id="status">Arrastra para rotar · Scroll para zoom</div>
</div>
<script>
const canvas = document.getElementById('globe');
const ctx = canvas.getContext('2d');
const container = document.getElementById('globe-container');

// Países a resaltar (desde Python)
const HIGHLIGHT_COUNTRIES = {paises_js};

// Coordenadas aproximadas de países (ISO → [lat, lon])
const COUNTRY_COORDS = {{
  "United States": [37.09, -95.71],
  "Russia": [61.52, 105.31],
  "China": [35.86, 104.19],
  "Germany": [51.16, 10.45],
  "United Kingdom": [55.37, -3.43],
  "France": [46.22, 2.21],
  "Japan": [36.20, 138.25],
  "Saudi Arabia": [23.88, 45.07],
  "Brazil": [-14.23, -51.92],
  "India": [20.59, 78.96],
  "Venezuela": [6.42, -66.58],
  "Iran": [32.42, 53.68],
  "Turkey": [38.96, 35.24],
  "Ukraine": [48.37, 31.16],
  "Israel": [31.04, 34.85],
  "South Africa": [-30.55, 22.93],
  "Argentina": [-38.41, -63.61],
  "Mexico": [23.63, -102.55],
  "Canada": [56.13, -106.34],
  "Australia": [-25.27, 133.77],
  "Spain": [40.46, -3.74],
  "Italy": [41.87, 12.56],
  "Netherlands": [52.13, 5.29],
  "Switzerland": [46.81, 8.22],
  "Egypt": [26.82, 30.80],
  "Nigeria": [9.08, 8.67],
  "Qatar": [25.35, 51.18],
  "United Arab Emirates": [23.42, 53.84],
  "South Korea": [35.90, 127.76],
  "Indonesia": [-0.78, 113.92],
  "Pakistan": [30.37, 69.34],
  "Poland": [51.91, 19.14],
  "Colombia": [4.57, -74.29],
}};

let W, H, R;
let rotX = 0.3, rotY = -0.5;
let isDragging = false, lastX, lastY;
let scale = 1.0;
let animFrame;
let autoRotate = true;

function resize() {{
  W = container.offsetWidth;
  H = container.offsetHeight;
  canvas.width = W;
  canvas.height = H;
  R = Math.min(W, H) * 0.42 * scale;
}}

// Proyección esférica → 2D con rotación
function project(lat, lon) {{
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lon + 180) * Math.PI / 180;
  let x0 = -Math.sin(phi) * Math.cos(theta);
  let y0 = Math.cos(phi);
  let z0 = Math.sin(phi) * Math.sin(theta);
  // Rotar Y
  const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
  const x1 = x0 * cosY + z0 * sinY;
  const z1 = -x0 * sinY + z0 * cosY;
  // Rotar X
  const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
  const y2 = y0 * cosX - z1 * sinX;
  const z2 = y0 * sinX + z1 * cosX;
  return {{
    x: W / 2 + R * x1,
    y: H / 2 - R * y2,
    visible: z2 > -0.1
  }};
}}

function drawGlobe() {{
  ctx.clearRect(0, 0, W, H);

  // Glow ambiente
  const grd = ctx.createRadialGradient(W/2, H/2, R*0.3, W/2, H/2, R*1.1);
  grd.addColorStop(0, 'rgba(200,169,110,0.04)');
  grd.addColorStop(1, 'rgba(8,10,15,0)');
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, W, H);

  // Esfera base
  const sphereGrad = ctx.createRadialGradient(W/2 - R*0.25, H/2 - R*0.25, R*0.05, W/2, H/2, R);
  sphereGrad.addColorStop(0, '#111520');
  sphereGrad.addColorStop(0.6, '#080D14');
  sphereGrad.addColorStop(1, '#04060A');
  ctx.beginPath();
  ctx.arc(W/2, H/2, R, 0, Math.PI * 2);
  ctx.fillStyle = sphereGrad;
  ctx.fill();

  // Borde del globo
  ctx.beginPath();
  ctx.arc(W/2, H/2, R, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(200,169,110,0.15)';
  ctx.lineWidth = 1;
  ctx.stroke();

  // Meridianos
  ctx.strokeStyle = 'rgba(200,169,110,0.06)';
  ctx.lineWidth = 0.5;
  for (let lon = -180; lon <= 180; lon += 30) {{
    ctx.beginPath();
    let first = true;
    for (let lat = -90; lat <= 90; lat += 2) {{
      const p = project(lat, lon);
      if (p.visible) {{
        if (first) {{ ctx.moveTo(p.x, p.y); first = false; }}
        else ctx.lineTo(p.x, p.y);
      }} else {{ first = true; }}
    }}
    ctx.stroke();
  }}

  // Paralelos
  for (let lat = -60; lat <= 60; lat += 30) {{
    ctx.beginPath();
    let first = true;
    for (let lon = -180; lon <= 180; lon += 2) {{
      const p = project(lat, lon);
      if (p.visible) {{
        if (first) {{ ctx.moveTo(p.x, p.y); first = false; }}
        else ctx.lineTo(p.x, p.y);
      }} else {{ first = true; }}
    }}
    ctx.stroke();
  }}

  // Ecuador destacado
  ctx.strokeStyle = 'rgba(200,169,110,0.12)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  let firstEq = true;
  for (let lon = -180; lon <= 180; lon += 1) {{
    const p = project(0, lon);
    if (p.visible) {{
      if (firstEq) {{ ctx.moveTo(p.x, p.y); firstEq = false; }}
      else ctx.lineTo(p.x, p.y);
    }} else {{ firstEq = true; }}
  }}
  ctx.stroke();

  // Puntos de países resaltados
  if (HIGHLIGHT_COUNTRIES.length > 0) {{
    HIGHLIGHT_COUNTRIES.forEach(country => {{
      const coords = COUNTRY_COORDS[country];
      if (!coords) return;
      const p = project(coords[0], coords[1]);
      if (!p.visible) return;

      // Halo exterior
      const halo = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 20);
      halo.addColorStop(0, 'rgba(200,169,110,0.25)');
      halo.addColorStop(1, 'rgba(200,169,110,0)');
      ctx.fillStyle = halo;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 20, 0, Math.PI * 2);
      ctx.fill();

      // Punto central
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#C8A96E';
      ctx.fill();

      // Anillo pulsante (aproximado con opacidad variable)
      const t = Date.now() / 1000;
      const pulse = 0.4 + 0.6 * Math.sin(t * 2);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 8 + 4 * Math.sin(t * 2), 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(200,169,110,${{pulse * 0.5}})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Etiqueta
      ctx.fillStyle = 'rgba(200,169,110,0.9)';
      ctx.font = '9px JetBrains Mono, monospace';
      ctx.letterSpacing = '1px';
      ctx.fillText(country.toUpperCase(), p.x + 10, p.y - 6);
    }});
  }}

  // Estrella polar (ornamento)
  const pole = project(90, 0);
  if (pole.visible) {{
    ctx.beginPath();
    ctx.arc(pole.x, pole.y, 2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(200,169,110,0.4)';
    ctx.fill();
  }}
}}

function animate() {{
  if (autoRotate && !isDragging) {{
    rotY += 0.003;
  }}
  drawGlobe();
  animFrame = requestAnimationFrame(animate);
}}

// Interactividad
canvas.addEventListener('mousedown', e => {{
  isDragging = true;
  autoRotate = false;
  lastX = e.clientX;
  lastY = e.clientY;
  e.preventDefault();
}});
canvas.addEventListener('mousemove', e => {{
  if (!isDragging) return;
  const dx = e.clientX - lastX;
  const dy = e.clientY - lastY;
  rotY += dx * 0.005;
  rotX += dy * 0.005;
  rotX = Math.max(-Math.PI/2, Math.min(Math.PI/2, rotX));
  lastX = e.clientX;
  lastY = e.clientY;
}});
canvas.addEventListener('mouseup', () => {{ isDragging = false; }});
canvas.addEventListener('mouseleave', () => {{ isDragging = false; }});

canvas.addEventListener('wheel', e => {{
  scale *= e.deltaY > 0 ? 0.93 : 1.07;
  scale = Math.max(0.5, Math.min(2.0, scale));
  R = Math.min(W, H) * 0.42 * scale;
  e.preventDefault();
}}, {{ passive: false }});

// Touch
canvas.addEventListener('touchstart', e => {{
  isDragging = true;
  autoRotate = false;
  lastX = e.touches[0].clientX;
  lastY = e.touches[0].clientY;
  e.preventDefault();
}}, {{ passive: false }});
canvas.addEventListener('touchmove', e => {{
  if (!isDragging) return;
  const dx = e.touches[0].clientX - lastX;
  const dy = e.touches[0].clientY - lastY;
  rotY += dx * 0.005;
  rotX += dy * 0.005;
  rotX = Math.max(-Math.PI/2, Math.min(Math.PI/2, rotX));
  lastX = e.touches[0].clientX;
  lastY = e.touches[0].clientY;
  e.preventDefault();
}}, {{ passive: false }});
canvas.addEventListener('touchend', () => {{ isDragging = false; }});

// Label de países
const label = document.getElementById('countries-label');
if (HIGHLIGHT_COUNTRIES.length > 0) {{
  label.innerHTML = '<span style="color:#4A5568;">Foco:</span><br>' + HIGHLIGHT_COUNTRIES.join('<br>');
}} else {{
  label.innerHTML = '<span style="color:#2D3748;">Sin foco activo</span>';
}}

resize();
window.addEventListener('resize', () => {{
  resize();
  R = Math.min(W, H) * 0.42 * scale;
}});
animate();
</script>
</body>
</html>
"""
        st.components.v1.html(globo_html, height=440)
        st.markdown(f"""
        <div style="margin-top:0.5rem;">
            <span class="rp-seccion-label">
                {f"Países en análisis: {', '.join(st.session_state.globe_countries)}" if st.session_state.globe_countries else "Formula una consulta para activar el localizador geopolítico"}
            </span>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# VISTA 4: CONTACTO
# =========================================================================
elif st.session_state.pagina_actual == "Contacto":
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


# =========================================================================
# VISTA 5: MESA EDITORIAL
# =========================================================================
elif st.session_state.pagina_actual == "MesaEditorial":
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


# =========================================================================
# VISTAS DINÁMICAS DE ARTÍCULOS INDIVIDUALES
# =========================================================================
elif st.session_state.pagina_actual in ARTICULOS_DB:
    art_info = ARTICULOS_DB[st.session_state.pagina_actual]

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


# =========================================================================
# PIE DE PÁGINA
# =========================================================================
st.markdown(f"""
<div class="rp-footer">
    <span class="rp-footer-copy">Realpolitik Intelligence Network © 2026 · Documento de Acceso Abierto</span>
    <span class="rp-footer-copy">{coord_display}</span>
</div>
""", unsafe_allow_html=True)
