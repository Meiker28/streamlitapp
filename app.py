import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

#image = Image.open('IVFey8Tz_400x400.jpg')

df = pd.read_csv('process_lead.csv')
out = df[df.lead>100]

out.sort_values(by='lead',ascending=False)
df = df[df.lead<=100]
#df.head()
df.head()
dt= df.groupby(['marca','modelo']).sum().reset_index()[['marca','modelo']]
marca_  = df.marca.value_counts().index.tolist()

def cambio(df):
    df['Ganancia'] = round(df.lead/df.iloc[0].lead,1).astype(str) + 'x'
    return df

st.title("Recomendación de Avisos")

menu = ['App','Análisis de Leads','Avisos Atípicos']
choices = st.sidebar.selectbox('Seleccionar',menu)

if choices == 'App':
    st.image(image,use_column_width=True,clamp = True)

    #st.subheader('EDA')
    marca_mod = df.groupby(['marca','modelo','nombretipopublicacion']).lead.median().reset_index()
    marca = st.selectbox('Marca', marca_)

    mdl= dt[dt.marca==marca].modelo.value_counts().sort_index().index.tolist()
    modelo = st.selectbox('Modelo', mdl)

    tr = marca_mod[marca_mod.modelo==modelo].sort_values('lead')
    tr = cambio(tr).reset_index(drop=True)
    st.table ( tr)

    st.write(px.bar(tr ,x='nombretipopublicacion', y='lead',  color='nombretipopublicacion'))

if choices == 'Análisis de Leads':

    st.subheader('Análisis de Leads')
    #st.subheader('Explore the original data')

    xvar = st.selectbox('Seleciona el eje-x:', ['precio','lead','kilometraje'])
    yvar = st.selectbox('Seleciona el eje-y:', ['kilometraje','lead','precio'])
    cat = st.selectbox('Seleciona la categoria:', ['nombretipopublicacion','marca','modelo'])

    st.write(px.scatter(df ,x=xvar, y=yvar,  color=cat,width=850, height=600,title="Distribución por tipo de publicación"))

    marca_mod = df.groupby(['marca','modelo','nombretipopublicacion']).lead.median().reset_index()
    publicacion = st.selectbox('Seleciona tipo de publicación:', ['GRATUITO','SIMPLE','DESTACADO','PLUS','PREMIUM'])
    st.write(px.bar(marca_mod[marca_mod.nombretipopublicacion==publicacion].sort_values('lead',ascending=False)[0:15] ,
    x='modelo', y='lead',  color='nombretipopublicacion',width=850, height=600,title="Modelos de vehículo con mayor Lead"))


    marca = st.selectbox('Marca', marca_)

    mdl= dt[dt.marca==marca].modelo.value_counts().sort_index().index.tolist()
    modelo = st.selectbox('Modelo', mdl)

    st.write(px.box(df[df.modelo==modelo] ,x='nombretipopublicacion', y='lead',
    color='nombretipopublicacion',width=850, height=600,points='all',title="Distribución de Leads por tipo de publicación "))

sm = out[['idaviso','marca','modelo','precio','kilometraje','lead']].sort_values('lead',ascending=False).head(5).reset_index(drop=True)
precio_mercado = [12500,15200,24650,19250,12000]
sm['precio mercado'] = precio_mercado

if choices == 'Avisos Atípicos':
    st.subheader('Avisos Atípicos')

    xvar = st.selectbox('Seleciona el eje-x:', ['precio','lead','kilometraje'])
    yvar = st.selectbox('Seleciona el eje-y:', ['kilometraje','lead','precio'])
    cat = st.selectbox('Seleciona la categoria:', ['nombretipopublicacion','marca','modelo'])

    st.write(px.scatter(out ,x=xvar, y=yvar,  color=cat,width=850, height=600,title="Distribución por tipo de publicación"))
    st.table ( sm)
