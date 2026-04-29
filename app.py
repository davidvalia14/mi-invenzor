import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuración para que se vea bien en móviles y PCs
st.set_page_config(page_title="Invenzor - Consultor de Inversión", layout="wide")

# Estilo visual elegante
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border: 1px solid #e2e8f0; }
    h1 { color: #1e293b; font-weight: 800; }
    </style>
    """, unsafe_content_html=True)

st.title("🏛️ Invenzor")
st.write("Análisis macroeconómico y sugerencia táctica de cartera en tiempo real.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configura tu Perfil")
    perfil = st.selectbox("¿Cómo es tu perfil?", ["Conservador", "Moderado", "Arriesgado"], index=1)
    capital = st.number_input("Capital de referencia (€)", value=10000, step=500)
    st.divider()
    st.write("Esta herramienta analiza tendencias de mercado y sugiere pesos ideales para 5 activos clave.")

# --- LÓGICA DE DATOS ---
@st.cache_data(ttl=3600) # Esto hace que la web sea rápida y no colapse
def analizar_mercado():
    # Activos: SPY (Acciones), AGG (Bonos), GLD (Oro), BTC (Bitcoin), BIL (Efectivo)
    tickers = {"Acciones": "SPY", "Bonos": "AGG", "Oro": "GLD", "Bitcoin": "BTC-USD", "Efectivo": "BIL"}
    data = yf.download(list(tickers.values()), period="1y")['Close']
    
    # Análisis de tendencia (Precio vs Media 200 días)
    resultados = {}
    for nombre, ticker in tickers.items():
        actual = data[ticker].iloc[-1]
        media = data[ticker].rolling(200).mean().iloc[-1]
        resultados[nombre] = "Alcista" if actual > media else "Bajista"
    
    return resultados, tickers

# --- MOSTRAR RESULTADOS ---
try:
    tendencias, tickers = analizar_mercado()
    
    # Distribución lógica basada en perfil y mercado
    pesos = {"Acciones": 0.2, "Bonos": 0.2, "Oro": 0.2, "Bitcoin": 0.2, "Efectivo": 0.2}
    
    # Lógica inteligente simple
    if tendencias["Acciones"] == "Bajista":
        pesos["Acciones"] -= 0.1; pesos["Efectivo"] += 0.1
    if perfil == "Arriesgado":
        pesos["Acciones"] += 0.15; pesos["Bonos"] -= 0.15
    elif perfil == "Conservador":
        pesos["Acciones"] -= 0.1; pesos["Bonos"] += 0.1

    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("📊 Distribución Recomendada")
        fig = go.Figure(data=[go.Pie(labels=list(pesos.keys()), values=list(pesos.values()), hole=.4)])
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_der:
        st.subheader("📝 Hoja de Ruta")
        st.markdown(f"""
        <div class="card">
            <h4>Análisis para perfil {perfil}</h4>
            <p>Estado del mercado: <b>{"Inestable" if tendencias["Acciones"] == "Bajista" else "Saludable"}</b></p>
            <ul>
                <li><b>Acciones:</b> {tendencias["Acciones"]}</li>
                <li><b>Bitcoin:</b> {tendencias["Bitcoin"]}</li>
            </ul>
            <strong>Sugerencia:</strong> Invierte <b>{(pesos['Acciones']*capital):,.0f}€</b> en Renta Variable diversificada.
        </div>
        """, unsafe_content_html=True)

    st.write("### 📋 Desglose de Operaciones")
    tabla = pd.DataFrame({
        "Activo": pesos.keys(),
        "Porcentaje": [f"{v*100:.1f}%" for v in pesos.values()],
        "Cantidad a Invertir": [f"{v*capital:,.2f} €" for v in pesos.values()]
    })
    st.table(tabla)

except Exception as e:
    st.error("Estamos actualizando los datos del mercado. Por favor, recarga en unos segundos.")