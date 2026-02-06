import streamlit as st
import pandas as pd
import datetime

class Delta():
        
        def __init__(self, df_filtrado, inicio, fin):
                self.df_filtrado = df_filtrado
                self.inicio = inicio
                self.fin = fin
                
                cantidad_dias = (fin - inicio).days + 1
                self.final_previo = inicio - datetime.timedelta(days=1) 
                self.inicio_previo = self.final_previo - datetime.timedelta(days=cantidad_dias - 1)
                self.periodo_actual = (df_filtrado['fecha'].dt.date >= inicio) & (df_filtrado['fecha'].dt.date <= fin)
                self.periodo_previo = (df_filtrado['fecha'].dt.date >= self.inicio_previo) & (df_filtrado['fecha'].dt.date <= self.final_previo)
               
                
        def total_ventas(self):      
                valor_actual = self.df_filtrado.loc[self.periodo_actual, 'ventas'].sum()
                valor_previo = self.df_filtrado.loc[self.periodo_previo, 'ventas'].sum()
                
                if valor_previo == 0 or pd.isna(valor_previo):
                        calculo_delta = 0.0
                        return calculo_delta, valor_actual, valor_previo
                calculo_delta = ((valor_actual - valor_previo) / valor_previo) * 100
                return calculo_delta, valor_actual, valor_previo
        
        def conteo_producto(self):
                conteo_actual = self.df_filtrado.loc[self.periodo_actual, 'producto'].nunique()
                conteo_previo = self.df_filtrado.loc[self.periodo_previo, 'producto'].nunique()
                diferencia_conteo = conteo_actual - conteo_previo
                return conteo_actual, conteo_previo, diferencia_conteo
        
        def promedio_ventas(self):
                datos_actual = self.df_filtrado.loc[self.periodo_actual, 'ventas']
                datos_previo = self.df_filtrado.loc[self.periodo_previo, 'ventas']
                
                prom_actual = datos_actual.mean() if not datos_actual.empty else 0
                prom_previo = datos_previo.mean() if not datos_previo.empty else 0
                
                if prom_previo == 0:
                        diferencia_prom = 0.0
                else:
                        diferencia_prom = ((prom_actual - prom_previo) / prom_previo) * 100
                return prom_actual, prom_previo, diferencia_prom
        
def metrica_total_ventas(df_filtrado, inicio, fin):
        dta_vnt = Delta(df_filtrado, inicio, fin)
        calculo_delta, valor_actual, valor_previo = dta_vnt.total_ventas()
        st.metric('Ventas Totales',
        f'${valor_actual:,.0f}',
        delta= f'{calculo_delta:.1f}%')
        with st.expander('Comparación'):
                st.write(f'**-Actual: {dta_vnt.inicio} al {dta_vnt.fin} (${valor_actual:,.0f})**')
                st.write(f'**-Previo: {dta_vnt.inicio_previo} al {dta_vnt.final_previo} (${valor_previo:,.0f})**')

def metrica_cant_productos(df_filtrado, inicio, fin):
        dta_cont = Delta(df_filtrado, inicio, fin)
        conteo_actual, conteo_previo, dif_conteo = dta_cont.conteo_producto()
        st.metric('Productos activos',
        conteo_actual,
        delta=dif_conteo)
        with st.expander('Comparación'):
                st.write(f'**-Actual: {dta_cont.inicio} al {dta_cont.fin} ({conteo_actual})**')
                st.write(f'**-Previo: {dta_cont.inicio_previo} al {dta_cont.final_previo} ({conteo_previo})**')
                
def metrica_prom_ventas(df_filtrado, inicio, fin):
        dta_prom = Delta(df_filtrado, inicio, fin)
        prom_actual, prom_previo, dif_prom = dta_prom.promedio_ventas()
        st.metric('Promedio',
        f'{prom_actual:,.0f}',
        delta= f'{dif_prom:.1f}%')
        with st.expander('Comparación'):
                st.write(f'**-Actual: {dta_prom.inicio} al {dta_prom.fin} ({prom_actual:.1f})**')
                st.write(f'**-Previo: {dta_prom.inicio_previo} al {dta_prom.final_previo} ({prom_previo:.1f})**')