import streamlit as st

def inicio_filtros(df):
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

def generar_sidebar(df):
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
    
    return productos_elegir, categorias_seleccionadas

def aplicar_filtros(df, productos_seleccionados, categorias_seleccionadas, rango_fechas):
    df_filtrado = df[df['producto'].isin(productos_seleccionados)]

    if len(rango_fechas) == 2:
        inicio, fin = rango_fechas
        df_filtrado = df_filtrado[(df_filtrado['fecha'].dt.date >= inicio) & 
            (df_filtrado['fecha'].dt.date <= fin)]

    df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_seleccionadas)]   
    return df_filtrado