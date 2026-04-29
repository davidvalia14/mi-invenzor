import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Invenzor | Smart Wealth", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    </style>
    """, unsafe_content_html=True)

# --- CABECERA ---
st.title("🏛️ INVENZOR")
st.markdown("<p style='color: #8892b0; font-size: 20px;'>Inteligencia Macro y Gestión Táctica</p>", unsafe_content_html=True)
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Centro de Control")
    perfil = st.select_slider("Perfil de Riesgo", options=["Conservador", "Moderado", "Arriesgado"], value="Moderado")
    capital = st.number_input("Capital total (€)", value=10000, step=1000)
    st.info("Datos en tiempo real via Yahoo Finance")

# --- LÓGICA DE DATOS ---
@st.cache_data(ttl=3600)
def fetch_market_data():
    assets = {"RV": "URTH", "RF": "AGG", "ORO": "GLD", "BTC": "BTC-USD"}
    data = yf.download(list(assets.values()), period="1y")['Close']
    intel = {}
    for name, ticker in assets.items():
        price = data[ticker].iloc[-1]
        sma_200 = data[ticker].rolling(200).mean().iloc[-1]
        intel[name] = {"trend": "ALCISTA" if price > sma_200 else "BAJISTA", "price": price}
    return intel

try:
    intel = fetch_market_data()
    
    # Motor de pesos
    pesos = {"Acciones": 0.25, "Bonos": 0.25, "Oro": 0.20, "Bitcoin": 0.15, "Efectivo": 0.15}
    if intel["RV"]["trend"] == "BAJISTA":
        pesos["Acciones"] -= 0.10
        pesos["Efectivo"] += 0.10
    
    if perfil == "Arriesgado":
        pesos["Acciones"] += 0.15; pesos["Bonos"] -= 0.15
    elif perfil == "Conservador":
        pesos["Acciones"] -= 0.15; pesos["Bonos"] += 0.15

    # --- DASHBOARD ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><h4>Tendencia Acciones</h4><h2>{intel['RV']['trend']}</h2></div>", unsafe_content_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><h4>Tendencia Crypto</h4><h2>{intel['BTC']['trend']}</h2></div>", unsafe_content_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><h4>Estado</h4><h2>ESTABLE</h2></div>", unsafe_content_html=True)

    st.write("##")
    c1, c2 = st.columns([1.2, 1])

    with c1:
        fig = go.Figure(data=[go.Pie(labels=list(pesos.keys()), values=list(pesos.values()), hole=.5)])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("💡 Resumen de Estrategia")
        st.write(f"Para tu perfil **{perfil}**, el sistema recomienda una exposición del {pesos['Acciones']*100:.1f}% en renta variable.")
        st.write(f"El mercado de Bitcoin se encuentra en fase **{intel['BTC']['trend']}**.")

    st.write("---")
    st.subheader("💰 Desglose de Inversión")
    df_final = pd.DataFrame({
        "Activo": pesos.keys(),
        "Peso": [f"{v*100:.1f}%" for v in pesos.values()],
        "Importe (€)": [f"{v*capital:,.2f} €" for v in pesos.values()]
    })
    st.table(df_final)

except Exception as e:
    st.error("Error al cargar datos. Refresca la página.")
