import streamlit as st
import pathlib
import pandas as pd
from typing import Any

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

def get_assets_path(archivo: str) -> str:
    return str(BASE_DIR/'assets'/archivo)


@st.cache_data
def obtener_datos(_conn: Any) -> pd.DataFrame:
    query = 'SELECT fecha, producto, ventas, region, vendedor, categoria FROM ventas_electronica'
    return _conn.query(query)
