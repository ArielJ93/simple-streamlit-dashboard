import streamlit as st
from modulos.utils import get_assets_path as gap

def inicio_filtros(df):
    if 'filtro_productos' not in st.session_state:
        st.session_state.filtro_productos = df['producto'].unique().tolist()[:10]
    
    if 'filtro_categoria' not in st.session_state:
        st.session_state.filtro_categoria = df['categoria'].unique().tolist()
    
    if 'filtro_region' not in st.session_state:
        st.session_state.filtro_region = df['region'].unique().tolist()
        
    if 'filtro_fechas' not in st.session_state:
        st.session_state.filtro_fechas = [df['fecha'].min().date(), df['fecha'].max().date()]

    if 'seleccionar_todos_productos' not in st.session_state:
        st.session_state.seleccionar_todos_productos = False
    
    

def reiniciar_filtros():
    st.session_state.filtro_productos = []
    st.session_state.filtro_fechas = []
    st.session_state.filtro_categoria = []
    st.session_state.filtro_region = []
    st.session_state.seleccionar_todos_productos = False

def generar_sidebar(df):
    with st.sidebar:
        st.image(gap('logo.png'))
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
        
        lista_categorias = df['categoria'].unique().tolist()
        categorias_seleccionadas = st.multiselect('Filtrar por categoría', lista_categorias, key='filtro_categoria')

        lista_regiones = df['region'].unique().tolist()
        regiones_seleccionadas = st.multiselect('Filtrar por region', lista_regiones, key='filtro_region')
        
    return productos_elegir, categorias_seleccionadas, regiones_seleccionadas

def aplicar_filtros(df, productos_seleccionados, categorias_seleccionadas, regiones_seleccionadas):
    df_filtrado = df[df['producto'].isin(productos_seleccionados)]
    df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_seleccionadas)]   
    df_filtrado= df_filtrado[df_filtrado['region'].isin(regiones_seleccionadas)]
    
    return df_filtrado

def aplicar_filtro_completo(df_filtrado_final, rango_fechas):
    if len(rango_fechas) == 2:
        inicio, fin = rango_fechas
        df_filtrado_completo = df_filtrado_final[(df_filtrado_final['fecha'].dt.date >= inicio) & (df_filtrado_final['fecha'].dt.date <= fin)]
        return df_filtrado_completo
    return df_filtrado_final