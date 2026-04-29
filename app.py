import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuración básica
st.set_page_config(page_title="Invenzor Pro", layout="wide")

# Título principal
st.title("🏛️ Invenzor")
st.markdown("### *Consultor Estratégico de Inversión*")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración")
    perfil = st.selectbox("Tu Perfil de Riesgo", ["Conservador", "Moderado", "Arriesgado"], index=1)
    capital = st.number_input("Capital total (€)", value=10000, step=1000)

# --- LÓGICA DE DATOS ---
@st.cache_data(ttl=3600)
def obtener_datos():
    # Bajamos datos de los activos principales
    tickers = {"Acciones": "SPY", "Bonos": "AGG", "Oro": "GLD", "Bitcoin": "BTC-USD", "Efectivo": "BIL"}
    data = yf.download(list(tickers.values()), period="1y")['Close']
    
    # Calculamos tendencia
    tendencias = {}
    for nombre, ticker in tickers.items():
        actual = data[ticker].iloc[-1]
        media_200 = data[ticker].rolling(200).mean().iloc[-1]
        tendencias[nombre] = "Alcista" if actual > media_200 else "Bajista"
    return tendencias

try:
    status = obtener_datos()

    # --- LÓGICA DE PESOS ---
    pesos = {"Acciones": 0.25, "Bonos": 0.25, "Oro": 0.20, "Bitcoin": 0.15, "Efectivo": 0.15}
    
    if status["Acciones"] == "Bajista":
        pesos["Acciones"] -= 0.10
        pesos["Efectivo"] += 0.10
    
    if perfil == "Arriesgado":
        pesos["Acciones"] += 0.15
        pesos["Bonos"] -= 0.15
    elif perfil == "Conservador":
        pesos["Acciones"] -= 0.15
        pesos["Bonos"] += 0.15

    # --- DISEÑO DE LA WEB ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Distribución Sugerida")
        fig = go.Figure(data=[go.Pie(labels=list(pesos.keys()), values=list(pesos.values()), hole=.3)])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💡 Resumen Táctico")
        st.info(f"Para un perfil **{perfil}**, el sistema recomienda priorizar la seguridad.")
        for activo, tendencia in status.items():
            st.write(f"**{activo}:** {'✅' if tendencia == 'Alcista' else '⚠️'} {tendencia}")

    st.divider()
    st.subheader("📋 Tu Plan de Inversión")
    df = pd.DataFrame({
        "Activo": pesos.keys(),
        "Porcentaje": [f"{v*100:.1f}%" for v in pesos.values()],
        "Inversión (€)": [f"{v*capital:,.2f} €" for v in pesos.values()]
    })
    st.table(df)

except Exception as e:
    st.warning("Conectando con los mercados financieros... por favor, actualiza la página en unos segundos.")
    
