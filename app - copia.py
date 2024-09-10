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
st.markdown( "# :green[AGROINDUSTRIAL  ASESORES] #"  )


with st.sidebar:
    st.header("Menú de opciones")
    selected3 = option_menu(None, ["Home", "Temperaturas",  "Precipitaciones","Temperaturas medias" ,'Tablas','boxplot',"heladas",
                                   "Minimas","Temporada verano","Temporada invierno","Predicción densidad"], 
    icons=['house', 'cloud-slash', "list-task", 'brightness-alt-low','table','lightning-fill','asterisk','clouds-fill', "sun",
           "cloud-hail-fill","bi-bucket-fill" ], 
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
   df['precipitacion'] = pd.to_numeric(df['precipitacion'].str.replace(',', '.'))
   # creo una columna denominada "heladas", vale 1 si hay helada y cero en caso contrario
   df["heladas"] = 0
   for row in df.itertuples():
    if row.temp_min <=0:
        df.loc[row.Index,'heladas']=1

   return df

datos = lectura()

if selected3 == 'Home':
   st.write("AGROINDUSTRIAL ASESORES es una consultoría tecnológica con más de 15 años de experiencia en los campos de la agronomía, veterinaria, medioambiente,\
             agroenergías, vitivinicultura e industria agroalimentaria en general. Disponemos de un plantel de técnicos con amplia experiencia en la definición,\
             gestión y financiación de proyectos de I+D+i en todos los sectores agropecuarios e industriales dispuestos a ayudarle a llevar \
            a la realidad sus inquietudes innovadoras.")
   st.markdown("<br><br><br>",unsafe_allow_html=True)
   b1,b2,b3 = st.columns(3)
   with b2:
      st.image("img/logo.png")
   
   st.markdown("<br><br><br> En este sitio web puedes ver nuestra sección de I+D+i para ayudarte en la implantación y desarrollo de herramientas\
               de su emprea. Puedes pasar a <a href='http://www.agroindustrialasesores.com/#' target='_blank'> nuestra página web central en este enlace </a>.",unsafe_allow_html=True)

elif selected3 == 'Temperaturas':
   anios = list(datos.year_fecha.unique())
   anio = st.selectbox("seleccionar un año:",anios, help="Con el año seleccionado se mostrarán las temperaturas máxima y mínimas observadas")
   resul = gra.temperaturas(datos,anio)
   st.plotly_chart(resul[0]) 
   col1,col2,col3 =st.columns(3)
   with col2:
      with st.popover("Ver resumen estadístico"):
         st.subheader("Resumen estadístico de la amplitud térmica")
         st.write("(para el año seleccionado)")
      
         st.write("El número total de observaciones es de: "+str(resul[1][0]))
         st.write("La media de las amplitudes térmicas para el año seleccionado es de: ",str(round(resul[1][1],2)))
         st.write("La desviación respecto de la media de las amplitudes térmicas para el año seleccionado es de: ",str(round(resul[1][2],2)))
         st.write("El máximo de las amplitudes térmicas para el año seleccionado es de: ",str(round(resul[1][7],2)))
         st.write("El mínimo de las amplitudes térmicas para el año seleccionado es de: ",str(round(resul[1][3],2)))
         st.write("El 25% de las amplitudes térmicas para el año seleccionado tienen  un valor por debajo de: ",str(round(resul[1][4],2)))
         st.write("El 50% de las amplitudes térmicas para el año seleccionado tienen  un valor por debajo de: ",str(round(resul[1][5],2)))
         st.write("El 75% de las amplitudes térmicas para el año seleccionado tienen  un valor por debajo de: ",str(round(resul[1][6],2)))

   st.divider()
   st.markdown("""
   :red[NOTA: ] :balck[En este gráfico se muestran las temperaturas máximas y mínimas observadas en la zona durante todo el período de estudio. Se puede hacer zoom 
               utilizando los elementos que están debajo del gráfico y desplazándolos a la derecha o a la izquierda]
   """)     

elif selected3 == 'Precipitaciones':
   anios = list(datos.year_fecha.unique())
   anio = st.selectbox("seleccionar un año:",anios, help="Con el año seleccionado se mostrarán las precipitaciones observadas para ese año")
  
   resul = gra.precipitaciones(datos,anio)
   st.plotly_chart(resul[0])
   col1,col2,col3 =st.columns(3)
   with col2:
      with st.popover("Ver resumen estadístico"):
         st.subheader("Resumen estadístico de los días que han llovido en el año seleccionado")
               
         st.write("El número total de días con lluvia es de: "+str(resul[1][0]))
         st.write("La media de la cantidad caída  para el año seleccionado es de: ",str(round(resul[1][1],2)))
         st.write("La desviación respecto de la media de la cantidad de lluvia para el año seleccionado es de: ",str(round(resul[1][2],2)))
         st.write("El máximo de lluvia caída para el año seleccionado es de: ",str(round(resul[1][7],2)))
         st.write("El mínimo de lluvia caída para el año seleccionado es de: ",str(round(resul[1][3],2)))
         st.write("El 25% de los días lluviosos para el año seleccionado ha llovido un valor por debajo de: ",str(round(resul[1][4],2)))
         st.write("El 50% de los días lluviosos para el año seleccionado ha llovido un valor por debajo de: ",str(round(resul[1][5],2)))
         st.write("El 75% de los días lluviosos para el año seleccionado ha llovido un valor por debajo de: ",str(round(resul[1][6],2)))
         st.divider()
         st.markdown("#### Dias de lluvia, total de lluvia y media de lluvia por mes ####")
         st.dataframe(resul[2],hide_index=True, use_container_width=True)


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
   tab1,tab2 =st.tabs(["Gráfico","Datos por año"])

   with tab1:
      col1, col2, col3,col4,col5 = st.columns(5)
      with col1:
         d1 = st.date_input("Elegir primera fecha", datetime.date(2021, 3, 15),format="DD-MM-YYYY")
         temp1 = st.number_input("temperatura baja",min_value=20,max_value=37,value=22)

      with col3:

         b1 =st.button("Ver gráfica")
      
      with col5:
         d2 = st.date_input("Elegir segunda fecha", datetime.date(2021, 10, 20),format="DD-MM-YYYY")
         temp2 = st.number_input("temperatura alta",min_value=22,max_value=45, value=37)
      
      
      st.divider()
      if b1:
         result5 = gra.temp_maxima(datos,d1,d2,temp1,temp2)
         st.plotly_chart(result5[0])
         st.write("El número de días con temperatura máxima entre {} y {} grados es de {}".format(temp1,temp2,result5[1]))
      st.divider()
      with st.popover("Ver el significado del gráfico"):
         st.markdown("""
            :red[NOTA: ] :balck[En este gráfico se muestra para los días comprendidos entre las dos fechas seleccionadas, las temperaturas máximas
                     de la zona, resaltando en color verde aquellos casos en los que la temperatura máxima esté entre los dos
                     datos de temperatura seleccionados]              
                     """)
      
      with tab2:
         col1, col2, col3,col4,col5 = st.columns(5)
         with col1:
            d11 = st.date_input("Elegir primera fecha", datetime.date(2021, 3, 16),format="DD-MM-YYYY")
            temp11 = st.number_input("temperatura baja",min_value=20,max_value=37,value=21)

         with col3:

            b11 =st.button("Ver resultados")
         
         with col5:
            d22 = st.date_input("Elegir segunda fecha", datetime.date(2021, 10, 21),format="DD-MM-YYYY")
            temp22 = st.number_input("temperatura alta",min_value=22,max_value=45, value=36)
         
         
         st.divider()         

         
         if b11:
            #st.write("Procesando la información ....")
            resultado = dat.temp_maxima(datos,d11,d22,temp11,temp22)
            lista_anios = list(resultado[0].keys())
            lista_dias =[]
            lista_porcen =[]
            for h in list(resultado[0].keys()):
               lista_dias.append(resultado[0][h])
               lista_porcen.append(round((resultado[0][h]/resultado[1][h])*100,2))
            resultado_final =pd.DataFrame({"Años":lista_anios,"Dias filtrados":lista_dias,"Porcentaje":lista_porcen})
            st.dataframe(resultado_final,hide_index=True, use_container_width=True)
            
            st.divider()
            col1,col2 = st.columns(2)
            with col1:
               with st.popover("Ver resumen estadístico por año natural",use_container_width = False):
                  anios =resultado[2].keys()
                  media = []
                  sd = []
                  minima = []
                  q1 = []
                  q2 = []
                  q3 = []
                  maxima = []
                  for h in list(resultado[2].keys()):
                     media.append(resultado[2][h][1])
                     sd.append(resultado[2][h][2])
                     minima.append(resultado[2][h][3])
                     q1.append(resultado[2][h][4])
                     q2.append(resultado[2][h][5])
                     q3.append(resultado[2][h][6])
                     maxima.append(resultado[2][h][7])

                  st.subheader("Resumen  de las temperaturas máximas por año")
                  res = pd.DataFrame({"Año":anios,"T.media":media,"T.mínima":minima,"T.máxima":maxima,"Desviaciones":sd,
                                    "25%":q1,"50%":q2,"75%":q3})
                  st.dataframe(res,hide_index=True, use_container_width=True)  
                  st.markdown("**Significado de las columnas**") 
                  st.markdown("**T.media**: Temperatura media de las temperaturas altas de todo el año") 
                  st.markdown("**T.mínima**: Temperatura mínima de todas las temperaturas altas de todo el año") 
                  st.markdown("**T.máxima**: Temperatura máxima registrada en todo el año")  
                  st.markdown("**Desviaciones**: Desviaciones de las temperaturas máximas respecto de su media") 
                  st.markdown("**25%**: Precentil 25, es decir por debajo de ese valor está el 25% de las temperaturas máximas registradas en ese año")
                  st.markdown("**50%**: Precentil 50, es decir por debajo de ese valor está el 50% de las temperaturas máximas registradas en ese año") 
                  st.markdown("**75%**: Precentil 75, es decir por debajo de ese valor está el 75% de las temperaturas máximas registradas en ese año")   
            with col2:
               with st.popover("Ver resumen estadístico entre fechas elegidas",use_container_width = False): 
                  anios2 =resultado[3].keys()
                  media2 = []
                  sd2 = []
                  minima2 = []
                  q1_2 = []
                  q2_2 = []
                  q3_2 = []
                  maxima2 = []
                  for h in list(resultado[3].keys()):
                     media2.append(resultado[3][h][1])
                     sd2.append(resultado[3][h][2])
                     minima2.append(resultado[3][h][3])
                     q1_2.append(resultado[3][h][4])
                     q2_2.append(resultado[3][h][5])
                     q3_2.append(resultado[3][h][6])
                     maxima2.append(resultado[3][h][7])

                  st.subheader("Resumen  de las temperaturas máximas por año entre las fechas elegidas")
                  res2 = pd.DataFrame({"Año":anios2,"T.media":media2,"T.mínima":minima2,"T.máxima":maxima2,"Desviaciones":sd2,
                                    "25%":q1_2,"50%":q2_2,"75%":q3_2})
                  st.dataframe(res2,hide_index=True, use_container_width=True)  
                  st.markdown("**Significado de las columnas**") 
                  st.markdown("**T.media**: Temperatura media de las temperaturas altas de todo el año") 
                  st.markdown("**T.mínima**: Temperatura mínima de todas las temperaturas altas de todo el año") 
                  st.markdown("**T.máxima**: Temperatura máxima registrada en todo el año")  
                  st.markdown("**Desviaciones**: Desviaciones de las temperaturas máximas respecto de su media") 
                  st.markdown("**25%**: Precentil 25, es decir por debajo de ese valor está el 25% de las temperaturas máximas registradas en ese año")
                  st.markdown("**50%**: Precentil 50, es decir por debajo de ese valor está el 50% de las temperaturas máximas registradas en ese año") 
                  st.markdown("**75%**: Precentil 75, es decir por debajo de ese valor está el 75% de las temperaturas máximas registradas en ese año")  


         st.divider()
         st.markdown("""
         :red[NOTA: ] :balck[En esta página se muestran los días que verifican las condiciones seleccionadas en la parte superior. Para cada 
                     año se han elegido los días comprendidos entre las dos fechas seleccionadas en la parte superior)]              
                  """)


   
elif selected3 == "Temporada invierno":
   tab1,tab2 =st.tabs(["Gráfico","Datos por temporada"])

   with tab1:
      col1, col2, col3 = st.columns(3)
      with col1:
         d1 = st.date_input("Elegir primera fecha", datetime.date(2020, 11, 1),format="DD-MM-YYYY")
         d2 = st.date_input("Elegir segunda fecha", datetime.date(2021, 3, 30),format="DD-MM-YYYY")
      with col2:
         t1 = st.number_input("Desde temperatura: ",min_value=-15,max_value=5,value=-1)
         t2 = st.number_input("Hasta temperatura: ",min_value=-15,max_value=5,value=1)
      with col3:
         dias = st.number_input("Número de días seguidos: ",min_value=2,max_value=6,value=3)
         boton = st.button("Ver gráfica")
      st.divider()
      if boton:
         result6 = gra.dias_seguidos(datos,d1,d2,t1,t2,dias)
         st.plotly_chart(result6[0])
         st.write("El número total de días con las condiciones indicadas es de {}. Los días concretos son los siguientes:".format(len(result6[1])))

         texto = ''
         for h in range(len(result6[1])):
            texto += result6[1][h]+"; "

         st.write(texto)

      st.divider()
      with st.popover("Ver el significado del gráfico"):
         st.markdown("""
            :red[NOTA: ] :balck[En este gráfico se muestran los días seguidos que hay con unas temperaturas mínimas comprendidas entre 
                     las dos temperaturas indicadas en la parte superior, para unas fechas comprendidas entre las seleccionadas en el 
                     panel superior. El número de días seguidos, también se seleccionan en el panel superior. Los días que cumplen
                     las condiciones indicadas se marcan con un color rojo]              
                     """)
   
   with tab2:
      col1, col2, col3 = st.columns(3)
      with col1:
         d11 = st.date_input("Elegir primera fecha", datetime.date(2011, 11, 1),format="DD-MM-YYYY")
         d22 = st.date_input("Elegir segunda fecha", datetime.date(2012, 3, 30),format="DD-MM-YYYY")
      with col2:
         t11 = st.number_input("Desde temperatura: ",min_value=-16,max_value=5,value=-1)
         t22 = st.number_input("Hasta temperatura: ",min_value=-15,max_value=6,value=1)
      with col3:
         dias22 = st.number_input("Número de días seguidos: ",min_value=2,max_value=7,value=3)
         boton2 = st.button("Ver datos")

      st.divider()
      if boton2:
         resultado = dat.dias_seguidos(datos,d11,d22,t11,t22,dias22)
         #pongo en listas los resultados
         temporada = list(resultado[0].keys())
         n_dias = []
         porcen = []
         for h in list(resultado[0].keys()):
            n_dias.append(len(resultado[0][h]))
            po = round((len(resultado[0][h])/resultado[1][h])*100,2)
            porcen.append(po)
         resultado_final =pd.DataFrame({"Temporada":temporada,"Número de días":n_dias,"Porcentaje":porcen})
         st.dataframe(resultado_final,hide_index=True, use_container_width=True)

         col1,col2 =st.columns(2)
         with col1:
            with st.popover("Ver resultados detallados"):
               
               for h in list(resultado[0].keys()):
                  st.write("Temporada: {}. Total días:{}".format(h,len(resultado[0][h])))
                  st.write( "".join(resultado[0][h]))
         with col2:
            with st.popover("Resumen estadístico por temporadas"):
               st.subheader("Resumen  de las temperaturas mínimas por temporadas")
               st.write("relativo sólo a los días seleccionados")
               anios =resultado[2].keys()
               media = []
               sd = []
               minima = []
               q1 = []
               q2 = []
               q3 = []
               maxima = []
               for h in list(resultado[2].keys()):
                  media.append(resultado[2][h][1])
                  sd.append(resultado[2][h][2])
                  minima.append(resultado[2][h][3])
                  q1.append(resultado[2][h][4])
                  q2.append(resultado[2][h][5])
                  q3.append(resultado[2][h][6])
                  maxima.append(resultado[2][h][7])

               
               res = pd.DataFrame({"Temporada":anios,"T.media":media,"T.mínima":minima,"T.máxima":maxima,"Desviaciones":sd,
                                 "25%":q1,"50%":q2,"75%":q3})
               st.dataframe(res,hide_index=True, use_container_width=True)  
               st.markdown("**Significado de las columnas**") 
               st.markdown("**T.media**: Temperatura media de las temperaturas altas de todo el año") 
               st.markdown("**T.mínima**: Temperatura mínima de todas las temperaturas altas de todo el año") 
               st.markdown("**T.máxima**: Temperatura máxima registrada en todo el año")  
               st.markdown("**Desviaciones**: Desviaciones de las temperaturas máximas respecto de su media") 
               st.markdown("**25%**: Precentil 25, es decir por debajo de ese valor está el 25% de las temperaturas máximas registradas en ese año")
               st.markdown("**50%**: Precentil 50, es decir por debajo de ese valor está el 50% de las temperaturas máximas registradas en ese año") 
               st.markdown("**75%**: Precentil 75, es decir por debajo de ese valor está el 75% de las temperaturas máximas registradas en ese año") 
            
      st.divider()
      st.markdown("""
         :red[NOTA: ] :balck[En este apartado tienes información del número de días de cada temporada invernal que cumple con las restricciones que se 
                  han marcado en la parte superior]              
                  """)
      
elif selected3 == "Predicción densidad":
   if 'clicked1' not in st.session_state:
      st.session_state.clicked1 = False
   if 'clicked2' not in st.session_state:
      st.session_state.clicked2 = False
   def click_1():
      st.session_state.clicked1 = True
   def click_2():
      st.session_state.clicked2 = True

   st.subheader("Cálculo de la densidad de la Paulonia")
   st.write("Aquí podemos calcular el valor de la densidad de la Paulonia en base a los resultados del estudio hecho en Navarrés por Nick Merriman, Anders Taeroe, and Karsten Raulund-Rasmussen")
   
   diametro = st.number_input("Introduce el valor del diámetro (DBH, en centímetros)",min_value=0.20, value=4.0)
   densidad = 234.8+ 2.2959*diametro
   col1, col2, col3 = st.columns(3)
   with col2:
      calcular = st.button("Calcular el valor de la densidad ", on_click=click_1)
      
   if st.session_state.clicked1:
      st.write("El valor de la densidad  es {} Kg/m^3, para un diámetro de {} cm".format(round(densidad,2),round(diametro,2)))
      st.session_state.clicked1 = False
      
   st.divider()
   st.subheader("Predicción densidad futura de Paulonia. ")
   st.write("Se obtienen la estimación del incremento del diámetro de Paulonia fortunei y de Paulonia elongata según el número de años \
            a tener en cuenta.")
   n_anios = st.number_input("Introduce el número de años: ",min_value=1,value=1)
   n_anios2 = 1996+n_anios
   idpf = -399778+402.947*n_anios2-0.1015*n_anios2**2
   # Multiplicamos por -1 para cambiar los signos de la ecuación pues de la otra manera no tiene mucho sentido
   idpe = -0.1*(1.56569-1558.75*n_anios+0.3879*n_anios**2)
   col1, col2, col3 = st.columns(3)
   with col2:
      calcular_2 = st.button("Calcular el valor incremento diámetro", on_click=click_2)
   if st.session_state.clicked2:
      st.write("El incremento del diámetro para Paulonia fortunei es {}, y para Paulonia elongata es {}".format(round(idpf,3),round(idpe,3)))
      st.session_state.clicked2 = False