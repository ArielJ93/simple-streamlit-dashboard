import streamlit as st

@st.cache_data
def obtener_datos(_conn):
    query = 'SELECT fecha, producto, ventas, region, vendedor, categoria FROM ventas_electronica'
    return _conn.query(query)
