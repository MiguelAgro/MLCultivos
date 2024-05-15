import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import utilidades.graficos as gra
import utilidades.tablas_datos as dat
import datetime

# Hecho con entorno 3.9.17 de conda
# Esto es para poner un título a la web
st.set_page_config(
        page_title="Cultivos",
)
st.header("Resultados del cultivo")


with st.sidebar:
    st.header("Menú de opciones")
    selected3 = option_menu(None, ["Home", "Temperaturas",  "Precipitaciones","Temperaturas medias" ,'Tablas','boxplot',"heladas",
                                   "Minimas","Temporada verano","Temporada invierno"], 
    icons=['house', 'cloud-slash', "list-task", 'brightness-alt-low','table','lightning-fill','asterisk','clouds-fill', "sun","cloud-hail-fill" ], 
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

elif selected3 == 'Temporada verano':
   col1, col2, col3,col4,col5 = st.columns(5)
   with col1:
      d1 = st.date_input("Elegir primera fecha", datetime.date(2021, 3, 15))
      temp1 = st.number_input("temperatura baja",min_value=20,max_value=37,value=22)

   with col3:

      b1 =st.button("Ver gráfica")
   
   with col5:
      d2 = st.date_input("Elegir segunda fecha", datetime.date(2021, 10, 20))
      temp2 = st.number_input("temperatura alta",min_value=22,max_value=45, value=37)
   
   
   st.divider()
   if b1:
      result5 = gra.temp_maxima(datos,d1,d2,temp1,temp2)
      st.plotly_chart(result5[0])
      st.write("El número de días con temperatura máxima entre {} y {} grados es de {}".format(temp1,temp2,result5[1]))
   st.divider()
   st.markdown("""
      :red[NOTA: ] :balck[En este gráfico se muestra para los días comprendidos entre las dos fechas seccionadas, las temperaturas máxima
                y mínima de la zona, resaltando en color rojo aquellos casos en los que la temperatura máxima este entre los dos
               datos de temperatura seleccionados (Tener en cuenta que está gráfica tarde un tiempo en su procesamiento)]              
               """)
   
elif selected3 == "Temporada invierno":
   col1, col2, col3 = st.columns(3)
   with col1:
      d1 = st.date_input("Elegir primera fecha", datetime.date(2020, 11, 1))
      d2 = st.date_input("Elegir segunda fecha", datetime.date(2021, 3, 30))
   with col2:
      t1 = st.number_input("Desde temperatura: ",min_value=-15,max_value=5,value=-1)
      t2 = st.number_input("Hasta temperatura: ",min_value=-15,max_value=5,value=1)
   with col3:
      dias = st.number_input("Número de días seguidos: ",min_value=2,max_value=6,value=3)
      boton = st.button("Ver gráfica")
   st.divider()
   if boton:
      result6 = gra.dias_seguidos(datos,d1,d2,t1,t2,dias)
      st.plotly_chart(result6)

   st.divider()
   st.markdown("""
      :red[NOTA: ] :balck[En este gráfico se muestran los días seguidos que hay con unas temperaturas mínimas comprendidas entre 
               las dos temperaturas indicadas en la parte superior, para unas fechas comprendidas entre las seleccionadas en el 
               panel superior. El número de días seguidos, también se seleccionan en el panel superior. Las amplitudes térmicas se indican
               con una línea vertical, que tendrá el color rojo cuando las temperaturas mínimas estén en el intervalo seleccionado)]              
               """)