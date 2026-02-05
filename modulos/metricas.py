import streamlit as st

def deltas(df_filtrado):
    
    periodo_actual = df_filtrado[(df_filtrado['fecha'].dt.date >= inicio) & 
            (df_filtrado['fecha'].dt.date <= fin)]
    cantidad_dias = len(periodo_actual)
    periodo_previo = df_filtrado[(df_filtrado['fecha'].dt.date >= inicio -cantidad_dias) & 
            (df_filtrado['fecha'].dt.date <= fin - cantidad_dias)]
    
    delta_porcentaje = (periodo_actual.sum() - periodo_previo.sum()) / periodo_previo.sum()
    return delta_porcentaje


def metrica_total_ventas(df_filtrado):
    total_ventas = df_filtrado['ventas'].sum()
    st.metric('Ventas Totales',
            f'${total_ventas:,.0f}',
            delta= deltas(df_filtrado))

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