import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN - Edita aquí tus opciones
# ============================================================
OPCIONES = [
    "Idea 1",
    "Idea 2",
    "Idea 3",
    "Idea 4",
    "Idea 5",
    "Idea 6",
    "Idea 7",
    "Idea 8",
    "Idea 9",
    "Idea 10",
]

# Contraseña para reiniciar la votación (cámbiala por la que tú quieras)
CLAVE_ADMIN = "admin123"

TITULO = "Votación de Ideas de Proyecto"
DATA_FILE = "votos.csv"
# ============================================================


st.set_page_config(page_title="CMPC - Votación de Ideas", page_icon="🌲", layout="centered")

# CSS corporativo CMPC - Verde oscuro, blanco, elegante
st.markdown("""
<style>
    /* Fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    /* Fondo principal */
    .stApp {
        background: linear-gradient(170deg, #f7f9f7 0%, #eef2ee 50%, #e8efe8 100%);
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Header personalizado */
    .cmpc-header {
        background: linear-gradient(135deg, #1a5632 0%, #0d3b1f 60%, #0a2e18 100%);
        padding: 40px 30px 35px;
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
    .cmpc-header::after {
        content: "";
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 70%);
        border-radius: 50%;
    }
    .cmpc-logo-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 4px;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .cmpc-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .cmpc-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        font-weight: 300;
        color: rgba(255,255,255,0.6);
        margin-top: 8px;
    }
    .cmpc-tree {
        font-size: 36px;
        margin-bottom: 12px;
        display: block;
    }
    
    /* Títulos */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        color: #1a5632 !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-family: 'Montserrat', sans-serif !important;
        color: #2d2d2d !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    .stRadio > div {
        background: white;
        border-radius: 16px;
        padding: 12px 20px;
        border: 1px solid rgba(26, 86, 50, 0.12);
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    
    /* Botones */
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
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #237a45 0%, #2a8f52 100%) !important;
        box-shadow: 0 6px 24px rgba(26, 86, 50, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Métricas */
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
    [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        color: #1a5632 !important;
        background: white !important;
        border-radius: 12px !important;
    }
    
    /* Info y Success */
    .stAlert {
        border-radius: 12px !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(26, 86, 50, 0.1) !important;
    }
    
    /* Caption footer */
    .cmpc-footer {
        text-align: center;
        color: rgba(26, 86, 50, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        font-weight: 400;
        margin-top: 20px;
        padding: 16px 0;
        letter-spacing: 0.5px;
    }
    
    /* Chart colors */
    .stBarChart {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Header corporativo CMPC
st.markdown("""
<div class="cmpc-header">
    <span class="cmpc-tree">🌲</span>
    <div class="cmpc-logo-text">CMPC</div>
    <div class="cmpc-title">Votación de Ideas de Proyecto</div>
    <div class="cmpc-subtitle">Selecciona y vota por la idea que más te guste</div>
</div>
""", unsafe_allow_html=True)

# Crear archivo de votos si no existe
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Opcion"])
    df.to_csv(DATA_FILE, index=False)

# Interfaz de votación
st.markdown("")
st.subheader("🗳️ Selecciona tu idea favorita")
voto = st.radio("", OPCIONES, label_visibility="collapsed")

if st.button("✅  Enviar mi voto"):
    nuevo_voto = pd.DataFrame([voto], columns=["Opcion"])
    nuevo_voto.to_csv(DATA_FILE, mode="a", header=False, index=False)
    st.success(f"¡Tu voto por '{voto}' fue registrado exitosamente!")
    st.balloons()

st.divider()

# Resultados
st.subheader("📊 Resultados en Vivo")

df_votos = pd.read_csv(DATA_FILE)

if not df_votos.empty and len(df_votos) > 0:
    conteo = df_votos["Opcion"].value_counts()
    total = len(df_votos)

    st.metric("Total de votos recibidos", total)
    
    st.markdown("")
    st.bar_chart(conteo, color="#1a5632")

    with st.expander("📋 Ver detalle numérico"):
        detalle = pd.DataFrame({
            "Idea": conteo.index,
            "Votos": conteo.values,
            "Porcentaje": [f"{(v/total*100):.1f}%" for v in conteo.values]
        })
        st.table(detalle)

    if st.button("🔄 Refrescar Resultados"):
        st.rerun()
else:
    st.info("Aún no hay votos registrados. ¡Sé el primero en votar!")

# Zona Admin
st.divider()

with st.expander("⚙️ Zona de Administrador"):
    st.warning("Esto borra TODOS los votos de forma permanente. No se puede deshacer.")
    clave = st.text_input("Escribe la contraseña de admin:", type="password")
    if st.button("🗑️ Reiniciar Votación"):
        if clave == CLAVE_ADMIN:
            df = pd.DataFrame(columns=["Opcion"])
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Votación reiniciada. Todos los votos fueron borrados.")
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta.")

# Footer
st.markdown('<div class="cmpc-footer">CMPC · Sistema de Votación de Ideas · Escanea el QR para participar</div>', unsafe_allow_html=True)
