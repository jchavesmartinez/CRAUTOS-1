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
import locale

st.set_page_config(
  page_title="DevStack CRAutos",
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

@st.cache_data
def limpiar_data():
    try:
    
        cars_historico=read_file_googledrive(credentials,'1U6BGO_oD0b84FMTChQ5fDy-Oi3XZaWdb')


        cars_historico1=pd.DataFrame(cars_historico)
        #st.write(cars_historico1)


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
            
            car["Price"] = int(car["Price"].replace("¢", "").replace("$", "").replace(",", ""))

            if car["Currency"] == "Dollars":
                car["Price"]=car["Price"]*tipo_de_cambio

        # Cambiar kilometraje

            mileage_str = car['Kilometraje']
            
            if "ND" in mileage_str:
                car['Kilometraje'] = 0
            else:
                mileage_value = int(re.sub(r'[^0-9]', '', mileage_str))  # Extract numeric part
                
                if 'mil' in mileage_str:
                    car['Kilometraje'] = int(mileage_value * 1.60934)  # Convert miles to kilometers
                elif 'k' in mileage_str:
                    car['Kilometraje'] = int(mileage_value)
            
            # Cambiar visualizaciones
            
            car['Visualizaciones']=int(re.sub(r'[^0-9]', '', car['Visualizaciones']))

            # Cambiar costo de traspaso
            try:
                car['Costo de Traspaso (aprox.)'] = int(re.sub(r'[^0-9]', '', car['Costo de Traspaso (aprox.)']))
            except:
                car['Costo de Traspaso (aprox.)'] = 0
            
            # Cambiar fecha de ingreso


            month_map = {
                'Enero': '01',
                'Febrero': '02',
                'Marzo': '03',
                'Abril': '04',
                'Mayo': '05',
                'Junio': '06',
                'Julio': '07',
                'Agosto': '08',
                'Setiembre': '09',
                'Octubre': '10',
                'Noviembre': '11',
                'Diciembre': '12'
            }

            # Split the date string using " de " and " del "
            date_parts = car['Fecha de ingreso'].replace(' del ', ' de ').split(' de ')
            day = date_parts[0]
            month_name = date_parts[1]
            year = date_parts[2]

            # Convert month name to number using the dictionary
            month = month_map[month_name]

            # Construct the formatted date string
            car['Fecha de ingreso']= f"{year}-{month}-{day.zfill(2)}"

        
    
    except Exception as e:
        st.write(e)
        
    
    cars_historico=pd.DataFrame(cars_historico)

    new_column_names = {
        'SKU': 'Vehiculo_ID',
        'Model': 'MarcaModelo',
        'Price': 'Precio',
        'Brand' : 'Marca',
        'Year' : 'Año',
        'Currency' : 'Moneda',
        'Transmisión' : 'Transmision',
        '# de pasajeros' : 'Pasajeros',
        '# de puertas' : 'Puertas'
    }

    cars_historico.rename(columns=new_column_names, inplace=True)

    return cars_historico



def estadisticas_visuales(cars_historico):

    cars_historico = cars_historico.astype(str)
    
    modelo=cars_historico.copy()

    filters = {}
    filtered_df = cars_historico.copy()
    
    with st.expander("Menu de filtros"):

        st.write(cars_historico)

        dynamic_filters = DynamicFilters(cars_historico, filters=['Marca','Cilindrada', 'Estado','Transmision','MarcaModelo','Combustible', 'Color exterior','Placa','Estilo','Pasajeros', 'Color interior','Puertas'])
        dynamic_filters.display_filters(location='columns', num_columns=2)

        df=dynamic_filters.filter_df()

        st.markdown('<hr>', unsafe_allow_html=True)

        try:
            # Ensure the 'Año' column is of integer type
            df['Año'] = df['Año'].astype(int)

            # Create the slider for selecting the year range
            fechafiltro = st.slider('Año', min(df['Año']), max(df['Año']) + 1, (min(df['Año']), max(df['Año']) + 1))

            # Filter the DataFrame based on the selected range
            df = df[(df['Año'] >= fechafiltro[0]) & (df['Año'] <= fechafiltro[1])]

        except Exception as e:
            st.write('Solo existe un elemento, no es posible filtrar más los años')

        try:

            df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

            # Create the slider for selecting the price range
            preciofiltro = st.slider('Precio (Millones)', 
                                    float(min(df['Precio'])/1000000), 
                                    float((max(df['Precio'])+1)/1000000), 
                                    (float(min(df['Precio'])/1000000), float(max(df['Precio'])+1)/1000000), 
                                    step=500000/1000000)

            # Filter the DataFrame based on the selected range
            df = df[(df['Precio'] >= preciofiltro[0]*1000000) & (df['Precio'] <= preciofiltro[1]*1000000)]

        except Exception as e:
            st.write(e)
            st.write('Solo existe un elemento, no es posible filtrar más el precio')
            
        
        try:
        
            kmfiltro = st.slider('Kilometros', int(min(df['Kilometraje'])), int(max(df['Kilometraje']))+1, (int(min(df['Kilometraje'])),int(max(df['Kilometraje']))+1), step=10000)
            df=df[(df['Kilometraje'] >= list(kmfiltro)[0]) & (df['Kilometraje'] <= list(kmfiltro)[1])]
        except Exception as e:
            st.write(e)
            st.write('Solo existe un elemento, no es posible filtrar más el kilometraje')

    with st.expander("Extras"):

        colfiltros6, colfiltros7, colfiltros8 , colfiltros9, colfiltros10, colfiltros11, colfiltros12, colfiltros13 = st.columns([1, 1, 1, 1, 1, 1 , 1, 1])

        with colfiltros6:
            genre1 = st.radio("Dirección hidráulica",["Sin filtro", "Si", "No"])
            genre2 = st.radio("Vidrios eléctricos",["Sin filtro", "Si", "No"])
            genre3 = st.radio("Volante ajustable",["Sin filtro", "Si", "No"])
            genre4 = st.radio("Luces de Xenón/Bixenón",["Sin filtro", "Si", "No"])
            genre5 = st.radio("Sensores frontales",["Sin filtro", "Si", "No"])

            if genre1 != "Sin filtro":
                filters["Dirección hidráulica"] = genre1
            if genre2 != "Sin filtro":
                filters["Vidrios eléctricos"] = genre2
            if genre3 != "Sin filtro":
                filters["Volante ajustable"] = genre3
            if genre4 != "Sin filtro":
                filters["Luces de Xenón/Bixenón"] = genre4
            if genre5 != "Sin filtro":
                filters["Sensores frontales"] = genre5

            df = df[df['Dirección hidráulica'] == genre1] if genre1 != 'Sin filtro' else df
            df = df[df['Vidrios eléctricos'] == genre2] if genre2 != 'Sin filtro' else df
            df = df[df['Volante ajustable'] == genre3] if genre3 != 'Sin filtro' else df
            df = df[df['Luces de Xenón/Bixenón'] == genre4] if genre4 != 'Sin filtro' else df
            df = df[df['Sensores frontales'] == genre5] if genre5 != 'Sin filtro' else df

        with colfiltros7:        
            
            genre6 = st.radio("Aros de lujo",["Sin filtro", "Si", "No"])
            genre7 = st.radio("Bluetooth",["Sin filtro", "Si", "No"])
            genre8 = st.radio("Control de radio en el volante",["Sin filtro", "Si", "No"])
            genre9 = st.radio("Asiento con memoria",["Sin filtro", "Si", "No"])
            genre10 = st.radio("Vidrios tintados",["Sin filtro", "Si", "No"])

            if genre6 != "Sin filtro":
                filters["Aros de lujo"] = genre6
            if genre7 != "Sin filtro":
                filters["Bluetooth"] = genre7
            if genre8 != "Sin filtro":
                filters["Control de radio en el volante"] = genre8
            if genre9 != "Sin filtro":
                filters["Asiento con memoria"] = genre9
            if genre10 != "Sin filtro":
                filters["Vidrios tintados"] = genre10

            df = df[df['Aros de lujo'] == genre6] if genre6 != 'Sin filtro' else df
            df = df[df['Bluetooth'] == genre7] if genre7 != 'Sin filtro' else df
            df = df[df['Control de radio en el volante'] == genre8] if genre8 != 'Sin filtro' else df
            df = df[df['Asiento con memoria'] == genre9] if genre9 != 'Sin filtro' else df
            df = df[df['Vidrios tintados'] == genre10] if genre10 != 'Sin filtro' else df

        with colfiltros8:
            
            genre11 = st.radio("Tapicería de cuero",["Sin filtro", "Si", "No"])
            genre12 = st.radio("Aire acondicionado climatizado",["Sin filtro", "Si", "No"])
            genre13 = st.radio("Llave inteligente/botón de arranque",["Sin filtro", "Si", "No"])
            genre14 = st.radio("Sensor de lluvia",["Sin filtro", "Si", "No"])
            genre15 = st.radio("Aire acondicionado",["Sin filtro", "Si", "No"])

            if genre11 != "Sin filtro":
                filters["Tapicería de cuero"] = genre11
            if genre12 != "Sin filtro":
                filters["Aire acondicionado climatizado"] = genre12
            if genre13 != "Sin filtro":
                filters["Llave inteligente/botón de arranque"] = genre13
            if genre14 != "Sin filtro":
                filters["Sensor de lluvia"] = genre14
            if genre15 != "Sin filtro":
                filters["Aire acondicionado"] = genre15

            df = df[df['Tapicería de cuero'] == genre11] if genre11 != 'Sin filtro' else df
            df = df[df['Aire acondicionado climatizado'] == genre12] if genre12 != 'Sin filtro' else df
            df = df[df['Llave inteligente/botón de arranque'] == genre13] if genre13 != 'Sin filtro' else df
            df = df[df['Sensor de lluvia'] == genre14] if genre14 != 'Sin filtro' else df
            df = df[df['Aire acondicionado'] == genre15] if genre15 != 'Sin filtro' else df

        with colfiltros9:
            
            genre16 = st.radio("Cassette",["Sin filtro", "Si", "No"])
            genre17 = st.radio("Frenos ABS",["Sin filtro", "Si", "No"])
            genre18 = st.radio("Control electrónico de estabilidad",["Sin filtro", "Si", "No"])
            genre19 = st.radio("Monitor de presión de llantas",["Sin filtro", "Si", "No"])
            genre20 = st.radio("Disco compacto",["Sin filtro", "Si", "No"])

            if genre16 != "Sin filtro":
                filters["Cassette"] = genre16
            if genre17 != "Sin filtro":
                filters["Frenos ABS"] = genre17
            if genre18 != "Sin filtro":
                filters["Control electrónico de estabilidad"] = genre18
            if genre19 != "Sin filtro":
                filters["Monitor de presión de llantas"] = genre19
            if genre20 != "Sin filtro":
                filters["Disco compacto"] = genre20

            df = df[df['Cassette'] == genre16] if genre16 != 'Sin filtro' else df
            df = df[df['Frenos ABS'] == genre17] if genre17 != 'Sin filtro' else df
            df = df[df['Control electrónico de estabilidad'] == genre18] if genre18 != 'Sin filtro' else df
            df = df[df['Monitor de presión de llantas'] == genre19] if genre19 != 'Sin filtro' else df
            df = df[df['Disco compacto'] == genre20] if genre20 != 'Sin filtro' else df

        with colfiltros10:
            
            genre21 = st.radio("Bolsa de aire",["Sin filtro", "Si", "No"])
            genre22 = st.radio("Sunroof/techo panorámico",["Sin filtro", "Si", "No"])
            genre23 = st.radio("Control de descenso",["Sin filtro", "Si", "No"])
            genre24 = st.radio("Computadora de viaje",["Sin filtro", "Si", "No"])
            genre25 = st.radio("Radio con USB/AUX",["Sin filtro", "Si", "No"])

            if genre21 != "Sin filtro":
                filters["Bolsa de aire"] = genre21
            if genre22 != "Sin filtro":
                filters["Sunroof/techo panorámico"] = genre22
            if genre23 != "Sin filtro":
                filters["Control de descenso"] = genre23
            if genre24 != "Sin filtro":
                filters["Computadora de viaje"] = genre24
            if genre25 != "Sin filtro":
                filters["Radio con USB/AUX"] = genre25

            df = df[df['Bolsa de aire'] == genre21] if genre21 != 'Sin filtro' else df
            df = df[df['Sunroof/techo panorámico'] == genre22] if genre22 != 'Sin filtro' else df
            df = df[df['Control de descenso'] == genre23] if genre23 != 'Sin filtro' else df
            df = df[df['Computadora de viaje'] == genre24] if genre24 != 'Sin filtro' else df
            df = df[df['Radio con USB/AUX'] == genre25] if genre25 != 'Sin filtro' else df

        with colfiltros11:
            
            genre26 = st.radio("Alarma",["Sin filtro", "Si", "No"])
            genre27 = st.radio("Cámara de retroceso",["Sin filtro", "Si", "No"])
            genre28 = st.radio("Caja de cambios dual",["Sin filtro", "Si", "No"])
            genre29 = st.radio("Retrovisores auto-retractibles",["Sin filtro", "Si", "No"])
            genre30 = st.radio("Revisión Técnica al día",["Sin filtro", "Si", "No"])

            if genre26 != "Sin filtro":
                filters["Alarma"] = genre26
            if genre27 != "Sin filtro":
                filters["Cámara de retroceso"] = genre27
            if genre28 != "Sin filtro":
                filters["Caja de cambios dual"] = genre28
            if genre29 != "Sin filtro":
                filters["Retrovisores auto-retractibles"] = genre29
            if genre30 != "Sin filtro":
                filters["Revisión Técnica al día"] = genre30

            df = df[df['Alarma'] == genre26] if genre26 != 'Sin filtro' else df
            df = df[df['Cámara de retroceso'] == genre27] if genre27 != 'Sin filtro' else df
            df = df[df['Caja de cambios dual'] == genre28] if genre28 != 'Sin filtro' else df
            df = df[df['Retrovisores auto-retractibles'] == genre29] if genre29 != 'Sin filtro' else df
            df = df[df['Revisión Técnica al día'] == genre30] if genre30 != 'Sin filtro' else df

        with colfiltros12:
            
            genre31 = st.radio("Espejos eléctricos",["Sin filtro", "Si", "No"])
            genre32 = st.radio("Desempañador Trasero",["Sin filtro", "Si", "No"])
            genre33 = st.radio("Sensores de retroceso",["Sin filtro", "Si", "No"])
            genre34 = st.radio("Turbo",["Sin filtro", "Si", "No"])
            genre35 = st.radio("Cierre central",["Sin filtro", "Si", "No"])

            if genre31 != "Sin filtro":
                filters["Espejos eléctricos"] = genre31
            if genre32 != "Sin filtro":
                filters["Desempañador Trasero"] = genre32
            if genre33 != "Sin filtro":
                filters["Sensores de retroceso"] = genre33
            if genre34 != "Sin filtro":
                filters["Turbo"] = genre34
            if genre35 != "Sin filtro":
                filters["Cierre central"] = genre35

            df = df[df['Espejos eléctricos'] == genre31] if genre31 != 'Sin filtro' else df
            df = df[df['Desempañador Trasero'] == genre32] if genre32 != 'Sin filtro' else df
            df = df[df['Sensores de retroceso'] == genre33] if genre33 != 'Sin filtro' else df
            df = df[df['Turbo'] == genre34] if genre34 != 'Sin filtro' else df
            df = df[df['Cierre central'] == genre35] if genre35 != 'Sin filtro' else df

        with colfiltros13:
            
            genre36 = st.radio("Control crucero",["Sin filtro", "Si", "No"])
            genre37 = st.radio("Halógenos",["Sin filtro", "Si", "No"])
            genre38 = st.radio("Volante multifuncional",["Sin filtro", "Si", "No"])
            genre39 = st.radio("Asientos eléctricos",["Sin filtro", "Si", "No"])

            if genre36 != "Sin filtro":
                filters["Control crucero"] = genre36
            if genre37 != "Sin filtro":
                filters["Halógenos"] = genre37
            if genre38 != "Sin filtro":
                filters["Volante multifuncional"] = genre38
            if genre39 != "Sin filtro":
                filters["Asientos eléctricos"] = genre39


            df = df[df['Control crucero'] == genre36] if genre36 != 'Sin filtro' else df
            df = df[df['Halógenos'] == genre37] if genre37 != 'Sin filtro' else df
            df = df[df['Volante multifuncional'] == genre38] if genre38 != 'Sin filtro' else df
            df = df[df['Asientos eléctricos'] == genre39] if genre39 != 'Sin filtro' else df
           







st.title('Portal de inversión carros Costa Rica')

cars_historico=limpiar_data()

estadisticas_visuales(cars_historico)





