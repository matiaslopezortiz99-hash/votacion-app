import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN - Edita aquí tus opciones
# ============================================================
# Para agregar o quitar ideas, simplemente agrega o borra líneas.
# Ejemplo: si solo quieres 5 opciones, borra las que sobran.
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

# Título que aparece arriba de la página
TITULO = "💡 Votación en Tiempo Real"

# Archivo donde se guardan los votos (no cambiar a menos que sepas lo que haces)
DATA_FILE = "votos.csv"
# ============================================================


# Configuración de la página
st.set_page_config(page_title="Votación de Ideas", page_icon="💡", layout="centered")

# CSS personalizado para que se vea bonito
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #0a0a0f 0%, #111128 40%, #0d1117 100%);
    }
    .stRadio > label {
        color: rgba(255,255,255,0.8) !important;
        font-size: 16px !important;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title(TITULO)

# Crear archivo de votos si no existe
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Opcion"])
    df.to_csv(DATA_FILE, index=False)

# Interfaz de votación
st.subheader("Selecciona la idea que más te guste:")
voto = st.radio("", OPCIONES, label_visibility="collapsed")

# Botón de votar
if st.button("✅ Enviar Voto"):
    nuevo_voto = pd.DataFrame([voto], columns=["Opcion"])
    nuevo_voto.to_csv(DATA_FILE, mode="a", header=False, index=False)
    st.success(f"¡Tu voto por '{voto}' fue registrado! 🎉")
    st.balloons()

# Separador
st.divider()

# Resultados
st.subheader("📊 Resultados en Vivo")

df_votos = pd.read_csv(DATA_FILE)

if not df_votos.empty and len(df_votos) > 0:
    conteo = df_votos["Opcion"].value_counts()
    total = len(df_votos)

    # Mostrar total de votos
    st.metric("Total de votos", total)

    # Gráfico de barras
    st.bar_chart(conteo)

    # También mostrar como tabla
    with st.expander("Ver detalle numérico"):
        detalle = pd.DataFrame({
            "Idea": conteo.index,
            "Votos": conteo.values,
            "Porcentaje": [f"{(v/total*100):.1f}%" for v in conteo.values]
        })
        st.table(detalle)

    # Botón refrescar
    if st.button("🔄 Refrescar Resultados"):
        st.rerun()
else:
    st.info("Aún no hay votos. ¡Sé el primero! 🚀")

# Footer
st.divider()
st.caption("Sistema de votación en tiempo real • Escanea el QR para votar")
