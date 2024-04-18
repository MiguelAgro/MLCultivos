import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



def temperaturas(df):
    fig = go.Figure()
    trace1= px.line(df, x='fecha', y="temp_min")

    trace2 = px.line(df, x='fecha', y="temp_max")
    trace2.update_traces(line_color='red')

    fig.add_trace(trace1.data[0])
    fig.add_trace(trace2.data[0])
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        title=dict(text="Temperaturas máxima y mínima \n", font=dict(size=25), automargin=True, yref='paper')
    )

    return fig

def precipitaciones(df):
    
    fig = px.bar(df, x='fecha', y='precipitacion')
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_traces(marker_color='red', marker_line_color='rgb(8,48,107)')
    
    return fig

def temp_medias(df):
    df3 = df[['year_fecha', 'month_fecha','temp_min']]
    df3=(df3.groupby(by=["year_fecha","month_fecha"])['temp_min']).mean().to_frame(name="minima")
    df3.reset_index()
    df3 = (df3.pivot_table(index=['month_fecha'], columns='year_fecha',
                         values='minima')
             .reset_index()
          )
    
    fig = px.parallel_coordinates(df3, color="month_fecha",
                              dimensions=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021],
                              labels={'month_fecha':'Mes'},range_color=[0.5, 11.5],
                             color_continuous_scale=[(0.00, "red"),   (0.09, "red"),
                                                     (0.09, "green"), (0.18, "green"),
                                                     (0.18, "blue"),  (0.27, "blue"),
                                                      (0.27, "chocolate"),(0.36,"chocolate"),
                                                     (0.36,"crimson"),(0.45,"crimson"),
                                                     (0.45,"gold"),(0.54,"gold"),
                                                     (0.54,"deeppink"),(0.63,"deeppink"),
                                                     (0.63,"magenta"),(0.72,"magenta"),
                                                     (0.72,"peru"),(0.81,"peru"),
                                                     (0.81,"yellow"),(0.9,"yellow"),
                                                     (0.9,"black"),(1.00,"black")
                              ],
                              
                             )

    fig.update_layout(coloraxis_colorbar=dict(
        tickvals=[1,2,3,4,5,6,7,8,9,10,11],
        ticktext=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre"],
        lenmode="pixels", len=400),
                    title=dict(text='Temperatura media mínima de cada mes por año',automargin=True))
    
    return fig

def boxplot(dat, mes):
    # función para sacar el box plot de un determinado mes
    df_mes = dat.loc[dat.month_fecha==mes][['year_fecha','temp_min']]
    fig = px.box(df_mes, x='year_fecha',y='temp_min')
    fig.update_layout(
        xaxis_title='Año de observación',
        yaxis_title="Temperatura mínima"
    )
    return fig

def mes_minima(dat, mes):
    # Saco para un determinado mes y para cada día las temperaturas mínimas observadas y luego lo represento
    df_mes = dat.loc[dat.month_fecha==mes][['year_fecha','day_fecha','temp_min']]
    df_mes = pd.pivot_table(df_mes, values='temp_min', index=['day_fecha'],columns=['year_fecha'],aggfunc='sum')
    df_mes['dia'] = df_mes.index
    fig = px.line(df_mes, x="dia", y=df_mes.columns,
              #hover_data={"date": "|%B %d, %Y"},
              title='Temperaturas mínimas observadas, en el mes seleccionado').update_traces(visible='legendonly',
                                                                                             selector=lambda t: not t.name in ["2012","2021"])
    fig.update_layout(
        xaxis_title="día del mes",
        yaxis_title="Temperatura mínima"
    )
    
    return fig