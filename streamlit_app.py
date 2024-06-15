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

#@st.cache_data
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

#@st.cache_data
def agrupar_por_años(cars_historico):

    # Determine the minimum and maximum year
    min_year = cars_historico['Año'].min()
    max_year = cars_historico['Año'].max()

    # Create a list of year groups
    year_groups = []
    current_year = min_year
    while current_year <= max_year:
        end_year = current_year + 2
        year_groups.append((current_year, end_year))
        current_year += 3

    # Define a function to assign the year group
    def assign_year_group(year):
        for start, end in year_groups:
            if start <= year <= end:
                return f'{start}-{end}'
        return None

    # Apply the function to create a new column
    cars_historico["Grupo de años"] = cars_historico['Año'].apply(assign_year_group)

    return cars_historico

def estadisticas_visuales(cars_historico):

    df = cars_historico.astype(str)
    
    modelo=df.copy()

    filters = {}
    filtered_df = df.copy()
    
    with st.expander("Menu de filtros"):

        dynamic_filters = DynamicFilters(df, filters=['Marca','Cilindrada', 'Estado','Transmision','MarcaModelo','Combustible', 'Color exterior','Placa','Estilo','Pasajeros', 'Color interior','Puertas'])
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
            df['Kilometraje'] = pd.to_numeric(df['Kilometraje'], errors='coerce').astype('Int64')
            # Ensure there are no NaN values in 'Kilometraje' column
            df = df.dropna(subset=['Kilometraje'])

            # Create the slider for selecting the kilometers range
            kmfiltro = st.slider('Kilometros', int(min(df['Kilometraje'])), int(max(df['Kilometraje'])) + 1, 
                                (int(min(df['Kilometraje'])), int(max(df['Kilometraje'])) + 1), step=10000)

            # Filter the DataFrame based on the selected range
            df = df[(df['Kilometraje'] >= kmfiltro[0]) & (df['Kilometraje'] <= kmfiltro[1])]

        except Exception as e:
            st.write(e)
            st.write('Solo existe un elemento, no es posible filtrar más el kilometraje')

    with st.expander("Extras"):

        colfiltros6, colfiltros7, colfiltros8 , colfiltros9, colfiltros10, colfiltros11, colfiltros12, colfiltros13 = st.columns([1, 1, 1, 1, 1, 1 , 1, 1])

        with colfiltros6:
            genre1 = st.radio("Dirección hidráulica",["Sin filtro", "SI", "NO"])
            genre2 = st.radio("Vidrios eléctricos",["Sin filtro", "SI", "NO"])
            genre3 = st.radio("Volante ajustable",["Sin filtro", "SI", "NO"])
            genre4 = st.radio("Luces de Xenón/Bixenón",["Sin filtro", "SI", "NO"])
            genre5 = st.radio("Sensores frontales",["Sin filtro", "SI", "NO"])

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
            
            genre6 = st.radio("Aros de lujo",["Sin filtro", "SI", "NO"])
            genre7 = st.radio("Bluetooth",["Sin filtro", "SI", "NO"])
            genre8 = st.radio("Control de radio en el volante",["Sin filtro", "SI", "NO"])
            genre9 = st.radio("Asiento con memoria",["Sin filtro", "SI", "NO"])
            genre10 = st.radio("Vidrios tintados",["Sin filtro", "SI", "NO"])

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
            
            genre11 = st.radio("Tapicería de cuero",["Sin filtro", "SI", "NO"])
            genre12 = st.radio("Aire acondicionado climatizado",["Sin filtro", "SI", "NO"])
            genre13 = st.radio("Llave inteligente/botón de arranque",["Sin filtro", "SI", "NO"])
            genre14 = st.radio("Sensor de lluvia",["Sin filtro", "SI", "NO"])
            genre15 = st.radio("Aire acondicionado",["Sin filtro", "SI", "NO"])

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
            
            genre16 = st.radio("Cassette",["Sin filtro", "SI", "NO"])
            genre17 = st.radio("Frenos ABS",["Sin filtro", "SI", "NO"])
            genre18 = st.radio("Control electrónico de estabilidad",["Sin filtro", "SI", "NO"])
            genre19 = st.radio("Monitor de presión de llantas",["Sin filtro", "SI", "NO"])
            genre20 = st.radio("Disco compacto",["Sin filtro", "SI", "NO"])

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
            
            genre21 = st.radio("Bolsa de aire",["Sin filtro", "SI", "NO"])
            genre22 = st.radio("Sunroof/techo panorámico",["Sin filtro", "SI", "NO"])
            genre23 = st.radio("Control de descenso",["Sin filtro", "SI", "NO"])
            genre24 = st.radio("Computadora de viaje",["Sin filtro", "SI", "NO"])
            genre25 = st.radio("Radio con USB/AUX",["Sin filtro", "SI", "NO"])

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
            
            genre26 = st.radio("Alarma",["Sin filtro", "SI", "NO"])
            genre27 = st.radio("Cámara de retroceso",["Sin filtro", "SI", "NO"])
            genre28 = st.radio("Caja de cambios dual",["Sin filtro", "SI", "NO"])
            genre29 = st.radio("Retrovisores auto-retractibles",["Sin filtro", "SI", "NO"])
            genre30 = st.radio("Revisión Técnica al día",["Sin filtro", "SI", "NO"])

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
            
            genre31 = st.radio("Espejos eléctricos",["Sin filtro", "SI", "NO"])
            genre32 = st.radio("Desempañador Trasero",["Sin filtro", "SI", "NO"])
            genre33 = st.radio("Sensores de retroceso",["Sin filtro", "SI", "NO"])
            genre34 = st.radio("Turbo",["Sin filtro", "SI", "NO"])
            genre35 = st.radio("Cierre central",["Sin filtro", "SI", "NO"])

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
            
            genre36 = st.radio("Control crucero",["Sin filtro", "SI", "NO"])
            genre37 = st.radio("Halógenos",["Sin filtro", "SI", "NO"])
            genre38 = st.radio("Volante multifuncional",["Sin filtro", "SI", "NO"])
            genre39 = st.radio("Asientos eléctricos",["Sin filtro", "SI", "NO"])

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
           
    with st.expander('Estadisticas'):

        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce').astype('float')
        
        for column, value in filters.items():
            df = filtered_df[filtered_df[column] == value]
        
        col3, col4, col5, col6, col7 , col8, col9 = st.columns(7)
        col3.metric("Carros totales", len(df['Marca']))
        col4.metric("Precio min", int(min(df['Precio'])))
        col5.metric("Precio promedio", int(df['Precio'].mean()))
        col6.metric("Precio moda", int(df['Precio'].mode().iloc[0]))
        col7.metric("Mediana precio", int(df['Precio'].median()))
        col8.metric("Precio maximo", int(max(df['Precio'])))
        col9.metric("Desviacion estandar relativa", str(int((df['Precio'].std()/df['Precio'].mean())*100))+"%")
    
        st.markdown('<hr>', unsafe_allow_html=True)


        col1, col2 = st.columns([1, 1])

        with col1:

            # grafico1 = st.radio(
            #     "Grafico a mostrar ",
            #     ["Histograma", "Dispersión"],
            #     horizontal=True,
            # )

            #st.markdown('<hr>', unsafe_allow_html=True)

            grafico1='Histograma'


            if grafico1=='Histograma':

                option1 = st.selectbox(
                    'Variable a graficar',
                    ('Grupo de años','MarcaModelo','Marca','Precio','Cilindrada','Estilo','Pasajeros','Combustible','Transmision','Estado','Kilometraje','Placa','Color ext','Color int','Puertas','Provincia'))

                # Create a sample DataFrame (replace this with your 'df' from the CSV)
                data1 = {'values': df[option1].values}
                df1 = pd.DataFrame(data1)

                # Create a histogram using Plotly Express
                fig1 = px.histogram(df1, x='values', nbins=10, title='Histograma '+str(option1))

                fig1.update_layout(
                    plot_bgcolor='white',  # Background color of the plot area
                    paper_bgcolor='white'  # Background color of the entire figure
                )
                
                # Display the histogram in the Streamlit app
                fig1.update_layout(width=760, height=500)

                st.plotly_chart(fig1)

            if grafico1=='Dispersión':

                # Sample data
                np.random.seed(40)
                data = pd.DataFrame({
                    'X': np.random.rand(40),
                    'Y': np.random.rand(40),
                    'Category': np.random.choice(['A', 'B'], size=50)
                })

                # Scatter plot using Plotly Express
                fig4 = px.scatter(data, x='X', y='Y', color='Category', title='Aun en desarrollo')

                fig4.update_layout(width=760, height=500)

                fig4.update_layout(
                    plot_bgcolor='white',  # Background color of the plot area
                    paper_bgcolor='white'  # Background color of the entire figure
                )

                st.plotly_chart(fig4)

        with col2:
            
            
            # grafico2 = st.radio(
            #     "Grafico a mostrar",
            #     ["Histograma", "Dispersión"],
            #     horizontal=True,
            # )

            # st.markdown('<hr>', unsafe_allow_html=True)

            grafico2='Histograma'

            if grafico2=='Histograma':

                option2 = st.selectbox(
                    'Variable a graficar ',
                    ('MarcaModelo','Marca','Precio','Cilindrada','Estilo','Pasajeros','Combustible','Transmision','Estado','Kilometraje','Placa','Color ext','Color int','Puertas','Provincia','Grupo de años'))

                

                # Create a sample DataFrame (replace this with your 'df' from the CSV)
                data2 = {'values': df[option2].values}
                df2 = pd.DataFrame(data2)

                # Create a histogram using Plotly Express
                fig2 = px.histogram(df2, x='values', nbins=10, title='Histograma '+str(option2))

                fig2.update_layout(
                    plot_bgcolor='white',  # Background color of the plot area
                    paper_bgcolor='white'  # Background color of the entire figure
                )
                
                # Display the histogram in the Streamlit app
                fig2.update_layout(width=760, height=500)

                st.plotly_chart(fig2)

            if grafico2=='Dispersión':

                # Sample data
                np.random.seed(42)
                data = pd.DataFrame({
                    'X': np.random.rand(50),
                    'Y': np.random.rand(50),
                    'Category': np.random.choice(['A', 'B'], size=50)
                })

                # Scatter plot using Plotly Express
                fig3 = px.scatter(data, x='X', y='Y', color='Category', title='Aun en desarrollo')

                fig3.update_layout(width=760, height=500)


                fig3.update_layout(
                    plot_bgcolor='white',  # Background color of the plot area
                    paper_bgcolor='white'  # Background color of the entire figure
                )

                st.plotly_chart(fig3)
        
    with st.expander("Potenciales Inversiones"):

        try:
            col1_a, col2_a, col3_a = st.columns(3)

            with col1_a:

                precio_descuento = st.number_input('% Descuento sobre el precio',0,100,10)
                precio_descuento=precio_descuento/100
                km_descuento = st.number_input('% Descuento sobre el kilometraje',0,100,10)
                km_descuento=km_descuento

            with col2_a:

                muestra_tamaño = st.number_input('Tamaño minimo de la muestra',0,10000000000,5)
                nota_final_minima = st.number_input('Nota final minima',0,100,80)

            with col3_a:
                precio_minimo = st.number_input('Precio piso',0,10000000000,700000)
                precio_maximo = st.number_input('Precio techo',0,10000000000,10000000)


            modelo_completo=modelo
            modelo_completo["grupo_id"] = modelo_completo["Marca"].astype(str) + modelo_completo["MarcaModelo"].astype(str) + modelo_completo["Grupo de años"].astype(str)

            modelo['Precio'] = pd.to_numeric(modelo['Precio'], errors='coerce').astype('float')
            modelo['Kilometraje'] = pd.to_numeric(modelo['Kilometraje'], errors='coerce').astype('float')
            modelo['Año'] = pd.to_numeric(modelo['Año'], errors='coerce').astype('float')

            modelo = df.groupby(['Marca', 'MarcaModelo', 'Grupo de años']).agg({'Año': 'mean','Kilometraje':['mean','median'], 'Precio': ['mean', 'count','median','std']}).reset_index()
            modelo.columns = ['Marca', 'MarcaModelo', 'Grupo de años', 'Año_mean','KM_mean','KM_median', 'Precio_mean', 'Precio_count', 'Precio_median','Precio_std']
            modelo['Precio_relativestd']=modelo['Precio_std']/modelo['Precio_mean']*100
            modelo = modelo[modelo['Precio_count'] >= muestra_tamaño]
            modelo["grupo_id"] = modelo["Marca"].astype(str) + modelo["MarcaModelo"].astype(str) + modelo["Grupo de años"].astype(str)

                    # Assuming df1 and df2 are your two DataFrames, and 'common_column' is the column you want to use for merging.
            modelo = pd.merge(modelo_completo, modelo, on='grupo_id', suffixes=('_modelo_completo', '_modelo'))

            # Drop duplicate columns
            modelo = modelo.loc[:, ~modelo.columns.duplicated()]
            modelo['precio_margen_mean']=modelo['Precio']/modelo['Precio_mean']
            modelo['precio_margen_median']=modelo['Precio']/modelo['Precio_median']

            modelo = modelo[modelo['precio_margen_mean'] < 1-precio_descuento]
            modelo = modelo[modelo['precio_margen_median'] < 1-precio_descuento]

            modelo['precio_margen_mean']=modelo['Precio_mean']-modelo['Precio']
            modelo['precio_margen_median']=modelo['Precio_median']-modelo['Precio']

            modelo = modelo[modelo['precio_margen_mean'] >= precio_minimo]
            modelo = modelo[modelo['precio_margen_median'] >= precio_minimo]

            modelo['km_margen_mean']=modelo['Kilometraje']/modelo['KM_mean']*100
            modelo['km_margen_median']=modelo['Kilometraje']/modelo['KM_median']*100

            modelo = modelo[modelo['km_margen_mean'] < 100-km_descuento]
            modelo = modelo[modelo['km_margen_median'] < 100-km_descuento]
            modelo = modelo[modelo['km_margen_mean'] > 0.1]

            modelo['precio_margen_mean%']=modelo['Precio']/modelo['Precio_mean']*100
            modelo['precio_margen_median%']=modelo['Precio']/modelo['Precio_median']*100


            def asignar_nota_marca(valor):
                if valor > 100:
                    return 100
                elif 60 <= valor <= 100:
                    return 90
                elif 30 <= valor < 60:
                    return 80
                elif 15 <= valor < 30:
                    return 60
                elif 5 <= valor < 15:
                    return 40
                else:
                    return None 

            def asignar_nota_precio(row):
                mean_porcentual = row['precio_margen_mean%']
                if mean_porcentual < 60:
                    factor_mean= 100
                elif 60 <= mean_porcentual <= 75:
                    factor_mean= 90
                elif 75 <= mean_porcentual < 85:
                    factor_mean= 80
                elif 85 <= mean_porcentual < 95:
                    factor_mean= 60
                elif 95 <= mean_porcentual < 100:
                    factor_mean= 40


                median_porcentual = row['precio_margen_median%']
                if median_porcentual < 60:
                    factor_median= 100
                elif 60 <= median_porcentual <= 75:
                    factor_median= 90
                elif 75 <= median_porcentual < 85:
                    factor_median= 80
                elif 85 <= median_porcentual < 95:
                    factor_median= 60
                elif 95 <= median_porcentual < 100:
                    factor_median= 40

                mean_dinero = row['precio_margen_mean']
                if mean_dinero > 2000000:
                    factor_mean_dinero= 100
                elif 1000000 <= mean_dinero <= 2000000:
                    factor_mean_dinero= 90
                elif 700000 <= mean_dinero < 1000000:
                    factor_mean_dinero= 80
                elif 300000 <= mean_dinero < 700000:
                    factor_mean_dinero= 60
                elif 0 <= mean_dinero < 300000:
                    factor_mean_dinero= 40
                else:
                    factor_mean_dinero= 0

                median_dinero = row['precio_margen_median']
                if median_dinero > 2000000:
                    factor_median_dinero= 100
                elif 1000000 <= median_dinero <= 2000000:
                    factor_median_dinero= 90
                elif 700000 <= median_dinero < 1000000:
                    factor_median_dinero= 80
                elif 350000 <= median_dinero < 700000:
                    factor_median_dinero= 60
                elif 0 <= median_dinero < 350000:
                    factor_median_dinero= 40
                else:
                    factor_median_dinero= 0

                nota_relativestd= 100-row['Precio_relativestd']

                nota_precio=(factor_mean*0.1)+(factor_mean_dinero*0.1)+(factor_median*0.2)+(factor_median_dinero*0.2)+(nota_relativestd*0.4)

                return nota_precio


            modelo['factor_muestra']=modelo['Precio_count'].apply(asignar_nota_marca)
            modelo['factor_precio'] = modelo.apply(asignar_nota_precio, axis=1)
            modelo['factor_año'] = 100 - (2024-modelo['Año'])
            modelo['factor_km'] = 100-modelo['km_margen_median']


            columns_to_count_indices = list(range(27, 66))
            # Add a new column 'yes_count' to store the count of 'yes' values across specified columns
            modelo['factor_extras'] = modelo.iloc[:, columns_to_count_indices].apply(lambda row: row.eq('SI').sum(), axis=1)
            modelo['factor_extras']=modelo['factor_extras']/39*100

            modelo['nota_final'] = (modelo['factor_muestra']*0.35)+(modelo['factor_precio']*0.25)+(modelo['factor_año']*0.3)+(modelo['factor_km']*0.15)+(modelo['factor_extras']*0.05)

            modelo = modelo[modelo['nota_final'] > nota_final_minima]

            modelo = modelo[modelo['Precio'] <= precio_maximo]

            #columns_to_drop = [1, 3]  # Columns 'B' and 'D' by index
            modelo = modelo.drop(modelo.columns[columns_to_count_indices], axis=1)
            #modelo = modelo.drop(columns=['Color ext', 'Color int','Puertas','Libre impuestos','Negociable','Recibe','Provincia','Traspaso','Vehiculo_ID','Fecha ingreso','Visualizaciones','MarcaModelo_modelo_completo','Moneda','Marca_modelo_completo',
            #                                'Extraccion Dia','Grupo de años_modelo_completo','grupo_id','Visuales por Dia','Año_mean','Grupo de años_modelo','Estado','KM_mean','Precio_mean','Precio_std','precio_margen_mean','precio_margen_median','Precio_relativestd',
            #                                'km_margen_mean','km_margen_median','precio_margen_mean%','precio_margen_median%'])
            modelo = modelo[['URL', 'Marca_modelo_completo','MarcaModelo_modelo_completo','Año','Precio','precio_margen_median', 'Kilometraje','KM_median', 'factor_muestra', 'factor_precio', 'factor_km', 'factor_extras', 'nota_final', 'Nombre', 'Teléfono']]

            new_column_names = {
                'URL': 'Página Web',
                'Marca_modelo_completo': 'Marca',
                'MarcaModelo_modelo_completo': 'Modelo',
                'precio_margen_median' : 'Ganancia Esperada',
                'KM_median' : 'Kilometraje habitual',
                'factor_muestra' : 'Nota Muestra',
                'factor_precio' : 'Nota Precio',
                'factor_km' : 'Nota Kilometraje',
                'factor_extras' : 'Nota Extras',
                'nota_final': 'Nota Final'
            }

            modelo.rename(columns=new_column_names, inplace=True)

            st.dataframe(modelo)
        
        except:
            st.write("No existen potenciales inversiones")
        







st.title('Portal de inversión carros Costa Rica')

cars_historico=limpiar_data()

cars_historico=agrupar_por_años(cars_historico)

estadisticas_visuales(cars_historico)





