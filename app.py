import streamlit as st
import pandas as pd
import datetime
from modulos.utils import obtener_datos
import modulos.filtros as flt
import modulos.metricas as mtr
import modulos.graficos as grf


def main() -> None:
    st.set_page_config(page_title='Dashboard Pro',
                    page_icon='📊',
                    layout= 'wide')
    fecha_actual = datetime.datetime.now().strftime('%d %B %Y')
    st.write(f'Fecha: \n {fecha_actual}')
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
    rango_fechas = st.date_input('Seleccionar periodo', min_value=fecha_min, max_value=fecha_max, key='filtro_fechas', label_visibility="collapsed", width=235)
    if len(rango_fechas) != 2:
        st.info("👆 Por favor selecciona una fecha de inicio y fin para ver los datos.")
        st.stop() # Detiene la ejecución del resto del script hasta que se arregle
        
    inicio, fin = rango_fechas

    seleccionar_todos = st.checkbox('Seleccionar todos los productos ', value=False, key='seleccionar_todos_productos')
    if seleccionar_todos:
        productos_seleccionados = df['producto'].unique().tolist()
    else: 
        productos_seleccionados = productos_elegir

    st.divider()    
    df_filtrado = flt.aplicar_filtros(df, productos_seleccionados, categorias_seleccionadas, regiones_seleccionadas)    
    df_filtrado_completo = flt.aplicar_filtro_completo(df_filtrado, rango_fechas) 
        
    if df_filtrado_completo.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
    else:
        delta = mtr.Delta(df_filtrado, inicio, fin)
        col1,col2,col3 = st.columns(3)
        with col1: mtr.metrica_total_ventas(delta)   
        with col2: mtr.metrica_cant_productos(delta)
        with col3: mtr.metrica_prom_ventas(delta)
            
        tab_graficos, tab_equipo, tab_datos = st.tabs(["📈 Análisis de Ventas", "👥 Vendedores y Regiones", "📄 Registro Completo"])   
        
        with tab_graficos:
            col1, col_divider, col2 = st.columns([10,0.5,10])
            with col1: grf.grafico_linea(df_filtrado_completo)
            with col_divider:
                st.markdown("""
                    <div style="
                        border-left: 1.5px solid #444444; 
                        height: 400px; 
                        margin: 0 auto;
                        opacity: 0.6;
                    "></div>""", 
                    unsafe_allow_html=True)
            with col2: grf.grafico_barra_producto(df_filtrado_completo)
                
        with tab_equipo:
            col1, col_divider, col2 = st.columns([10, 0.5, 10])
            with col1: grf.grafico_torta(df_filtrado_completo)   
            with col_divider:
                st.markdown("""
                    <div style="
                        border-left: 1.5px solid #444444; 
                        height: 400px; 
                        margin: 0 auto;
                        opacity: 0.6;
                    "></div>""", 
                    unsafe_allow_html=True)
            with col2: grf.grafico_barra_region(df_filtrado_completo)
                
        with tab_datos:    
            st.markdown("#### Datos completos")
            st.dataframe(df_filtrado_completo, hide_index=True, width='stretch', column_config={
                'fecha': st.column_config.DateColumn('Fecha de Venta', format='DD-MM-YYYY')})
    # st.markdown("---")
    # st.markdown("Fuente de datos: [API Pública de Datos Económicos](URL_DE_LA_FUENTE)")

    st.markdown("---")
    with st.expander("ℹ️ Detalles de la Fuente de Datos"):
        st.markdown("""
        *   **Fuente:** Base de Datos MySQL Interna (Esquema: `ventas_db`)
        *   **Sistema:** CRM de Gestión de Clientes v3.1
        *   **Propietario:** Departamento de TI / Equipo de Ventas
        *   **Última Actualización:** 15 de Noviembre de 2024
        """)

if __name__ == '__main__':
    main()