<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h1 align=center> **Tomas Fernandez - TFTomasFernandez** </h1>
# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>


¡Bienvenidos a mi primer proyecto individual! 

<hr>  

## Mi Rol como desarrollador

Trabajamos como **`Data Scientist`** en una start-up que provee servicios de agregación de plataformas de streaming. Necesito crear mi primer modelo de ML que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha! 

Tuve que empezar desde 0, haciendo un trabajo rápido de **`Data Engineer`** y tener un **`MVP`** (_Minimum Viable Product_) para las próximas semanas!,

<p align="center">
<img src="https://github.com/HX-PRomero/PI_ML_OPS/raw/main/src/DiagramaConceptualDelFlujoDeProcesos.png"  height=500>
</p>

<sub> Nota: Aqui se reflejan procesos no herramientas tecnologicas.<sub/>

## **Estas son las propuesta de trabajo que tuve que resolver**

**`Transformaciones`**:  Para este MVP no necesitas perfección, ¡necesitas rapidez! ⏩ Vas a hacer estas, ***y solo estas***, transformaciones a los datos:


+ Algunos campos, como **`belongs_to_collection`**, **`production_companies`** y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder  y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

+ Los valores nulos de los campos **`revenue`**, **`budget`** deben ser rellenados por el número **`0`**.
  
+ Los valores nulos del campo **`release date`** deben eliminarse.

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**, además deberán crear la columna **`release_year`** donde extraerán el año de la fecha de estreno.

+ Crear la columna con el retorno de inversión, llamada **`return`** con los campos **`revenue`** y **`budget`**, dividiendo estas dos últimas **`revenue / budget`**, cuando no hay datos disponibles para calcularlo, deberá tomar el valor **`0`**.

+ Eliminar las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.

<br/>

**`Desarrollo API`**:   Propones disponibilizar los datos de la empresa usando el framework ***FastAPI***. Las consultas que propones son las siguientes:

Deben crear 6 funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).
  
+ def **cantidad_filmaciones_mes( *`Mes`* )**:
    Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

         
+ def **cantidad_filmaciones_dia( *`Dia`* )**:
    Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.


+ def **score_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
    

+ def **votos_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
    

+ def **get_actor( *`nombre_actor`* )**:
    Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. **La definición no deberá considerar directores.**
    

+ def **get_director( *`nombre_director`* )**:
    Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.



<br/>


**`Deployment`**: Utilizar [Render](https://render.com/docs/free#free-web-services), o cualquier otro servicio que permita que la API pueda ser consumida desde la web.

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior. Las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos, ¡podría ayudar al sistema de recomendación! Sabes que puedes apoyarte en librerías como _pandas profiling, missingno, sweetviz, autoviz_, entre otros y sacar de allí tus conclusiones 😉

**`Sistema de recomendación`**: 

Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación de películas. El EDA debería incluir gráficas interesantes para extraer datos, como por ejemplo una nube de palabras con las palabras más frecuentes en los títulos de las películas. Éste consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán según el score de similaridad y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente. Debe ser deployado como una función adicional de la API anterior y debe llamarse:


+ def **recomendacion( *`titulo`* )**:
    Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

<br/>

## 1. Transformación de Datos

1. Se inició con los archivos `movies_dataset.csv` y `credits.csv` que contenían información sobre películas y créditos asociados.
2. Se realizó una exploración inicial de los datos para comprender su estructura y contenido.
3. Se identificaron los problemas de calidad de los datos, como valores faltantes, duplicados o inconsistencias.
4. Se procedió a realizar la normalización de los datos para facilitar su procesamiento y análisis a través de archivo main.ipynb:
    ### En el caso del archivo `movies_data.csv`, se realizaron las transformaciones y se exportó a peliculas.csv:
- [Archivo peliculas](https://github.com/TFTomasFernandez/Proyecto_1/tree/Repositorio/Datasets%20utilizados)
    ### En el caso del archivo `credits.csv`, se realizaron las transformaciones con la clase DataGuru2 y se exportó a df_credits_norm.csv:
- [Archivos creditos cast y crew](https://github.com/TFTomasFernandez/Proyecto_1/tree/Repositorio/Datasets%20utilizados)

## 2. Análisis exploratorio de los datos y sistema de recomendación

El análisis exploratorio de datos realizado consistió en el procesamiento y exploración de los conjuntos de datos "movies_data.csv" y "credits.csv" para obtener información relevante sobre las películas.

### Respecto a la consulta para recomendar peliculas, se desarollo de la siguiente manera:

1. El título de la película de entrada se convirtió a minúsculas para evitar problemas de coincidencia de mayúsculas y minúsculas.

2. Se creó una nueva columna en el DataFrame df_movies_norm que contiene los títulos en minúsculas.

3. El DataFrame se filtró para obtener la película de entrada específica.

4. Se verificó si se encontró la película de entrada en el conjunto de datos.

5. Se procedió a obtener los géneros de la película de entrada.

6. El DataFrame se filtró nuevamente para encontrar películas que tuvieran al menos uno de los géneros de la película de entrada. La película de entrada se excluyó del conjunto filtrado.

7. Las películas resultantes se ordenaron en base a su puntuación y popularidad, de forma descendente.

8. Se seleccionaron las 5 primeras películas como recomendaciones.

9. Se creó una lista de diccionarios que almacenaban la información relevante de cada película recomendada, como el título, la fecha de lanzamiento, la puntuación y la popularidad.

10. Se devolvió un diccionario que contenía el título de la película de entrada y la lista de películas recomendadas.

11. En caso de no encontrarse ninguna película con el título de entrada, se devolvió un mensaje indicando que no se encontró ninguna coincidencia en el conjunto de datos.

En resumen, este método proporciona una funcionalidad para recomendar películas similares basándose en los géneros de una película de entrada específica.

## 3. Desarrollo de la API con FastAPI
1. Se utilizó el framework FastAPI para desarrollar una API que permitiera acceder a los datos normalizados.
2. Se crearon las rutas y controladores correspondientes para manejar las solicitudes de los usuarios.
3. Se implementaron las operaciones básicas de consulta y búsqueda de películas, así como también la obtención de información detallada de una película específica.
4. Se realizaron pruebas locales para asegurarse de que la API funcionara correctamente.

## 4. Despliegue del Proyecto en Render

1. Se configuró el entorno de despliegue utilizando Render, un servicio de alojamiento y despliegue de aplicaciones web
2. Se creó un archivo de configuración `requirements.txt` con las dependencias necesarias para el proyecto.
4. Se realizó el despliegue del proyecto en Render, asegurando que la API estuviera disponible en línea.



**`Video`**: Necesitas que al equipo le quede claro que tus herramientas funcionan realmente! Haces un video mostrando el resultado de las consultas propuestas y de tu modelo de ML entrenado!

<sub> **Spoiler**: El video NO DEBE durar mas de ***7 minutos*** y DEBE mostrar las consultas requeridas en funcionamiento desde la API y una breve explicacion del modelo utilizado para el sistema de recomendacion. En caso de que te sobre tiempo luego de grabarlo, puedes mostrar explicar tu EDA, ETL e incluso cómo desarrollaste la API. <sub/>

<br/>

## **Fuente de datos**

- + [Dataset](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5?usp=drive_link): Carpeta con los 2 archivos con datos que requieren ser procesados (movies_dataset.csv y credits.csv), tengan en cuenta que hay datos que estan anidados (un diccionario o una lista como valores en la fila).
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>
