import streamlit as st
import pandas as pd
import plotly.express as px
from modulos.conexion_sql import obtener_datos
import modulos.filtros as flt
import modulos.metricas as mtr
import modulos.graficos as grf


def main():
    st.set_page_config(page_title='Dashboard Pro',
                    page_icon='📊',
                    layout= 'wide')
    st.title('🚀 Dashboard de Ventas')
    st.write('Bienvenido a tu dashboard profesional')

    conn = st.connection('mysql', type='sql')
    df = obtener_datos(conn)
    df['fecha'] = pd.to_datetime(df['fecha'])

    flt.inicio_filtros(df)

    productos_elegir, categorias_seleccionadas, regiones_seleccionadas = flt.generar_sidebar(df)

    st.markdown("#### 📅 Periodo de Análisis")
    fecha_min = df['fecha'].min()
    fecha_max = df['fecha'].max()
    rango_fechas = st.date_input('Seleccionar periodo', min_value=fecha_min, max_value=fecha_max, key='filtro_fechas', label_visibility="collapsed")

    col1, col2 = st.columns([1,2.6], vertical_alignment='center')
    with col1:
        seleccionar_todos = st.checkbox('Seleccionar todos los productos', value=False, key='seleccionar_todos_productos')
        if seleccionar_todos:
            productos_seleccionados = df['producto'].unique().tolist()
        else: 
            productos_seleccionados = productos_elegir
    with col2:
        st.markdown('**(para que se aplique el filtro de producto asegúrate de desmarcar esta casilla)**')
        
    st.divider()    
        
    df_filtrado = flt.aplicar_filtros(df, productos_seleccionados, categorias_seleccionadas, rango_fechas, regiones_seleccionadas) 
        
    if df_filtrado.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
    else:
        col1,col2,col3 = st.columns(3)
        with col1: mtr.metrica_total_ventas(df_filtrado)   
        with col2: mtr.metrica_cant_productos(df_filtrado)
        with col3: mtr.metrica_prom_ventas(df_filtrado)
            
        tab_graficos, tab_equipo, tab_datos = st.tabs(["📈 Análisis de Ventas", "👥 Vendedores y Regiones", "📄 Registro Completo"])   
        
        with tab_graficos:
            col1, col_divider, col2 = st.columns([10,0.5,10])
            with col1: grf.grafico_linea(df_filtrado)
            with col_divider:
                st.markdown("""
                    <div style="
                        border-left: 1.5px solid #444444; 
                        height: 400px; 
                        margin: 0 auto;
                        opacity: 0.6;
                    "></div>""", 
                    unsafe_allow_html=True)
            with col2: grf.grafico_barra_producto(df_filtrado)
                
        with tab_equipo:
            col1, col_divider, col2 = st.columns([10, 0.5, 10])
            with col1: grf.grafico_torta(df_filtrado)   
            with col_divider:
                st.markdown("""
                    <div style="
                        border-left: 1.5px solid #444444; 
                        height: 400px; 
                        margin: 0 auto;
                        opacity: 0.6;
                    "></div>""", 
                    unsafe_allow_html=True)
            with col2: grf.grafico_barra_region(df_filtrado)
                
        with tab_datos:    
            st.markdown("#### Datos completos")
            st.dataframe(df_filtrado, hide_index=True, width='stretch', column_config={
                'fecha': st.column_config.DateColumn('Fecha de Venta', format='DD-MM-YYYY')})

if __name__ == '__main__':
    main()