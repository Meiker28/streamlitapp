import streamlit as st
import numpy as np
import pandas as pd
#import requests
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go
import markdown
import plotly.express as px
import base64
#import Path
IMAGE = "images/basketball.jpg"

#md = markdown.Markdown()

GITHUB_ROOT = (
    "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-streamlit/master/"
    "gallery/nba_roster_turnover/"
)

IMAGE_GITHUB = GITHUB_ROOT + "images/basketball.jpg"

IMAGE = "images/basketball.jpg"

@st.cache
def get_image():
    response = requests.get(IMAGE_GITHUB)
    return Image.open(BytesIO(response.content))

@st.cache
def load_images(name):
    img = Image.open(name)
    return img

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1000px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

st.title("""
 Financial Risk Analizer
""")

st.subheader('Alumnos')
#st.write("""
# Revenue Managment
#""")
#df = pd.DataFrame({'id_cod':['20150232','20160893','20190506'],'pred':[20,30,10]})

image = load_images('university.jpg')
st.sidebar.image(image, use_column_width=True)
#st.sidebar.markdown(
#    "Explore NBA roster turnover since\nthe 2003-04 season. **Roster turnover** is \ndefined as the "
#    "sum of the difference\nin total minutes played by each player\non a given team between any two "
#    "years."
#)

st.sidebar.markdown(
    "En la **Educación Superior**, existen tres grandes líneas de aplicación de la **Inteligencia Artificial**"
    " en las que veremos grandes cambios que conformarán el nuevo modelo educativo."
)


page = st.sidebar.selectbox("Nuestras Soluciones", ["Admission Optmizer", "Financial Risk Analizer","Student retention"])
df = pd.read_csv('Prediccsiones.csv')


df.DBECA_ESTADO.fillna('SIN BECA',inplace=True)
df.EE_TIPO.fillna('Otros',inplace=True)
df.DCAT_PAGO.fillna('CATEGORIA A',inplace=True)
df.RIESGO_INASISTENCIA.fillna('SIN RIESGO',inplace=True)
df.RECORDSEGMENTO.fillna('MEDIA INFERIOR',inplace=True)
#df.shape

#df.columns
df['DESERCIÓN'] = np.random.uniform(size=23745)

t1  = df.groupby('DMODALIDADINGRESO').agg({'PDESCUENTO_CUOTA':'mean','DESERCIÓN':'mean'}).reset_index()



fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>MODALIDAD DE INGRESO</b>','<b>CUOTA DE DESCUENTO</b>',
                          '<b>PROM PROB DESERCIÓN </b>'],
                fill_color='royalblue',
                align='left',
                font=dict(color='white', size=12)),
    cells=dict(values=[t1.DMODALIDADINGRESO, t1.PDESCUENTO_CUOTA, t1.DESERCIÓN],
               fill_color='lavender',
               align='left',
                font = dict(color = 'darkslategray', size = 11)))
])




def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

with open("prediction.jpg", "rb") as image_file:
    data = base64.b64encode(image_file.read()).decode()

d1 =df[(df.PREDICHO>5) & (df.PREDICHO<=20) ]
if page == "Homepage":
    st.header("This is your data explorer.")
    st.write("Please select a page on the left.")
    st.dataframe(d1)

elif page == "Financial Risk Analizer":

    type = st.sidebar.radio("Tipo",('Exploración de datos','Predicción'))

    if type =='Exploración de datos':
        st.write(fig)

        st.subheader('Explore the original data')
        xvar = st.selectbox('Seleciona el eje-x:', ['PDESCUENTO_CUOTA','MONTO_MAT','MONTO_CUOTA','COLEGIO_PENSION'])
        yvar = st.selectbox('Seleciona el eje-y:', ['PDESCUENTO_MAT','MONTO_MAT','MONTO_CUOTA','COLEGIO_PENSION'])
        cat = st.selectbox('Seleciona la categoria:', ['DMODALIDADINGRESO','RIESGO_INASISTENCIA','DBECA_ESTADO'])
        st.write(px.scatter(df ,x=xvar, y=yvar,  color=cat))


    #st.title("Predicción")
    elif type =='Predicción':
        st.markdown("<center> <h1> Predicción de Descuentos</h1></center>",unsafe_allow_html=True)
        img = load_images('prediction.jpg')
        #encoded_string = base64.b64encode(image_file.read())
        #"<center>"+md.convert(top_results_markdown)+"</center>"
        #st.markdown("<center>"+md.convert("<img src='/home/meiker/web_app/project/university.jpg' width='850' height='200'/>") +"</center>",unsafe_allow_html=True)
        st.image(img,use_column_width=True)
        #st.markdown(f"<center>"+"<p> <img src={} width='850' height='200' />"+"</center> </p>",unsafe_allow_html=True)
        #header_html =  "<img src='data:image/png;base64,{}'   height='500' width='400' class='img-fluid' />".format(data)
        #st.markdown("<center>"+header_html+"</center>", unsafe_allow_html=True)

        Edad = st.number_input('Edad', min_value=1, max_value=100, value=20)

        Ciclo = st.slider('Ciclo', min_value=1, max_value=10, value=1)
        sex = st.selectbox('Mérito General', ['Décimo Superior', 'Quinto Superior','Tercio Superior','Otros'])
        sit_laboral = st.radio('Situación Laboral',('Sí','No'))


        cod_alumno= st.selectbox('Ingrese Código de Alumno',d1.CALUMNO.unique())
        new_df = d1.loc[d1.CALUMNO ==cod_alumno,['PREDICHO']].values
        if st.button('Predecir'):
            st.success("El porcentaje de descuento del alumno es:  {}%".format(int(new_df)))






#df.FLAG_SITUACIONLAB.value_counts().index.tolist()
#df.EE_TIPO.value_counts()








#cod_alumno= st.sidebar.multiselect('Ingrese Código de Alumno',d1.CALUMNO.tolist())




#st.write(d1)

#st.subheader('Predicción de descuentos de alumnos')

#cod_alumno= st.multiselect('Ingrese Código de Alumno',d1.CALUMNO.tolist())
#new_df = d1.loc[d1.CALUMNO.isin(cod_alumno),['PREDICHO']].values


#st.write('El descuento de la matricula es:' new_df)
