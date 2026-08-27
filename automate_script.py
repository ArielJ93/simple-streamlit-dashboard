import pymysql
import os
import streamlit as st  

try:
    host = st.secrets["connections"]["mysql"]["host"]
    user = st.secrets["connections"]["mysql"]["username"]
    password = st.secrets["connections"]["mysql"]["password"]
    database = st.secrets["connections"]["mysql"]["database"]
    port = int(st.secrets["connections"]["mysql"]["port"])
    
except Exception:
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    database = os.environ.get("DB_NAME")
    port = 12369

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        ssl={"ssl": {}})
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT producto FROM ventas_electronica LIMIT 10;")
        resultado = cursor.fetchone()
        print(f"Conexión establecida. Resultado: {resultado}")
        
except Exception as e:
    print(f"Error de conexión: {e}")
    
    
finally:
    if "connection" in locals() and connection.open:
        connection.close()
