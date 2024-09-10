import streamlit as st
import pandas as pd


def tablas(datos):
    datos['fecha'] = datos['fecha'].dt.date
    datos = datos[['fecha','nombre_estacion_off','altitud','temp_media','precipitacion','temp_min','horatmin',
                   'temp_max','horatmax','direccion','racha','horaracha','label']]
    
    col1,col2 = st.columns(2, gap='large')
    with col1:
        minima = st.number_input('Elegir la temperatura máxima para filtrar la tabla', value=2)

    with col2:
        adelante = st.button('Mostrar resultados')

    st.divider()

    if adelante:
        datos2 =datos.loc[datos.temp_min <= minima]
        st.dataframe(data=datos2, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("""
    :red[NOTA: ] :balck[En este apartado se muestra una tabla, donde se pueden ver los registros resultantes si filtramos por una determinada temperatura que se indica
                en la parte superior, poniendo en esta parte determinado valor y haciendo click en el botón, se muestran los registros de los datos con una temperatura
                mínima menor o igual que que la indicada en la zona superior ]
    """)

# Función para detectar último día de helada hasta un dia y mes
def ultima_helada(datos, dia, mes):
    # selecciono lo datos anteriores a ese mes-dia
    df_mes_dia = datos.loc[((datos.day_fecha<=dia) & (datos.month_fecha==mes)) | (datos.month_fecha<mes)]
    resul = pd.DataFrame(columns=['anio','fecha','Temperatura'])
    anios = datos.year_fecha.unique()
    for anio in anios:
        sel = df_mes_dia.loc[(df_mes_dia.year_fecha== anio) & (df_mes_dia.heladas==1)]
        fe = sel.iloc[-1][['fecha','temp_min']]
        resul2 = pd.DataFrame({'anio':[anio],'fecha':[fe.fecha.strftime("%d-%m-%Y")],'Temperatura':[fe.temp_min]})
        resul= pd.concat([resul,resul2])
    #incluyo esto para eliminar el index en la salida de la tabla
    hide_streamlit_style = """
            <style>
            tbody th {display:none}
            .blank{
            display: none;
            }
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)   
    st.table(resul)
    
    st.divider()
    st.markdown("""
    :red[NOTA: ] :balck[En este apartado se van a obtener para cada año el último día que ha helado anterior al día y mes que se indica en el apartado de introducción de datos ]
""")
    
def temp_maxima(datos,d1,d2,temp1,temp2):
    """
    Con esta función obtengo  los días de verano con una tenperatura máxima entre temp1 y temp2
    """
    # convierto la columna fecha en formato date
    datos['fecha'] = datos['fecha'].dt.date
    df2 = datos[(datos.temp_max>=temp1) & (datos.temp_max<=temp2)]
    df2 = df2.copy()
    #df2.reset_index(inplace=True)
    # Obtengo los años que hay
    anios = list(df2.year_fecha.unique())
    # creo un diccionario donde almacenar los resultados
    resul = {}
    # En este otro diccionario, almaceno los días totales que tiene la base de datos (para porcentajes)
    resul_2 = {}
    # En este otro diccionario almaceno resumen estadístico del año natural
    resul_3 = {}
    # En este otro diccionario almaceno resumen estadístico entre las fechas elegidas
    resul_4 = {}
    for anio in anios:
        dd1 = d1.replace(year=anio)
        dd2 = d2.replace(year=anio)
        df3 = df2[(df2.fecha>=dd1) & (df2.fecha<=dd2)]
        resul[anio]=len(df3)
        # obtengo los datos totales que hay para cada año
        df4 = datos[datos.year_fecha==anio]
        resul_2[anio]=len(df4)
        resul_3[anio] = df4.temp_max.describe()
        resul_4[anio] = df3.temp_max.describe()

    return resul,resul_2,resul_3,resul_4

def dias_seguidos(dat,d1,d2,temp1,temp2,ndias):
    """
    En esta función obtengo información de los días seguido (ndias) que hay para cada temporada de invierno que están entre temp1 y temp2
    """
    # convierto la columna fecha en formato date
   
    dat['fecha'] = dat['fecha'].dt.date
    
    # defino un diccionario donde almaceno el resultado
    resul= {}
    # defino al diccionario donde almaceno el número total de días para calcular el porcentaje
    resul_dias = {}
    #defino un diccionario para almacenar los resultados estadísticos para cada temporada
    resul_esta ={}

    # Saco los años que están en el dataframe
    anios = list(dat.year_fecha.unique())
    # recorro cada año
    for anio in anios:
        # defino la temporada
        temporada = str(anio)+"-"+str(anio+1)

        dia1 =  d1.replace(year=anio)  
        dia2 = d2.replace(year=anio+1)
        df2 =dat[(dat.fecha>=dia1) & (dat.fecha<=dia2)]
        df2.reset_index(inplace=True)
        df2 = df2.copy()
        # Inicializo la variable temp_4_contar que cuenta el número de días seguidos con temperatura minima entre las pasadas a la función
        df2['temp_4_contar']=0
        # recorremos ahora el dataframe y contamos lo días seguidos con temp_min entre los valores pasados a la función
        for row in df2.itertuples():
            if row.temp_min >= temp1 and row.temp_min <= temp2:
                if row.Index == 0:
                    # Si es el primer registro pongo valor=1
                    valor= 1
                else:
                    valor = df2.loc[row.Index-1,'temp_4_contar']+1
                df2.loc[row.Index,'temp_4_contar']= valor
                # si valor supera ndias, pongo el mayor valor de ndias seguidos
                if valor >= ndias:
                    for h in range(1,int(valor)):
                        df2.loc[row.Index-h,'temp_4_contar'] = valor

        #creamos una lista de fechas para incluir las que cumplen condición
        fechas=[]
        for row in df2.itertuples():
            if row.temp_4_contar>=ndias:
                #print(strftime(row.fecha,"$d-%m-%y"))
                try:
                    fechas.append(row.fecha.strftime("%d-%m-%y") + "; ")
                except:
                    print("************ Ocurrió un error:")
                    print(row)
                
        # Almacenamos en el diccionario el valor obtenido  
        resul[temporada]=fechas
        resul_dias[temporada]=len(df2)
        resul_esta[temporada] = df2.temp_min.describe()

    return resul,resul_dias,resul_esta 