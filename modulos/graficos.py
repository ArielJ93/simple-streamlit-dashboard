import streamlit as st
import plotly.express as px
import pandas as pd

def grafico_linea(df_filtrado_completo: pd.DataFrame) -> None:
    ventas_categoria = df_filtrado_completo.groupby(['fecha','categoria'])['ventas'].sum().reset_index()
    fig_lineas = px.line(ventas_categoria, x='fecha', y='ventas',
                        title='Tendencia de Ventas',
                        template='plotly_dark',
                        color='categoria',
                        markers=True)
    fig_lineas.update_layout(title_x=0.5, title_xanchor='center')
    st.plotly_chart(fig_lineas, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_lineas'}})
    
def grafico_barra_producto(df_filtrado_completo: pd.DataFrame) -> None:
    ventas_topproductos = df_filtrado_completo.nlargest(10, 'ventas').reset_index()
    fig_barras = px.bar(ventas_topproductos, y='producto', x='ventas',
                        title='Ventas por producto <br>(solo puedes seleccionar hasta 10 productos)',
                        template='plotly_dark',
                        orientation='h',
                        )
    fig_barras.update_traces(textposition='outside', cliponaxis=False)
    fig_barras.update_layout(title_x=0.5, title_xanchor='center', yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_barras, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_barras_productos'}})
    
    
def grafico_torta(df_filtrado_completo: pd.DataFrame) -> None:
    ventas_vendedor = df_filtrado_completo.groupby('vendedor')['ventas'].sum().reset_index()
    fig_pie =px.pie(ventas_vendedor, names='vendedor', values='ventas', 
                    color='vendedor', 
                    title='Ventas($) por vendedor', 
                    template= 'plotly_dark', 
                    hole=0.3)
    fig_pie.update_traces(textfont_size=14, textfont_color='black')
    fig_pie.update_layout(title_x=0.5, title_xanchor='center')
    st.plotly_chart(fig_pie, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_tortas_vendedores'}})
    
def grafico_barra_region(df_filtrado_completo: pd.DataFrame) -> None:
    ventas_region = df_filtrado_completo.groupby('region')['ventas'].sum().reset_index()
    fig_barras_region = px.bar(ventas_region, x='region', y='ventas',
                            title='Ventas por region',
                            template='plotly_dark',
                            color='region')
    fig_barras_region.update_traces(textposition='outside', cliponaxis=True)
    fig_barras_region.update_layout(title_x=0.5, title_xanchor='center')
    st.plotly_chart(fig_barras_region, width='stretch', theme=None, config={'toImageButtonOptions': {'filename':'Gráfico_barras_region'}})
    
    