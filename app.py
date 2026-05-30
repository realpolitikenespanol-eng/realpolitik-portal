import streamlit as st
import os
import json
from google import genai
from google.genai import types

# =========================================================================
# CONFIGURACIÓN DE PÁGINA OBLIGATORIA (DEBE SER LA PRIMERA INSTRUCCIÓN)
# =========================================================================
st.set_page_config(page_title="REALPOLITIK | Portal", layout="wide", initial_sidebar_state="expanded")

# =========================================================================
# GESTIÓN DE BASE DE DATOS LOCAL (PERSISTENCIA JSON)
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
    "Art_Fed": {
        "titulo": "Tasas de Interés y la Parálisis del Ring de la Fed",
        "fecha": "ABRIL 2026",
        "categoria": "Geopolítica Monetaria & Mercados",
        "sinopsis": "Evaluación del spread de rendimiento institucional en los mercados soberanos primarios. Analizamos el impacto macroeconómico del anclaje de taxas y los dilemas estructurales que enfrenta la Reserva Federal ante la deuda pública global.",
        "imagen": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=800&auto=format&fit=crop",
        "contenido": "Aquí se desarrollará el cuerpo completo del informe sobre la Reserva Federal, las operaciones de mercado abierto y las implicaciones operativas en las mesas de dinero internacionales."
    },
    "Art_Taiwan": {
        "titulo": "Soberanía Tecnológica en los Estrechos de Taiwán",
        "fecha": "MARZO 2026",
        "categoria": "Weltpolitik & Teoría del Estado",
        "sinopsis": "Disección de la cadena de suministro global de semiconductores avanzados como vector de fuerza dura. Un estudio sobre el control territorial, los cuellos de botella de la infraestructura crítica y el nuevo realismo geopolítico.",
        "imagen": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop",
        "contenido": "Aquí se desarrollará el cuerpo completo del análisis estratégico respecto al Estrecho de Taiwán, evaluando los modelos de dependencia logística de ASML, TSMC y el balance defensivo regional."
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

# Inicializar Base de Datos Viva
ARTICULOS_DB = cargar_articulos()

# URL del Palacio del Parlamento (Bucarest) para el Bloque Hero
URL_HERO_NUEVA = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Bucarest_-_Palau_del_Parlament.png/960px-Bucarest_-_Palau_del_Parlament.png"

# Control de Estado de Navegación por URL y Session State
if "nav" in st.query_params:
    st.session_state.pagina_actual = st.query_params["nav"]
elif "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

if "editorial_autenticado" not in st.session_state:
    st.session_state.editorial_autenticado = False

if "historial_ia" not in st.session_state:
    st.session_state.historial_ia = []

# =========================================================================
# INYECCIÓN DE ESTILOS CSS AVANZADOS & RESPONSIVOS
# =========================================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Ocultar el menú superior derecho (hamburguesa) y el ícono de estado */
    [data-testid="stToolbar"] {{
        visibility: hidden;
        display: none;
    }}

    /* Ocultar la marca de agua "Made with Streamlit" abajo a la derecha */
    footer {{
        visibility: hidden;
        display: none;
    }}

    /* Ocultar el botón de "Deploy" si aparece en la barra superior */
    [data-testid="stDecoration"] {{
        visibility: hidden;
        display: none;
    }}

    .stApp {{
        background-color: #0b0d10 !important;
        color: #cbd5e1;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; }}
    .block-container {{ padding-top: 0rem !important; padding-bottom: 2rem !important; }}
    html, body, [class*="st-text"], .stMarkdown p, p {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 400; line-height: 1.7; color: #cbd5e1;
    }}

    /* --- BARRA DE NAVEGACIÓN SUPERIOR RESPONSIVA --- */
    .nav-superior-container {{
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        max-width: 1000px; 
        margin: 0 auto; 
        padding: 1.5rem 0; 
        gap: 1rem;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }}
    .nav-superior-container::-webkit-scrollbar {{
        display: none; /* Ocultar barra en móviles para diseño limpio */
    }}
    .nav-enlace {{
        font-family: 'Instrument Serif', serif !important; 
        font-size: 1.65rem !important;
        color: #64748b !important; 
        text-decoration: none !important; 
        transition: color 0.2s ease;
        background: none; 
        border: none; 
        cursor: pointer; 
        white-space: nowrap;
        padding: 0.2rem 0.5rem;
    }}
    .nav-enlace:hover {{ color: #ffffff !important; }}
    .nav-enlace-activo {{ color: #ffffff !important; border-bottom: 2px solid #ffffff; }}

    /* --- PORTADA EN BLOQUE HERO RESPONSIVO --- */
    .hero-container {{
        width: 100%; 
        min-height: 30vh;
        height: auto;
        background-image: linear-gradient(to bottom, rgba(11, 13, 16, 0.4) 0%, rgba(11, 13, 16, 1) 100%), url('{URL_HERO_NUEVA}');
        background-repeat: no-repeat; 
        background-position: center center; 
        background-size: cover;
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center;
        margin-bottom: 2.5rem; 
        padding: 3rem 1.5rem; 
        border-radius: 12px; 
        border: 1px solid #1e293b;
    }}
    .titulo-header {{
        font-family: 'Instrument Serif', serif !important; 
        font-size: 5.5rem !important;
        font-weight: 400; 
        text-align: center; 
        letter-spacing: 0.05em; 
        margin: 0; 
        color: #ffffff;
        text-transform: uppercase; 
        text-shadow: 3px 3px 20px rgba(0,0,0,0.9);
        line-height: 1;
    }}
    .subtitulo-header {{
        font-family: 'Instrument Serif', serif !important; 
        font-size: 2.2rem !important;
        font-style: italic; 
        text-align: center; 
        color: #e2e8f0; 
        margin-top: 1rem; 
        margin-bottom: 0;
        text-shadow: 2px 2px 15px rgba(0,0,0,0.9);
        line-height: 1.2;
    }}

    .declaracion-manifiesto {{
        font-family: 'Inter', sans-serif !important; 
        font-size: 1.25rem !important;
        font-weight: 300 !important; 
        line-height: 1.8; 
        color: #e2e8f0; 
        text-align: justify;
        border-bottom: 1px solid #1e293b; 
        padding-bottom: 2rem; 
        margin-bottom: 2rem;
    }}
    .cita-editorial {{
        font-family: 'Instrument Serif', serif !important; 
        font-size: 2.8rem !important;
        line-height: 1.2; 
        color: #ffffff; 
        font-style: italic; 
        margin-top: 1.5rem; 
        margin-bottom: 1.5rem; 
        text-align: left;
    }}
    h2, .stMarkdown h2 {{
        font-family: 'Instrument Serif', serif !important; 
        font-size: 2.5rem !important;
        font-weight: 400 !important; 
        color: #ffffff !important; 
        margin-top: 0.5rem !important; 
        margin-bottom: 1.5rem !important;
    }}

    /* --- TARJETAS FLEXIBLES --- */
    .tarjeta-analitica {{
        position: relative; 
        border: 1px solid #1e293b; 
        border-radius: 8px; 
        padding: 2rem; 
        margin-bottom: 1.5rem;
        background-size: cover; 
        background-position: center; 
        overflow: hidden; 
        transition: transform 0.3s ease, border-color 0.3s ease;
    }}
    .tarjeta-analitica:hover {{ transform: translateY(-4px); border-color: #334155; }}
    .tarjeta-1 {{ background-image: linear-gradient(to right, rgba(11, 13, 16, 0.95) 50%, rgba(11, 13, 16, 0.4) 100%), url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop'); }}
    .tarjeta-2 {{ background-image: linear-gradient(to right, rgba(11, 13, 16, 0.95) 50%, rgba(11, 13, 16, 0.4) 100%), url('https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=800&auto=format&fit=crop'); }}
    .tarjeta-3 {{ background-image: linear-gradient(to right, rgba(11, 13, 16, 0.95) 50%, rgba(11, 13, 16, 0.3) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop'); cursor: pointer; }}
    .tarjeta-analitica h4 {{ font-family: 'Instrument Serif', serif !important; font-size: 1.9rem !important; color: #ffffff; margin-top: 0; margin-bottom: 0.75rem; }}
    .tarjeta-analitica p {{ font-size: 0.92rem; color: #cbd5e1; margin-bottom: 0; max-width: 100%; }}

    /* --- COMPONENTES MENORES --- */
    .mini-cubiculo-link {{ text-decoration: none !important; color: inherit !important; display: block; height: 100%; }}
    .mini-cubiculo {{
        background: #11141a; 
        border: 1px solid #1e293b; 
        border-radius: 6px; 
        padding: 1.2rem; 
        height: 100%;
        transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
        margin-bottom: 1rem;
    }}
    .mini-cubiculo:hover {{ background: #161a22; border-color: #475569; transform: translateY(-2px); }}
    .mini-cubiculo h5 {{ font-family: 'Instrument Serif', serif !important; font-size: 1.35rem !important; color: #ffffff; margin-top: 0.2rem; margin-bottom: 0.5rem; line-height: 1.2; }}
    .micro-label {{ font-family: 'Inter', sans-serif !important; font-size: 0.72rem !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #64748b; margin-bottom: 0.3rem; }}

    /* --- FILAS EDITORIALES LÍQUIDAS --- */
    .reporte-fila {{ 
        display: flex; 
        flex-direction: row;
        justify-content: space-between; 
        align-items: center; 
        padding: 2.5rem 0; 
        border-bottom: 1px solid #1e293b; 
        gap: 3rem; 
    }}
    .reporte-info-bloque {{ flex: 1.4; }}
    .reporte-imagen-bloque {{ flex: 0.8; height: 200px; border-radius: 6px; overflow: hidden; border: 1px solid #1e293b; width: 100%; }}
    .reporte-imagen-bloque img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }}
    .reporte-fila:hover .reporte-imagen-bloque img {{ transform: scale(1.03); }}
    .reporte-meta {{ display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.75rem; color: #64748b; font-weight: 500; letter-spacing: 0.05em; margin-bottom: 0.5rem; }}
    .reporte-titulo {{ font-family: 'Instrument Serif', serif !important; font-size: 2.2rem !important; color: #ffffff !important; line-height: 1.15; margin-top: 0.2rem; margin-bottom: 0.75rem; text-decoration: none !important; }}
    .reporte-titulo:hover {{ color: #cbd5e1 !important; }}
    .reporte-sinopsis {{ font-size: 0.92rem; color: #94a3b8; line-height: 1.6; text-align: justify; }}

    /* --- CHAT --- */
    .globo-chat-usuario {{ background: #1e293b; border: 1px solid #334155; padding: 1rem; border-radius: 8px 8px 0px 8px; margin-bottom: 1rem; color: #f1f5f9; font-size: 0.9rem; }}
    .globo-chat-sistema {{ background: #11141a; border: 1px solid #1e293b; padding: 1rem; border-radius: 8px 8px 8px 0px; margin-bottom: 1rem; color: #cbd5e1; font-size: 0.9rem; border-left: 3px solid #64748b; }}

    /* =========================================================================
       SOPORTE ESPECÍFICO PARA DISPOSITIVOS MÓVILES (MEDIA QUERIES)
       ========================================================================= */
    @media (max-width: 768px) {{
        .nav-superior-container {{
            justify-content: flex-start;
            padding: 1rem 0.5rem;
        }}
        .nav-enlace {{
            font-size: 1.25rem !important;
        }}
        .hero-container {{
            padding: 2rem 1rem;
            min-height: 20vh;
        }}
        .titulo-header {{
            font-size: 2.5rem !important;
        }}
        .subtitulo-header {{
            font-size: 1.35rem !important;
        }}
        .declaracion-manifiesto {{
            font-size: 1.1rem !important;
            text-align: left;
        }}
        .cita-editorial {{
            font-size: 1.8rem !important;
        }}
        .reporte-fila {{
            flex-direction: column-reverse !important;
            gap: 1.5rem;
            padding: 1.5rem 0;
        }}
        .reporte-imagen-bloque {{
            height: 180px;
        }}
        .reporte-titulo {{
            font-size: 1.75rem !important;
        }}
        .tarjeta-analitica h4 {{
            font-size: 1.5rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# MENÚ DE NAVEGACIÓN SUPERIOR (Cinco Enlaces Dinámicos)
# =========================================================================
activo_inicio = "nav-enlace-activo" if st.session_state.pagina_actual == "Inicio" else ""
activo_articulos = "nav-enlace-activo" if st.session_state.pagina_actual == "Articulos" else ""
activo_ia = "nav-enlace-activo" if st.session_state.pagina_actual == "AuditoriaIA" else ""
activo_contacto = "nav-enlace-activo" if st.session_state.pagina_actual == "Contacto" else ""
activo_editorial = "nav-enlace-activo" if st.session_state.pagina_actual == "MesaEditorial" else ""

st.markdown(f"""
    <div class="nav-superior-container">
        <a href="?nav=Inicio" target="_self" class="nav-enlace {activo_inicio}">Menú Principal</a>
        <a href="?nav=Articulos" target="_self" class="nav-enlace {activo_articulos}">Artículos</a>
        <a href="?nav=AuditoriaIA" target="_self" class="nav-enlace {activo_ia}">Briefing Room</a>
        <a href="?nav=Contacto" target="_self" class="nav-enlace {activo_contacto}">Contacto</a>
        <a href="?nav=MesaEditorial" target="_self" class="nav-enlace {activo_editorial}">Mesa Editorial</a>
    </div>
    <hr style="border-top: 1px solid #1e293b; margin-top:0rem; margin-bottom:2.5rem;">
""", unsafe_allow_html=True)

# =========================================================================
# BARRA LATERAL NATIVA SINCRONIZADA
# =========================================================================
with st.sidebar:
    st.markdown('<div class="micro-label">Navegación del Sistema</div>', unsafe_allow_html=True)
    opciones_sidebar = ["Inicio", "Artículos", "Briefing Room", "Contacto", "Mesa Editorial"]
    
    idx_defecto = 0
    if st.session_state.pagina_actual == "Articulos" or st.session_state.pagina_actual.startswith("Art_"):
        idx_defecto = 1
    elif st.session_state.pagina_actual == "AuditoriaIA":
        idx_defecto = 2
    elif st.session_state.pagina_actual == "Contacto":
        idx_defecto = 3
    elif st.session_state.pagina_actual == "MesaEditorial":
        idx_defecto = 4
        
    seleccion = st.sidebar.radio("Ir a:", opciones_sidebar, index=idx_defecto)
    
    if seleccion == "Inicio" and st.session_state.pagina_actual != "Inicio":
        st.session_state.pagina_actual = "Inicio"; st.query_params["nav"] = "Inicio"; st.rerun()
    elif seleccion == "Archivo de Artículos" and not st.session_state.pagina_actual.startswith("Art"):
        st.session_state.pagina_actual = "Articulos"; st.query_params["nav"] = "Articulos"; st.rerun()
    elif seleccion == "Briefing Room" and st.session_state.pagina_actual != "AuditoriaIA":
        st.session_state.pagina_actual = "AuditoriaIA"; st.query_params["nav"] = "AuditoriaIA"; st.rerun()
    elif seleccion == "Contacto" and st.session_state.pagina_actual != "Contacto":
        st.session_state.pagina_actual = "Contacto"; st.query_params["nav"] = "Contacto"; st.rerun()
    elif seleccion == "Mesa Editorial" and st.session_state.pagina_actual != "MesaEditorial":
        st.session_state.pagina_actual = "MesaEditorial"; st.query_params["nav"] = "MesaEditorial"; st.rerun()

# =========================================================================
# LÓGICA DE ENTRADA Y RENDERIZADO DE VISTAS
# =========================================================================

# --- VISTA 1: MENU PRINCIPAL ---
if st.session_state.pagina_actual == "Inicio":
    st.markdown(f"""<div class="hero-container"><h1 class="titulo-header">REALPOLITIK</h1><p class="subtitulo-header">Economía, Geopolítica & Análisis de Poder</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="declaracion-manifiesto">En un entorno global definido por la volatilidad sistémica, los sesgos ideológicos y la saturación de ruido informativo, la comprensión del poder requiere un método riguroso. <strong>RealPolitik</strong> no es un espacio de opinión; mostramos la realidad, los datos y análisis objetivos para que tu generes tus propias perspectivas basadas en la realidad. Abordamos la intersección donde las dinámicas de los mercados financieros y la macroeconomía chocan con la arquitectura de la política de Estados y el diseño de las instituciones.</div>""", unsafe_allow_html=True)
    
    # Usamos columnas nativas que adaptan su disposición automáticamente en pantallas chicas
    col_izq, col_der = st.columns([1.2, 1.1], gap="large")
    with col_izq:
        st.markdown('<h2>El Enfoque Estructural</h2>', unsafe_allow_html=True)
        st.markdown('<div class="cita-editorial">"Las ideas guían el debate, pero las instituciones y los flujos de capital determinan el desenlace."</div>', unsafe_allow_html=True)
        if st.button("EXPLORA NUESTROS ARTÍCULOS COMPLETOS AQUÍ", use_container_width=True):
            st.session_state.pagina_actual = "Articulos"; st.query_params["nav"] = "Articulos"; st.rerun()
            
        st.markdown("<br><div class='micro-label'>PUBLICACIONES MÁS RECIENTES</div>", unsafe_allow_html=True)
        
        # Grid adaptativo para los tres artículos de abajo
        claves = list(ARTICULOS_DB.keys())[-3:]
        for k in claves:
            st.markdown(f"""<a href="?nav={k}" target="_self" class="mini-cubiculo-link"><div class="mini-cubiculo"><div class="micro-label">{ARTICULOS_DB[k]["fecha"]}</div><h5>{ARTICULOS_DB[k]["titulo"]}</h5><p style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">{ARTICULOS_DB[k]["sinopsis"][:55]}...</p></div></a>""", unsafe_allow_html=True)

    with col_der:
        st.markdown('<h2>Líneas de Investigación</h2>', unsafe_allow_html=True)
        st.markdown("""<div class="tarjeta-analitica tarjeta-1"><div class="micro-label" style="color: #94a3b8;">ÁREA TÉCNICA I</div><h4>Geopolítica Monetaria & Mercados</h4><p>Modelado e investigación de la hegemonía del dólar, mecánicas de mercado y bancos centrales.</p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="tarjeta-analitica tarjeta-2"><div class="micro-label" style="color: #94a3b8;">ÁREA TÉCNICA II</div><h4>Weltpolitik & Teoría del Estado</h4><p>Análisis de riesgo y proyecciones de poder bajo la óptica de la estabilidad institucional.</p></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="tarjeta-analitica tarjeta-3"><div class="micro-label" style="color: #cbd5e1;">LABORATORIO DE CÓMPUTO</div><h4>Auditoría de Datos con Inteligencia Artificial</h4><p>Acceder a la terminal de indexación avanzada para interrogar nuestro corpus completo de reportes institucionales mediante redes neuronales. Click abajo para iniciar la consola.</p></div>""", unsafe_allow_html=True)
        if st.button("INICIAR AUDITORÍA DE DATOS (IA)", use_container_width=True):
            st.session_state.pagina_actual = "AuditoriaIA"
            st.query_params["nav"] = "AuditoriaIA"
            st.rerun()

# --- VISTA 2: PORTAL DE ARTÍCULOS ---
elif st.session_state.pagina_actual == "Articulos":
    st.markdown('<h2>Archivo Global de Reportes</h2>', unsafe_allow_html=True)
    categorias = ["Todos los Reportes", "Geopolítica Monetaria & Mercados", "Weltpolitik & Teoría del Estado"]
    filtro_seleccionado = st.pills("Filtrar por Línea de Investigación:", categorias, default="Todos los Reportes")
    
    for art_id, info in ARTICULOS_DB.items():
        if filtro_seleccionado != "Todos los Reportes" and info["categoria"] != filtro_seleccionado:
            continue
        st.markdown(f"""
        <div class="reporte-fila">
            <div class="reporte-info-bloque">
                <div class="reporte-meta"><span>{info["fecha"]}</span><span>•</span><span style="color: #cbd5e1; text-transform: uppercase; font-size: 0.7rem; letter-spacing:0.1em;">{info["categoria"]}</span></div>
                <a href="?nav={art_id}" target="_self" style="text-decoration: none;"><h3 class="reporte-titulo">{info["titulo"]}</h3></a>
                <p class="reporte-sinopsis">{info["sinopsis"]}</p>
                <div style="margin-top: 1.2rem;"><a href="?nav={art_id}" target="_self" style="color: #ffffff; font-size: 0.85rem; font-weight: 500; text-decoration: none; border-bottom: 1px solid #64748b; padding-bottom: 2px;">Leer Reporte Completo ➔</a></div>
            </div>
            <div class="reporte-imagen-bloque"><img src="{info["imagen"]}" alt="Reporte Ilustración"></div>
        </div>
        """, unsafe_allow_html=True)

# --- VISTA 3: AUDITORÍA IA ---
elif st.session_state.pagina_actual == "AuditoriaIA":
    st.markdown('<h2>The Briefing Room</h2>', unsafe_allow_html=True)
    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
    
    col_panel, col_consola = st.columns([1, 1.4], gap="large")
    with col_panel:
        st.markdown('<div class="micro-label">FILTRACIÓN DE CONTENIDOS</div>', unsafe_allow_html=True)
        titulos_articulos = [info["titulo"] for info in ARTICULOS_DB.values()]
        articulo_seleccionado = st.selectbox("Seleccionar Artículo Base:", ["Todo el Corpus Disponible"] + titulos_articulos)
        if st.button("LIMPIAR REGISTROS DEL CHAT", use_container_width=True):
            st.session_state.historial_ia = []
            st.rerun()

    with col_consola:
        contenedor_chat = st.container(height=350, border=True)
        with contenedor_chat:
            if not st.session_state.historial_ia:
                st.markdown(f"""<div class="globo-chat-sistema"><strong>[REALAI v2.0]</strong> Basado en Gemini AI. Contexto actual establecido en: <em>{articulo_seleccionado}</em>.</div>""", unsafe_allow_html=True)
            else:
                for msg in st.session_state.historial_ia:
                    clase = "globo-chat-usuario" if msg["rol"] == "usuario" else "globo-chat-sistema"
                    prefijo = "<strong>Analista:</strong> " if msg["rol"] == "usuario" else "<strong>RealPolitik AI:</strong> "
                    st.markdown(f"""<div class="{clase}">{prefijo}{msg['texto']}</div>""", unsafe_allow_html=True)
                    
        prompt_usuario = st.chat_input("Escriba su pregunta...")
        if prompt_usuario:
            if not api_key:
                st.error("Falta la API Key en el entorno del servidor.")
                st.stop()
            st.session_state.historial_ia.append({"rol": "usuario", "texto": prompt_usuario})
            
            if articulo_seleccionado == "Todo el Contenido Disponible":
                contexto_documento = "\n\n".join([f"Articulo: {a['titulo']}\nContenido: {a['contenido']}" for a in ARTICULOS_DB.values()])
            else:
                id_art = [k for k, v in ARTICULOS_DB.items() if v["titulo"] == articulo_seleccionado][0]
                contexto_documento = f"Articulo: {articulo_seleccionado}\nContenido: {ARTICULOS_DB[id_art]['contenido']}"
            
            instrucciones = f"Actúas como el consultor/analista en jefe de REALPOLITIK. Tono frío, analítico, profundo y, sobre todo, absolutamente objetivo. Usa el corpus:\n{contexto_documento}"
            
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt_usuario,
                    config=types.GenerateContentConfig(system_instruction=instrucciones, temperature=0.3)
                )
                respuesta_ia = response.text
            except Exception as e:
                respuesta_ia = f"⚠️ Error del Sistema (google-genai): {str(e)}"
            
            st.session_state.historial_ia.append({"rol": "sistema", "texto": respuesta_ia})
            st.rerun()

# --- VISTA 4: CONTACTO ---
elif st.session_state.pagina_actual == "Contacto":
    st.markdown('<h2>Oficina de Enlace Corporativo</h2>', unsafe_allow_html=True)
    col_form, col_info = st.columns([1.4, 0.9], gap="large")
    with col_form:
        with st.form("formulario_contacto", clear_on_submit=True):
            tipo_enlace = st.selectbox("Naturaleza:", ["Consulta Académica / Proyectos de Investigación", "Propuesta de Colaboración Editorial"])
            nombre = st.text_input("Nombre Completo:")
            correo = st.text_input("Dirección de Correo:")
            asunto = st.text_input("Asunto:")
            mensaje = st.text_area("Mensaje:")
            if st.form_submit_button("Enviar Mensaje ➔", use_container_width=True):
                st.success("Requerimiento enviado exitosamente.")

# --- VISTA 5: MESA EDITORIAL INTERNA ---
elif st.session_state.pagina_actual == "MesaEditorial":
    st.markdown('<h2>Mesa Editorial y Control de Contenido</h2>', unsafe_allow_html=True)
    
    if not st.session_state.editorial_autenticado:
        st.markdown("<p style='color: #94a3b8;'>Ingrese las credenciales del panel de control de RealPolitik para continuar.</p>", unsafe_allow_html=True)
        col_login, _ = st.columns([1, 1.5])
        with col_login:
            with st.form("credenciales_editor"):
                input_user = st.text_input("Nombre de Usuario Editorial:")
                input_pass = st.text_input("Clave de Acceso Mecanizada:", type="password")
                if st.form_submit_button("AUTENTICAR PORTAL", use_container_width=True):
                    if input_user == "admin" and input_pass == "realpolitik2026":
                        st.session_state.editorial_autenticado = True
                        st.success("Acceso concedido.")
                        st.rerun()
                    else:
                        st.error("Credenciales de firma inválidas.")
        st.stop()
        
    st.sidebar.button("CERRAR SESIÓN EDITORIAL 🔒", on_click=lambda: st.session_state.update({"editorial_autenticado": False, "pagina_actual": "Inicio"}))
    
    tab_crear, tab_editar = st.tabs(["✍️ Publicar Nuevo Ensayo", "⚙️ Modificar / Eliminar Existentes"])
    
    with tab_crear:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("nuevo_articulo_form"):
            new_title = st.text_input("Título del Reporte:")
            new_date = st.text_input("Fecha de Edición (Ej: JUNIO 2026):", value="MAYO 2026")
            new_cat = st.selectbox("Línea de Investigación:", ["Geopolítica Monetaria & Mercados", "Weltpolitik & Teoría del Estado"])
            new_sinopsis = st.text_area("Sinopsis Analítica (Texto de Tarjeta):", max_chars=350)
            new_img = st.text_input("URL de Imagen de Portada (Unsplash / Wikimedia):", value="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop")
            new_content = st.text_area("Cuerpo Estructural del Ensayo (Contenido Completo):", height=300)
            
            if st.form_submit_button("EMITIR Y PUBLICAR REPORTE 🚀", use_container_width=True):
                if not new_title or not new_content:
                    st.error("El Título y el Cuerpo del ensayo son obligatorios para la indexación.")
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
                    st.success(f"Artículo '{new_title}' publicado con éxito en el archivo global.")
                    st.rerun()

    with tab_editar:
        st.markdown("<br>", unsafe_allow_html=True)
        if not ARTICULOS_DB:
            st.info("No hay artículos cargados en la base de datos local.")
        else:
            art_a_editar = st.selectbox("Seleccione el Ensayo que desea Modificar o Retirar:", list(ARTICULOS_DB.keys()), format_func=lambda x: ARTICULOS_DB[x]["titulo"])
            
            if st.button("🚨 ELIMINAR ARTÍCULO DEFINITIVAMENTE", use_container_width=True):
                del ARTICULOS_DB[art_a_editar]
                guardar_articulos(ARTICULOS_DB)
                st.warning("Artículo removido del registro.")
                st.rerun()
            
            st.markdown("<hr style='border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)
            
            with st.form("editar_articulo_form"):
                edit_title = st.text_input("Modificar Título:", value=ARTICULOS_DB[art_a_editar]["titulo"])
                edit_date = st.text_input("Modificar Fecha:", value=ARTICULOS_DB[art_a_editar]["fecha"])
                edit_cat = st.selectbox("Modificar Categoría:", ["Geopolítica Monetaria & Mercados", "Weltpolitik & Teoría del Estado"], index=0 if ARTICULOS_DB[art_a_editar]["categoria"] == "Geopolítica Monetaria & Mercados" else 1)
                edit_sinopsis = st.text_area("Modificar Sinopsis:", value=ARTICULOS_DB[art_a_editar]["sinopsis"])
                edit_img = st.text_input("Modificar URL Imagen:", value=ARTICULOS_DB[art_a_editar]["imagen"])
                edit_content = st.text_area("Modificar Contenido Completo:", value=ARTICULOS_DB[art_a_editar]["contenido"], height=250)
                
                if st.form_submit_button("SALVAGUARDAR CAMBIOS EDITORIALES 💾", use_container_width=True):
                    ARTICULOS_DB[art_a_editar] = {
                        "titulo": edit_title,
                        "fecha": edit_date.upper(),
                        "categoria": edit_cat,
                        "sinopsis": edit_sinopsis,
                        "imagen": edit_img,
                        "contenido": edit_content
                    }
                    guardar_articulos(ARTICULOS_DB)
                    st.success("Cambios estructurales aplicados correctamente.")
                    st.rerun()

# --- VISTAS DINÁMICAS DE LECTURA (PARA ARTÍCULOS INDIVIDUALES) ---
elif st.session_state.pagina_actual in ARTICULOS_DB:
    art_info = ARTICULOS_DB[st.session_state.pagina_actual]
    st.markdown(f"<p style='color: #64748b; font-size: 0.8rem; font-weight: 600; letter-spacing:0.12em;'>{art_info['fecha']} | {art_info['categoria'].upper()}</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family: \"Instrument Serif\", serif; font-size: 3rem; color: white; line-height: 1.1; margin-bottom: 2rem;'>{art_info['titulo']}</h1>", unsafe_allow_html=True)
    st.image(art_info['imagen'], use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    contenido_completo = art_info['contenido']
    
    # Comprobamos si el artículo solicita explícitamente el gráfico intercalado en el texto
    if "[GRAFICO_INTERACTIVO_RESERVAS]" in contenido_completo and "datos_grafica" in art_info and art_info["datos_grafica"].strip():
        import pandas as pd
        import plotly.express as px
        import io
        
        # Dividir el artículo en bloque pre-gráfico y bloque post-gráfico
        parte_alta, parte_baja = contenido_completo.split("[GRAFICO_INTERACTIVO_RESERVAS]")
        
        # 1. Renderizar primera parte del ensayo
        st.markdown(f"<div style='font-size: 1.15rem; color: #e2e8f0; line-height: 1.8; text-align: justify;'>{parte_alta}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Construir y Renderizar Gráfica de Plotly Interactiva
        try:
            data_stream = io.StringIO(art_info["datos_grafica"].strip())
            df = pd.read_csv(data_stream)
            
            fig = px.line(
                df, 
                x=df.columns[0], 
                y=df.columns[1], 
                template="plotly_dark",
                color_discrete_sequence=["#fbbf24"] # Color dorado/ámbar para las reservas metálicas
            )
            
            fig.update_layout(
                paper_bgcolor="#0b0d10",
                plot_bgcolor="#11141a",
                font_family="Inter",
                hovermode="x unified",
                margin=dict(l=30, r=20, t=30, b=30),
                showlegend=False
            )
            fig.update_xaxes(showgrid=True, gridcolor="#1e293b", linecolor="#334155", title_text="Año de Medición")
            fig.update_yaxes(showgrid=True, gridcolor="#1e293b", linecolor="#334155", title_text="Reservas de Oro de EE.UU. (Tons)")
            
            st.markdown("<div class='micro-label' style='text-align:center;'>INDICADOR CRÍTICO: AGOTAMIENTO DE COLATERALES EN FORT KNOX (1944-1971)</div>", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Fallo en la lectura de vectores del gráfico: {e}")
            
        # 3. Renderizar segunda parte del ensayo
        st.markdown(f"<div style='font-size: 1.15rem; color: #e2e8f0; line-height: 1.8; text-align: justify;'>{parte_baja}</div>", unsafe_allow_html=True)
        
    else:
        # Renderizado clásico en caso de artículos normales que no usan este marcador dinámico
        st.markdown(f"<div style='font-size: 1.15rem; color: #e2e8f0; line-height: 1.8; text-align: justify;'>{contenido_completo}</div>", unsafe_allow_html=True)
        
    st.markdown("<br><hr style='border-top: 1px solid #1e293b;'><br>", unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL ARCHIVO DE ARTÍCULOS", use_container_width=True):
        st.session_state.pagina_actual = "Articulos"; st.query_params["nav"] = "Articulos"; st.rerun()

# PIE DE PÁGINA GLOBAL
st.markdown("<br><br><div style='border-top: 1px solid #1e293b; padding-top: 1rem; text-align: center; font-size: 0.8rem; color: #475569; letter-spacing: 0.05em;'>REALPOLITIK INTELLIGENCE NETWORK © 2026 | DOCUMENTO DE ACCESO ABIERTO</div>", unsafe_allow_html=True)
# PIE DE PÁGINA GLOBAL
st.markdown("<br><br><div style='border-top: 1px solid #1e293b; padding-top: 1rem; text-align: center; font-size: 0.8rem; color: #475569; letter-spacing: 0.05em;'>REALPOLITIK INTELLIGENCE 2026 | DOCUMENTO DE ACCESO ABIERTO</div>", unsafe_allow_html=True)
