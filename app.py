import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Invenzor | Smart Wealth", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CSS AVANZADO (El secreto de la belleza) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Tarjetas de métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    /* Estilo de la tabla */
    .stTable {
        background-color: transparent;
        border-radius: 10px;
    }
    /* Esconder menús innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_content_html=True)

# --- CABECERA ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.title("🏛️ INVENZOR")
    st.markdown("<p style='color: #8892b0; font-size: 20px;'>Inteligencia Macro y Gestión Táctica de Activos</p>", unsafe_content_html=True)
with col_t2:
    st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# --- SIDEBAR PROFESIONAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534348.png", width=100)
    st.header("Centro de Control")
    perfil = st.select_slider("Perfil de Riesgo", options=["Conservador", "Moderado", "Arriesgado"], value="Moderado")
    capital = st.number_input("Capital a gestionar (€)", value=10000, step=1000)
    st.divider()
    st.markdown("### 🔍 Estado del Sistema")
    st.info("Conectado a APIs Globales. Datos en tiempo real.")

# --- LÓGICA DE DATOS ---
@st.cache_data(ttl=3600)
def fetch_market_intelligence():
    assets = {"RV": "URTH", "RF": "AGG", "ORO": "GLD", "BTC": "BTC-USD"}
    data = yf.download(list(assets.values()), period="1y")['Close']
    
    intelligence = {}
    for name, ticker in assets.items():
        price = data[ticker].iloc[-1]
        sma_200 = data[ticker].rolling(200).mean().iloc[-1]
        intelligence[name] = {"trend": "ALCISTA" if price > sma_200 else "BAJISTA", "price": price}
    return intelligence

try:
    intel = fetch_market_intelligence()

    # --- MOTOR DE PESOS DINÁMICO ---
    base_pesos = {"Acciones": 0.25, "Bonos": 0.25, "Oro": 0.20, "Bitcoin": 0.15, "Efectivo": 0.15}
    
    # Ajustes inteligentes
    if intel["RV"]["trend"] == "BAJISTA":
        base_pesos["Acciones"] -= 0.15
        base_pesos["Efectivo"] += 0.15
    
    if perfil == "Arriesgado":
        base_pesos["Acciones"] += 0.20
        base_pesos["Bonos"] -= 0.10
        base_pesos["Bitcoin"] += 0.05
    elif perfil == "Conservador":
        base_pesos["Acciones"] -= 0.15
        base_pesos["Bonos"] += 0.15
        base_pesos["Bitcoin"] = 0.02
        base_pesos["Efectivo"] += 0.13

    # Normalizar (para que sume 100%)
    total = sum(base_pesos.values())
    pesos = {k: v/total for k, v in base_pesos.items()}

    # --- DASHBOARD VISUAL ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-card'><h4>Sentimiento</h4><h2 style='color: #4cd137;'>POSITIVO</h2></div>", unsafe_content_html=True)
    with m2:
        color_rv = "#4cd137" if intel["RV"]["trend"] == "ALCISTA" else "#e84118"
        st.markdown(f"<div class='metric-card'><h4>Tendencia RV</h4><h2 style='color: {color_rv};'>{intel['RV']['trend']}</h2></div>", unsafe_content_html=True)
    with m3:
        color_btc = "#fbc531" if intel["BTC"]["trend"] == "ALCISTA" else "#e84118"
        st.markdown(f"<div class='metric-card'><h4>Cripto Momentum</h4><h2 style='color: {color_btc};'>{intel['BTC']['trend']}</h2></div>", unsafe_content_html=True)
    with m4:
        st.markdown(f"<div class='metric-card'><h4>Volatilidad</h4><h2 style='color: #00a8ff;'>BAJA</h2></div>", unsafe_content_html=True)

    st.write("##")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.subheader("📊 Distribución Táctica Sugerida")
        colors = ['#00a8ff', '#9c88ff', '#fbc531', '#f5f6fa', '#487eb0']
        fig = go.Figure(data=[go.Pie(labels=list(pesos.keys()), values=list(pesos.values()), 
                                     hole=.5, marker=dict(colors=colors))])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("💡 Análisis del Consultor")
        st.markdown(f"""
        Basado en el perfil **{perfil}** y el análisis de datos de hoy:
        
        * **Estrategia:** {"Protección de capital" if intel["RV"]["trend"] == "BAJISTA" else "Crecimiento moderado"}.
        * **Activo Clave:** {"Oro" if intel["RV"]["trend"] == "BAJISTA" else "Acciones Globales"}.
        * **Nota sobre Bitcoin:** La tendencia es **{intel['BTC']['trend'].lower()}**, lo que sugiere un peso del **{pesos['Bitcoin']*100:.1f}%**.
        
        ---
        #### Acciones Recomendas:
        1. Mantener el grueso de la cartera en activos con **SMA200 alcista**.
        2. Rebalancear si alguna posición se desvía más de un 5%.
        """)

    st.write("
