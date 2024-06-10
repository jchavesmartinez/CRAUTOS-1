import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np
import time
from streamlit import runtime
from streamlit_dynamic_filters import DynamicFilters


# Replace 'raw_csv_url' with the URL of the raw CSV file on GitHub

# Use st.set_page_config to configure the layout
st.set_page_config(
    layout="wide",  # Set the layout to "wide"
    page_title="Portal de inversiones autos",  # Set the title of the app
)

try:

    st.title('Portal de inversión carros Costa Rica')

    #@st.cache
    def load_data():
        # Load or compute your data here (e.g., from a CSV file)
        raw_csv_url = 'https://raw.githubusercontent.com/jchavesmartinez/crautos/main/MASTERDATA%20-%20LIMPIA.csv'
        df = pd.read_csv(raw_csv_url, encoding='latin-1')
        df['Kilometraje'] = df['Kilometraje'].fillna(1)
        return df

    # Load the data using the cached function
    df = load_data()

    modelo=df.copy()

    filters = {}
    filtered_df = df.copy()


    with st.expander("Menu de filtros"):

        dynamic_filters = DynamicFilters(df, filters=['Marca','Cilindrada', 'Estado','Transmision','MarcaModelo','Combustible', 'Color ext','Placa','Estilo','Pasajeros', 'Color int','Puertas'])
        dynamic_filters.display_filters(location='columns', num_columns=2)


        df=dynamic_filters.filter_df()

        st.markdown('<hr>', unsafe_allow_html=True)

        try:

            fechafiltro = st.slider('Año', min(df['Año']), max(df['Año'])+1, (min(df['Año']), max(df['Año'])+1))
            df=df[(df['Año'] >= list(fechafiltro)[0] ) & (df['Año'] <= list(fechafiltro)[1])]

        except:
            st.write('Solo existe un elemento, no es posible filtrar más los años')

        try:
        
            preciofiltro = st.slider('Precio (Millones)', float(min(df['Precio'])/1000000), float((max(df['Precio'])+1)/1000000), (float(min(df['Precio']))/1000000,float(max(df['Precio'])+1)/1000000), step=500000/1000000)
            df=df[(df['Precio'] >= list(preciofiltro)[0]*1000000 ) & (df['Precio'] <= list(preciofiltro)[1]*1000000)]

        except:
            st.write('Solo existe un elemento, no es posible filtrar más el precio')
            
        try:
        
            kmfiltro = st.slider('Kilometros', int(min(df['Kilometraje'])), int(max(df['Kilometraje']))+1, (int(min(df['Kilometraje'])),int(max(df['Kilometraje']))+1), step=10000)
            df=df[(df['Kilometraje'] >= list(kmfiltro)[0]) & (df['Kilometraje'] <= list(kmfiltro)[1])]
        except:
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
            
    with st.expander('Estadisticas'):

        for column, value in filters.items():
            df = filtered_df[filtered_df[column] == value]      


        
        col3, col4, col5, col6, col7 , col8, col9 = st.columns(7)
        col3.metric("Carros totales", len(df['Marca']))
        col4.metric("Precio min", int(min(df['Precio'])))
        col5.metric("Precio promedio", int(df['Precio'].mean()))
        col6.metric("Precio moda", int(df['Precio'].mode()))
        col7.metric("Mediana precio", int(df['Precio'].median()))
        col8.metric("Precio maximo", int(max(df['Precio'])))
        col9.metric("Desviacion estandar relativa", str(int((df['Precio'].std()/df['Precio'].mean())*100))+"%")
    
        st.markdown('<hr>', unsafe_allow_html=True)


        col1, col2 = st.columns([1, 1])

        with col1:

            grafico1 = st.radio(
                "Grafico a mostrar ",
                ["Histograma", "Dispersión"],
                horizontal=True,
            )

            st.markdown('<hr>', unsafe_allow_html=True)


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
            
            
            grafico2 = st.radio(
                "Grafico a mostrar",
                ["Histograma", "Dispersión"],
                horizontal=True,
            )

            st.markdown('<hr>', unsafe_allow_html=True)


            if grafico2=='Histograma':

                option2 = st.selectbox(
                    'WENAS',
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

        
        modelo['factor_marca']=modelo['Precio_count'].apply(asignar_nota_marca)
        modelo['factor_precio'] = modelo.apply(asignar_nota_precio, axis=1)
        modelo['factor_año'] = 100 - (2023-modelo['Año'])
        modelo['factor_km'] = 100-modelo['km_margen_median']


        columns_to_count_indices = list(range(3, 42))
        # Add a new column 'yes_count' to store the count of 'yes' values across specified columns
        modelo['factor_extras'] = modelo.iloc[:, columns_to_count_indices].apply(lambda row: row.eq('Si').sum(), axis=1)
        modelo['factor_extras']=modelo['factor_extras']/len(columns_to_count_indices)*100

        modelo['nota_final'] = (modelo['factor_marca']*0.35)+(modelo['factor_precio']*0.25)+(modelo['factor_año']*0.3)+(modelo['factor_km']*0.15)+(modelo['factor_extras']*0.05)

        modelo = modelo[modelo['nota_final'] > nota_final_minima]

        modelo = modelo[modelo['Precio'] <= precio_maximo]

        #columns_to_drop = [1, 3]  # Columns 'B' and 'D' by index
        modelo = modelo.drop(modelo.columns[columns_to_count_indices], axis=1)
        modelo = modelo.drop(columns=['Color ext', 'Color int','Puertas','Libre impuestos','Negociable','Recibe','Provincia','Traspaso','Vehiculo_ID','Fecha ingreso','Visualizaciones','MarcaModelo_modelo_completo','Moneda','Marca_modelo_completo',
                                        'Extraccion Dia','Grupo de años_modelo_completo','grupo_id','Visuales por Dia','Año_mean','Grupo de años_modelo','Estado','KM_mean','Precio_mean','Precio_std','precio_margen_mean','precio_margen_median','Precio_relativestd',
                                        'km_margen_mean','km_margen_median','precio_margen_mean%','precio_margen_median%'])

        modelo = modelo[['Marca_modelo', 'MarcaModelo_modelo','Combustible','Transmision','Estilo','Cilindrada','Año', 'Precio','Precio_median','Kilometraje','KM_median','Precio_count','nota_final','factor_marca','factor_precio','factor_año','factor_km','factor_extras','Comentarios','Pagina Web']]
        st.dataframe(modelo)




except Exception as e:
    st.error(f"An error occurred: {str(e)}")
