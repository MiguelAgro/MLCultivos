import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import utilidades.graficos as gra
import utilidades.tablas_datos as dat

# Hecho con entorno 3.9.17 de conda
# Esto es para poner un título a la web
st.set_page_config(
        page_title="Cultivos",
)
st.header("Resultados del cultivo")


with st.sidebar:
    st.header("Menú de opciones")
    selected3 = option_menu(None, ["Home", "Temperaturas",  "Precipitaciones","Temperaturas medias" ,'Tablas','boxplot',"heladas","Minimas"], 
    icons=['house', 'cloud-slash', "list-task", 'brightness-alt-low','table','lightning-fill','asterisk','clouds-fill' ], 
    menu_icon="cast", default_index=0, orientation="vertical",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
      }
   )


@st.cache_data
def lectura():
   df = pd.read_parquet('data/dataset.parquet')
   # ordenamos por la columna fecha
   df = df.sort_values(by=['fecha'])
   # quitamos las comas y lo sustituimos por puntos para algunos campos
   df['temp_max'] = pd.to_numeric(df['temp_max'].str.replace(',', '.'))
   df['temp_min'] = pd.to_numeric(df['temp_min'].str.replace(',', '.'))
   # creo una columna denominada "heladas", vale 1 si hay helada y cero en caso contrario
   df["heladas"] = 0
   for row in df.itertuples():
    if row.temp_min <=0:
        df.loc[row.Index,'heladas']=1

   return df

datos = lectura()

if selected3 == 'Home':
   st.write("Resultados obtenidos de fichero de temperaturas")
   st.write("actualizar esta página con el contenido que se desee")

elif selected3 == 'Temperaturas':
   resul = gra.temperaturas(datos)
   st.plotly_chart(resul) 

   st.divider()
   st.markdown("""
   :red[NOTA: ] :balck[En este gráfico se muestran las temperaturas máximas y mínimas observadas en la zona durante todo el período de estudio. Se puede hacer zoom 
               utilizando los elementos que están debajo del gráfico y desplazándolos a la derecha o a la izquierda]
   """)     

elif selected3 == 'Precipitaciones':
   resul = gra.precipitaciones(datos)
   st.plotly_chart(resul)

   st.divider()
   st.markdown("""
   :red[NOTA: ] :balck[En este gráfico se muestran las precipitaciones observadas en la zona durante todo el período de estudio. Se puede hacer zoom 
               utilizando los elementos que están debajo del gráfico y desplazándolos a la derecha o a la izquierda]
   """) 

elif selected3=='Tablas':
   dat.tablas(datos)
 

elif selected3 == 'Temperaturas medias':
   resul2 = gra.temp_medias(datos)
   st.plotly_chart(resul2)

   st.divider()
   st.markdown("""
   :red[NOTA: ] :balck[En este gráfico se muestra lo siguiente: para cada año y mes se calcula la media de las temperaturas mínimas y se muestra  su representación 
               en este gráfico ]
   """)

elif selected3 == 'boxplot':
   display = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre", "Noviembre","Diciembre"]
   options = list(range(len(display)))
   valor = st.selectbox("Elegir el mes", options, format_func=lambda x: display[x])
   resul3 = gra.boxplot(datos,valor+1)
   st.plotly_chart(resul3)

   st.markdown("""
   :red[NOTA: ] :balck[En este gráfico se debe elegir un mes en la parte superior del mismo, y para el mes indicado se obtienen los boxplot obtenidos para cada
               año estudiado.Para entender este tipo de gráficos, se aconseja acudir a ver el contenido que hay 
               en [ este enlace](https://www.pgconocimiento.com/diagrama-boxplot/) ]
   """)

elif selected3 == 'heladas':

   col1, col2, col3 = st.columns(3)
   with col1:
      val_dia = st.number_input("Dar el día del mes:",min_value=1, max_value=30)

   with col3:
      display = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre", "Noviembre","Diciembre"]
      options = list(range(len(display)))
      valor_mes = st.selectbox("Elegir el mes", options,index= 6 ,format_func=lambda x: display[x])

   st.divider()
   dat.ultima_helada(datos,val_dia,valor_mes+1)

elif selected3 == 'Minimas':
      display = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre", "Noviembre","Diciembre"]
      options = list(range(len(display)))
      valor_mes = st.selectbox("Elegir el mes", options,format_func=lambda x: display[x])  

      st.divider()
      resul4 = gra.mes_minima(datos,valor_mes+1)
      st.plotly_chart(resul4)

      st.divider()
      st.markdown("""
      :red[NOTA: ] :balck[En este gráfico se muestra para el mes seleccionado, las temperaturas mínimas observadas cada año. 
                  Inicialmente sólo se muestran dos líneas para dar claridad al gráfico, pero se pueden mostrar/ocultar TODAS las líneas, sin más que hacer click en el apartado de 
                  leyenda en la serie que se quiere mostrar/ocultar]
      """)      