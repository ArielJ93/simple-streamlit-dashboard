import streamlit as st
import pandas as pd
import datetime
from typing import Any 


def formateo(valor: float, texto_none: str | None, es_porcentaje = True) -> None | str | float: 
        if pd.isna(valor):
                return texto_none
        return f"{valor:.1f}%" if es_porcentaje else valor

class Delta():
        
        def __init__(self, df_filtrado: pd.DataFrame, inicio: datetime.date, fin: datetime.date) -> None:
                self.df_filtrado = df_filtrado
                self.inicio = inicio
                self.fin = fin
                
                cantidad_dias = (fin - inicio).days + 1
                self.final_previo = inicio - datetime.timedelta(days=1) 
                self.inicio_previo = self.final_previo - datetime.timedelta(days=cantidad_dias - 1)
                self.periodo_actual = (df_filtrado['fecha'].dt.date >= inicio) & (df_filtrado['fecha'].dt.date <= fin)
                self.periodo_previo = (df_filtrado['fecha'].dt.date >= self.inicio_previo) & (df_filtrado['fecha'].dt.date <= self.final_previo)
               
                
        def total_ventas(self) -> dict[str, Any]:      
                valor_actual = self.df_filtrado.loc[self.periodo_actual, 'ventas'].sum()
                valor_previo = self.df_filtrado.loc[self.periodo_previo, 'ventas'].sum()
                
                if pd.isna(valor_previo):
                        calculo_delta = None
                else:
                        calculo_delta = ((valor_actual - valor_previo) / valor_previo) * 100 if valor_previo !=0 else 0.0
                return {
                        'delta': calculo_delta,
                        'valor': valor_actual, 
                        'comparacion': valor_previo}
        
        def conteo_producto(self) -> dict[str, Any]:
                conteo_actual = self.df_filtrado.loc[self.periodo_actual, 'producto'].nunique()
                conteo_previo = self.df_filtrado.loc[self.periodo_previo, 'producto'].nunique()
                diferencia_conteo = conteo_actual - conteo_previo
                return {
                        'valor': conteo_actual, 
                        'comparacion': conteo_previo, 
                        'delta': diferencia_conteo}
        
        def promedio_ventas(self) -> dict[str, Any]:
                datos_actual = self.df_filtrado.loc[self.periodo_actual, 'ventas']
                datos_previo = self.df_filtrado.loc[self.periodo_previo, 'ventas']
                
                prom_actual = datos_actual.mean() 
                prom_previo = datos_previo.mean() 
                
                if pd.isna(prom_previo):
                        diferencia_prom = None
                else:
                        diferencia_prom = ((prom_actual - prom_previo) / prom_previo) * 100 if prom_previo !=0 else 0.0
                return {
                        'valor': prom_actual, 
                        'comparacion': prom_previo, 
                        'delta': diferencia_prom}
        
def metrica_total_ventas(objeto_delta: Delta) -> None:
        datos = objeto_delta.total_ventas()
        st.metric('Ventas Totales',
        f"${datos['valor']:,.0f}",
        delta= formateo(datos['delta'], texto_none= "Sin datos previos"))
        with st.expander('Comparación'):
                st.write(f"**-Actual: {objeto_delta.inicio} al {objeto_delta.fin} (${datos['valor']:,.0f})**")
                st.write(f"**-Previo: {objeto_delta.inicio_previo} al {objeto_delta.final_previo} (${datos['comparacion']:,.0f})**")

def metrica_cant_productos(objeto_delta: Delta) -> None:
        datos = objeto_delta.conteo_producto()
        st.metric('Productos activos',
        datos['valor'],
        delta=formateo(datos['delta'], texto_none= "Sin datos previos", es_porcentaje=False))
        with st.expander('Comparación'):
                st.write(f"**-Actual: {objeto_delta.inicio} al {objeto_delta.fin} ({datos['valor']})**")
                st.write(f"**-Previo: {objeto_delta.inicio_previo} al {objeto_delta.final_previo} ({datos['comparacion']})**")
                
def metrica_prom_ventas(objeto_delta: Delta) -> None:
        datos = objeto_delta.promedio_ventas()
        st.metric('Promedio',
        f"{datos['valor']:,.1f}",
        delta= formateo(datos['delta'], texto_none= "Sin datos previos"))
        with st.expander('Comparación'):
                st.write(f"**-Actual: {objeto_delta.inicio} al {objeto_delta.fin} ({datos['valor']:.1f})**")
                st.write(f"**-Previo: {objeto_delta.inicio_previo} al {objeto_delta.final_previo} ({datos['comparacion']:.1f})**")