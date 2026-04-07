import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN - NOMBRES REALES DE LOS PROYECTOS
# ============================================================

# Cada idea tiene: nombre, pilar (categoría) y color
PROYECTOS = [
    {"nombre": "Global Commercial Meeting 2026", "pilar": "Customer", "color": "#1a5632"},
    {"nombre": "Communication Milestones & Events", "pilar": "Customer", "color": "#237a45"},
    {"nombre": "New Campaign: From Fiber to Form", "pilar": "Customer", "color": "#2a8f52"},
    {"nombre": "Communication Focus: Building Our Future Together", "pilar": "Customer", "color": "#35a55f"},
    {"nombre": "Presentations: Global / By Market / Mill", "pilar": "Customer", "color": "#40bb6c"},
    {"nombre": "Automatization through IA: Database, Balance Scorecard, Dashboard, Reports", "pilar": "Growth & Innovation", "color": "#2563eb"},
    {"nombre": "Fiberplace: Onboarding Material", "pilar": "Competitiveness", "color": "#f59e0b"},
    {"nombre": "Salesforce: Communication to Customers", "pilar": "Competitiveness", "color": "#d97706"},
    {"nombre": "Salesforce: Customer Profiles", "pilar": "Competitiveness", "color": "#b45309"},
    {"nombre": "Salesforce: Segmentation & Mailings", "pilar": "Competitiveness", "color": "#92400e"},
    {"nombre": "RRSS: LinkedIn & WeChat & Website", "pilar": "Customer", "color": "#059669"},
    {"nombre": "New Catalogue for Meeting and Customers", "pilar": "Customer", "color": "#047857"},
    {"nombre": "Onboarding Kit", "pilar": "Customer", "color": "#065f46"},
    {"nombre": "CXE", "pilar": "Customer", "color": "#064e3b"},
    {"nombre": "Segmentation: Value Proposition", "pilar": "Customer", "color": "#14532d"},
    {"nombre": "Communication Most Sustainable Company in the World", "pilar": "Sustainability", "color": "#7c3aed"},
    {"nombre": "Launch Integrated Report", "pilar": "Sustainability", "color": "#6d28d9"},
    {"nombre": "ESG Event with Customers", "pilar": "Sustainability", "color": "#5b21b6"},
    {"nombre": "EPD's Design", "pilar": "Sustainability", "color": "#4c1d95"},
]

OPCIONES = [p["nombre"] for p in PROYECTOS]
PILARES = {p["nombre"]: p["pilar"] for p in PROYECTOS}
COLORES = {p["nombre"]: p["color"] for p in PROYECTOS}

# Colores por pilar para la leyenda
PILAR_COLORES = {
    "Customer": "#1a5632",
    "Growth & Innovation": "#2563eb",
    "Competitiveness": "#f59e0b",
    "Sustainability": "#7c3aed",
}

# Contraseña para reiniciar la votación
CLAVE_ADMIN = "MatiasL"

DATA_FILE = "votos.csv"
# ============================================================


st.set_page_config(page_title="CMPC - Votación de Ideas", page_icon="🌲", layout="centered")

# CSS corporativo CMPC
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(170deg, #f7f9f7 0%, #eef2ee 50%, #e8efe8 100%);
        font-family: 'Montserrat', sans-serif;
    }
    
    .cmpc-header {
        background: linear-gradient(135deg, #1a5632 0%, #0d3b1f 60%, #0a2e18 100%);
        padding: 36px 30px 30px;
        border-radius: 0 0 24px 24px;
        text-align: center;
        margin: -80px -80px 30px -80px;
        box-shadow: 0 8px 32px rgba(13, 59, 31, 0.25);
        position: relative;
        overflow: hidden;
    }
    .cmpc-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .cmpc-logo-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 4px;
        color: rgba(255,255,255,0.65);
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .cmpc-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .cmpc-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 300;
        color: rgba(255,255,255,0.55);
        margin-top: 6px;
    }
    .cmpc-tree {
        font-size: 32px;
        margin-bottom: 10px;
        display: block;
    }
    
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        color: #1a5632 !important;
    }
    
    .stRadio > label {
        font-family: 'Montserrat', sans-serif !important;
        color: #2d2d2d !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    .stRadio > div {
        background: white;
        border-radius: 16px;
        padding: 12px 20px;
        border: 1px solid rgba(26, 86, 50, 0.12);
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    
    .stButton > button {
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(135deg, #1a5632 0%, #237a45 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 16px rgba(26, 86, 50, 0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #237a45 0%, #2a8f52 100%) !important;
        box-shadow: 0 6px 24px rgba(26, 86, 50, 0.4) !important;
    }
    
    [data-testid="stMetric"] {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid rgba(26, 86, 50, 0.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] {
        color: #1a5632 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }
    
    .streamlit-expanderHeader {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
    }
    
    hr {
        border-color: rgba(26, 86, 50, 0.1) !important;
    }
    
    .cmpc-footer {
        text-align: center;
        color: rgba(26, 86, 50, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        margin-top: 20px;
        padding: 16px 0;
        letter-spacing: 0.5px;
    }
    
    /* Barras personalizadas */
    .bar-container {
        margin-bottom: 12px;
    }
    .bar-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 4px;
    }
    .bar-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        font-weight: 600;
        color: #2d2d2d;
        max-width: 70%;
        line-height: 1.3;
    }
    .bar-stats {
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        color: #888;
        white-space: nowrap;
    }
    .bar-track {
        height: 24px;
        background: #f0f0f0;
        border-radius: 6px;
        overflow: hidden;
        position: relative;
    }
    .bar-fill {
        height: 100%;
        border-radius: 6px;
        display: flex;
        align-items: center;
        padding-left: 8px;
        transition: width 0.5s ease;
        min-width: 0;
    }
    .bar-pillar {
        font-family: 'Montserrat', sans-serif;
        font-size: 9px;
        font-weight: 600;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
    
    /* Leyenda */
    .leyenda {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 16px 0;
        padding: 12px 16px;
        background: white;
        border-radius: 12px;
        border: 1px solid rgba(26, 86, 50, 0.1);
    }
    .leyenda-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .leyenda-dot {
        width: 10px;
        height: 10px;
        border-radius: 3px;
    }
    .leyenda-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        font-weight: 500;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="cmpc-header">
    <span class="cmpc-tree">🌲</span>
    <div class="cmpc-logo-text">CMPC</div>
    <div class="cmpc-title">Votación de Ideas de Proyecto 2026</div>
    <div class="cmpc-subtitle">Selecciona y vota por la iniciativa que consideres más relevante</div>
</div>
""", unsafe_allow_html=True)

# Crear archivo de votos
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Opcion"])
    df.to_csv(DATA_FILE, index=False)

# Votación
st.markdown("")
st.subheader("🗳️ Selecciona tu idea favorita")
voto = st.radio("", OPCIONES, label_visibility="collapsed")

if st.button("✅  Enviar mi voto"):
    nuevo_voto = pd.DataFrame([voto], columns=["Opcion"])
    nuevo_voto.to_csv(DATA_FILE, mode="a", header=False, index=False)
    pilar = PILARES.get(voto, "")
    st.success(f"¡Tu voto por '{voto}' ({pilar}) fue registrado!")
    st.balloons()

st.divider()

# Resultados
st.subheader("📊 Resultados en Vivo")

df_votos = pd.read_csv(DATA_FILE)

if not df_votos.empty and len(df_votos) > 0:
    conteo = df_votos["Opcion"].value_counts()
    total = len(df_votos)

    st.metric("Total de votos recibidos", total)

    # Leyenda de colores por pilar
    leyenda_html = '<div class="leyenda">'
    for pilar, color in PILAR_COLORES.items():
        leyenda_html += f'''
        <div class="leyenda-item">
            <div class="leyenda-dot" style="background:{color}"></div>
            <span class="leyenda-text">{pilar}</span>
        </div>'''
    leyenda_html += '</div>'
    st.markdown(leyenda_html, unsafe_allow_html=True)

    # Barras personalizadas con colores por pilar
    # Ordenar de mayor a menor votos
    sorted_ideas = sorted(OPCIONES, key=lambda x: conteo.get(x, 0), reverse=True)
    max_votos = conteo.max() if len(conteo) > 0 else 1

    bars_html = ""
    for idea in sorted_ideas:
        votos_idea = conteo.get(idea, 0)
        if votos_idea == 0:
            continue
        pct = (votos_idea / total * 100)
        bar_width = max(votos_idea / max_votos * 100, 2)
        color = COLORES.get(idea, "#1a5632")
        pilar = PILARES.get(idea, "")

        bars_html += f'''
        <div class="bar-container">
            <div class="bar-header">
                <span class="bar-name">{idea}</span>
                <span class="bar-stats">{votos_idea} voto{"s" if votos_idea != 1 else ""} · {pct:.1f}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{bar_width}%; background:{color};">
                    <span class="bar-pillar">{pilar}</span>
                </div>
            </div>
        </div>'''

    st.markdown(bars_html, unsafe_allow_html=True)

    # Tabla copiable para PPT
    with st.expander("📋 Tabla de resultados (para copiar a PPT)"):
        detalle = pd.DataFrame({
            "Proyecto": [i for i in sorted_ideas if conteo.get(i, 0) > 0],
            "Pilar": [PILARES.get(i, "") for i in sorted_ideas if conteo.get(i, 0) > 0],
            "Votos": [conteo.get(i, 0) for i in sorted_ideas if conteo.get(i, 0) > 0],
            "Porcentaje": [f"{(conteo.get(i, 0)/total*100):.1f}%" for i in sorted_ideas if conteo.get(i, 0) > 0]
        })
        st.dataframe(detalle, use_container_width=True, hide_index=True)
        st.caption("💡 Tip: Selecciona toda la tabla (Ctrl+A dentro de la tabla) y pégala en PowerPoint o Excel")

    st.markdown("")
    if st.button("🔄 Refrescar Resultados"):
        st.rerun()
else:
    st.info("Aún no hay votos registrados. ¡Sé el primero en votar!")

# Zona Admin
st.divider()

with st.expander("⚙️ Zona de Administrador"):
    st.warning("Esto borra TODOS los votos de forma permanente.")
    clave = st.text_input("Contraseña de admin:", type="password")
    if st.button("🗑️ Reiniciar Votación"):
        if clave == CLAVE_ADMIN:
            df = pd.DataFrame(columns=["Opcion"])
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Votación reiniciada.")
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta.")

# Footer
st.markdown('<div class="cmpc-footer">CMPC · Votación de Ideas de Proyecto 2026 · Escanea el QR para participar</div>', unsafe_allow_html=True)
