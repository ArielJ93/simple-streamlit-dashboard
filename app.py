import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Pro',
                page_icon='📊',
                layout= 'wide')
st.title('🚀 Dashboard de Ventas')
st.write('Bienvenido a tu dashboard profesional')

conn = st.connection('mysql', type='sql')

@st.cache_data
def obtener_datos(_conn):
    query = 'SELECT fecha, producto, ventas, region, vendedor, categoria FROM ventas_electronica'
    return _conn.query(query)

df = obtener_datos(conn)
df['fecha'] = pd.to_datetime(df['fecha'])


if 'filtro_productos' not in st.session_state:
    st.session_state.filtro_productos = df['producto'].unique().tolist()[:10]

if 'filtro_fechas' not in st.session_state:
    st.session_state.filtro_fechas = [df['fecha'].min().date(), df['fecha'].max().date()]

if 'filtro_categoria' not in st.session_state:
    st.session_state.filtro_categoria = df['categoria'].unique().tolist()

if 'seleccionar_todos_productos' not in st.session_state:
    st.session_state.seleccionar_todos_productos = False

def reiniciar_filtros():
    st.session_state.filtro_productos = []
    st.session_state.filtro_fechas = []
    st.session_state.filtro_categoria = []
    st.session_state.seleccionar_todos_productos = False

with st.sidebar:
    st.title('Controles')
    
    col_button1, col_button2 = st.columns(2)
    with col_button1:
        if st.button('🔄 Datos', width='stretch', help='Sincronizar con MySQL'):
            st.cache_data.clear()
            st.rerun()
    with col_button2:
        st.button('Limpiar filtros', on_click=reiniciar_filtros, width='stretch')
        
    st.divider()

    lista_productos = df['producto'].unique().tolist()
    productos_elegir = st.multiselect('Filtrar productos', lista_productos, key='filtro_productos')

    st.divider()
    
    lista_categorias = df['categoria'].unique().tolist()
    categorias_seleccionadas = st.multiselect('Filtrar por categoría', lista_categorias, key='filtro_categoria')
    

st.markdown("#### 📅 Periodo de Análisis")
fecha_min = df['fecha'].min()
fecha_max = df['fecha'].max()
rango_fechas = st.date_input('Seleccionar periodo', min_value=fecha_min, max_value=fecha_max, key='filtro_fechas', label_visibility="collapsed")

col1, col2 = st.columns([1,2.6], vertical_alignment='center')
with col1:
    seleccionar_todos = st.checkbox('Seleccionar todos los productos', value=False, key='seleccionar_todos_productos')
    if seleccionar_todos:
        productos_seleccionados = lista_productos
    else: 
        productos_seleccionados = productos_elegir
with col2:
    st.markdown('**(para que se aplique el filtro de producto asegúrate de desmarcar esta casilla)**')
st.divider()    
    
df_filtrado = df[df['producto'].isin(productos_seleccionados)]

if len(rango_fechas) == 2:
    inicio, fin = rango_fechas
    df_filtrado = df_filtrado[(df_filtrado['fecha'].dt.date >= inicio) & 
        (df_filtrado['fecha'].dt.date <= fin)]

df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_seleccionadas)]    
    
if df_filtrado.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
else:
    col1,col2,col3 = st.columns(3)
    with col1:
        total_ventas = df_filtrado['ventas'].sum()
        st.metric('Ventas Totales',
                f'${total_ventas:,.0f}',
                delta='12,5%')
    with col2:
        productos_unicos = df_filtrado['producto'].nunique()
        st.metric('Productos Activos',
                productos_unicos,
                delta='+3')
    with col3:
        promedio_ventas = df_filtrado['ventas'].mean() if not df_filtrado.empty else 0
        st.metric('Promedio diario',
                f'{promedio_ventas:,.0f}',
                delta='8,2%')
        
    tab_graficos, tab_equipo, tab_datos = st.tabs(["📈 Análisis de Ventas", "👥 Vendedores y Regiones", "📄 Registro Completo"])   
    
    with tab_graficos:
        col1, col_divider, col2 = st.columns([10,0.5,10])
        with col1:
            ventas_categoria = df_filtrado.groupby(['fecha','categoria'])['ventas'].sum().reset_index()
            fig_lineas = px.line(ventas_categoria, x='fecha', y='ventas',
                                title='Tendencia de Ventas',
                                template='plotly_dark',
                                color='categoria',
                                markers=True)
            fig_lineas.update_layout(title_x=0.5, title_xanchor='center')
            st.plotly_chart(fig_lineas, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_lineas'}})
        with col_divider:
            st.markdown("""
                <div style="
                    border-left: 1.5px solid #444444; 
                    height: 400px; 
                    margin: 0 auto;
                    opacity: 0.6;
                "></div>""", 
                unsafe_allow_html=True)
        
        with col2:
            ventas_topproductos = df_filtrado.nlargest(10, 'ventas').reset_index()
            fig_barras = px.bar(ventas_topproductos, y='producto', x='ventas',
                                title='Ventas por producto <br>(solo puedes seleccionar hasta 10 productos)',
                                template='plotly_dark',
                                orientation='h',
                                )
            fig_barras.update_traces(textposition='outside', cliponaxis=False)
            fig_barras.update_layout(title_x=0.5, title_xanchor='center', yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_barras, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_barras_productos'}})
    with tab_equipo:
        col1, col_divider, col2 = st.columns([10, 0.5, 10])
        with col1:
            ventas_vendedor = df_filtrado.groupby('vendedor')['ventas'].sum().reset_index()
            fig_pie =px.pie(ventas_vendedor, names='vendedor', values='ventas', 
                            color='vendedor', 
                            title='Ventas($) por vendedor', 
                            template= 'plotly_dark', 
                            hole=0.3)
            fig_pie.update_traces(textfont_size=14, textfont_color='black')
            fig_pie.update_layout(title_x=0.5, title_xanchor='center')
            st.plotly_chart(fig_pie, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_tortas_vendedores'}})
            
        with col_divider:
            st.markdown("""
                <div style="
                    border-left: 1.5px solid #444444; 
                    height: 400px; 
                    margin: 0 auto;
                    opacity: 0.6;
                "></div>""", 
                unsafe_allow_html=True)

        with col2:
            ventas_region = df_filtrado.groupby('region')['ventas'].sum().reset_index()
            fig_barras_region = px.bar(ventas_region, x='region', y='ventas',
                                    title='Ventas por region',
                                    template='plotly_dark',
                                    color='region')
            fig_barras_region.update_traces(textposition='outside', cliponaxis=True)
            fig_barras_region.update_layout(title_x=0.5, title_xanchor='center')
            st.plotly_chart(fig_barras_region, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_barras_region'}})
    
    with tab_datos:    
        st.markdown("#### Datos completos")
        st.dataframe(df_filtrado, hide_index=True, width='stretch', column_config={
            'fecha': st.column_config.DateColumn('Fecha de Venta', format='DD-MM-YYYY')})

