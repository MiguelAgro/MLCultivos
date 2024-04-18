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
