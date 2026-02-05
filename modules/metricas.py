import streamlit as st

def metrica_total_ventas(df_filtrado):
    total_ventas = df_filtrado['ventas'].sum()
    st.metric('Ventas Totales',
            f'${total_ventas:,.0f}',
            delta='12,5%')

def metrica_cant_productos(df_filtrado):
    productos_unicos = df_filtrado['producto'].nunique()
    st.metric('Productos Activos',
            productos_unicos,
            delta='+3')

def metrica_prom_ventas(df_filtrado):
    promedio_ventas = df_filtrado['ventas'].mean() if not df_filtrado.empty else 0
    st.metric('Promedio diario',
            f'{promedio_ventas:,.0f}',
            delta='8,2%')