import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import json
import pandas as pd
import re
import pydeck as pdk
import numpy as np
from streamlit_dynamic_filters import DynamicFilters
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import numpy as np

st.set_page_config(
  page_title="DevStack ERP",
  page_icon="🤑",
  layout="wide",
)


#---------------------------- Variables generales --------------------------------


credentials = {
    "type": "service_account",
    "project_id": "devstackerp",
    "private_key_id": "3a7d1511ed3d81296b76f192794449c8145de068",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDp5iCeNNQl7WO3\nHwBSsnBazysuke/CjA9V5Pu+V9j0+PetgQgJbbHHkGzvC1W2vkXaZDD/veTn69Fq\n7VL2snWmna2OUg+j03j/zZtI2m8AHJNUoUvGKXAaYcUO1wrinGCPRrpcioNl8ZvO\nnJcfWuO/siPO0iT7L7xgYtAqd2RSHYGzY/9Q/2BdA2XtrPEu2VT79fVocJDwKZ9W\nnU9slh2aE7CDKDjn2ljiQXSrx6NkZyEdEdm/oaEd+2zvacx/zTpFpSzKCavj4h+y\n/iSgVZ0YKkc4QgUhWIQFUfq3/4Sk81K2CCjHSXSz0H4lh7qsO6yqoe1LU/IqwfJH\nabcVScFfAgMBAAECggEAVIqhb42YwLy1NhM2gq2MfsYyzXpiNud5A4rokzwdZy42\nF7hztzS29XL2bNCkApFzniRosYdpnYpW/1cYjaKjc726ZZ6zmHtvWMZwQjzxshCi\nEAzc3ptLsb11BJAllxL+s8rUwW4vYEGcF2nyFZs8hqVU3ASI6WGvrQcKRs8wq5zd\num2nnQuvVYVfCtGcp5qlcrDBgJV5EBy8H13mmAZSQo88UtK39KLc2qih2HFAmZnM\nJCjZj6EiJ57G4HuL1EF1pr6fIPzVgsYl6LFZ3MCr5qxrVYi8UxozdLVhka2jLLY1\nZSz+IOa4gm66nlYjdJoypmRFCXJrS4xVaTdah0DOQQKBgQD6sjAUFxNA1Fe0AdIc\nQdQnW9jcynLaXYSMqWZ/D7WsNnE7AVTnPuPuM/tY4jrxA4YNOUwVhJJxfRCgtWWt\nUwpBn0iFrh3oOWcLAi1fxoxj76b+mtzjuVEBSBmBvsIvnQJOpTWNfPp2OsnZwwz4\n3oGBeQ1bhCcTZK2rUE7tc7QAkwKBgQDu2PavXl8mhhzReeWlA/BftoaHWr0GfEaz\nyeVkqNHOlKPEl+Hmdb/YmEEhvcIHmC+a9UT4RdZdRRboPy1m2Z53OJn5VYuNuIil\nsStZO15xBEik1/gWeKUjTVX5HQqdoTccJpWINLpx95uNrZpLafsbMVUowdIgEipm\nYC9pEs7XhQKBgFtewmMwHdZNDkIPP9MIsxg9Q4cFSmMIHp1dyHua8C36Eb7dt2Io\n684PqBY3LiBVlnAPaAmXrgArAvpv4sUPNPfB5B7E3SWcdk/u1TbJGLX7zLOTIdrl\n2f5LlvBQ5FmSMhsT37bXzDl3J8Z0bq/t+OmFgzbNrahF035S4NFukDZ9AoGAQYNR\nZpjEEJUIooyE6NZDwH0YOVgyMO01l2rxeMK1iaxLn0jptYTmskpQ0yhxaBPeOuq7\nmD3PppWkyt9JXMSkKp9j3HgSZzUOhiQqd7dJGEbMhiqW6dL9uMklo8bLeqEVtKsA\nqPONkGUSTbIoeDcBoVvOt/cx44oYByyq1G9MPOECgYAPzv5Q93oiMAJlWVuzv1RV\nw9HpOD6pv5ryPMMd/q+qrWfJDz5wYoU4ccTRh0CzgERNKRPCy7zNMqCHRp0xTqBU\nyGMjJY6w1fvZYoqXVa2TVB3gXnb64v3guG2N8wHpK9qeAciN4G/IrCy5a9IQv45o\nSF/AbO/1i7rBpBtwfDuhZQ==\n-----END PRIVATE KEY-----\n",
    "client_email": "itdevstack@devstackerp.iam.gserviceaccount.com",
    "client_id": "100362920078189694738",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/itdevstack%40devstackerp.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}


#---------------------------- Funciones generales --------------------------------

def read_file_googledrive(credentials,file_id):

    try:
        credentials_pdf = service_account.Credentials.from_service_account_info(credentials, scopes=['https://www.googleapis.com/auth/drive'])

        # Build the Drive service
        drive_service = build('drive', 'v3', credentials=credentials_pdf)

        # Request the file content
        file_content = drive_service.files().get_media(fileId=file_id).execute()

        # Convert bytes content to string
        text_content = file_content.decode('utf-8')  # Assuming UTF-8 encoding
        text_content = json.loads(file_content)
         
    except Exception as e:
        print(f"Error: {str(e)}")
        print("No fue posible leer el file")
        text_content=[]
    
    return text_content



#---------------------------- Funciones especificas --------------------------------

#@st.cache_data
def limpiar_data():
    try:
    
        cars_historico=read_file_googledrive(credentials,'1U6BGO_oD0b84FMTChQ5fDy-Oi3XZaWdb')


        cars_historico1=pd.DataFrame(cars_historico)
        st.write(cars_historico1)


        # Eliminar filas que no tienen datos

        if isinstance(cars_historico, list) and all(isinstance(car, dict) for car in cars_historico):
            cars_historico = [car for car in cars_historico if car.get("Brand")]

        # Precio publicado

        tipo_de_cambio=520

        for car in cars_historico:
            if car["Price"].startswith("¢"):
                car["Currency"] = "Colones"
            elif car["Price"].startswith("$"):
                car["Currency"] = "Dollars"
            else:
                car["Currency"] = "Unknown"



        
    
    except Exception as e:
        st.write(e)
    
    
    
    cars_historico=pd.DataFrame(cars_historico)
    st.write(cars_historico)
    









limpiar_data()
st.write("hila")

