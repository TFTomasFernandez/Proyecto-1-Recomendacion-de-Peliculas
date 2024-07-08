import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

df_Main = pd.read_csv('Datasets utilizados/Main.csv')
app = FastAPI()
###############################################################################################################################################################################
# Convertimos la columna 'release_date' a tipo datetime si no está en ese formato
@app.get("/Meses")
def cantidad_filmaciones_mes(mes:str):
    
    df_Main['release_date'] = pd.to_datetime(df_Main['release_date'], errors='coerce')
    
    # Filtramos películas que coincidan con el mes dado
    peliculas_en_mes = df_Main[df_Main['release_date'].dt.month_name('es').str.lower() == mes.lower()]
    
    # Eliminamos duplicados basados en la columna 'movie_title' por ejemplo, ajusta según tus datos
    peliculas_en_mes_sin_duplicados = peliculas_en_mes.drop_duplicates(subset=['title'])
    
    # Contar la cantidad de películas únicas en el mes
    cantidad = peliculas_en_mes_sin_duplicados.shape[0]
    
    resultado =  (cantidad)+ ' de películas fueron estrenadas en el mes de ' + (mes)

    return resultado


################################################################################################################################################################################
# Función para contar la cantidad de películas estrenadas en un día específico
@app.get("/Dias")
def cantidad_filmaciones_dia(dia:str=""):

#Mapeo de nombres de días en español a números de día. Se incluyen variantes sin acento ortográfico.
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5,'domingo': 6}

#Convertir el día ingresado a minúsculas y obtener su número correspondiente

    dia_numero = dias.get(dia.lower(), None)

    if dia_numero is None:
        return f"No se reconoce el día '{dia}'. Por favor, ingresa un día válido en español."

# Convertir release_date a datetime y extraer el día de la semana
    df_Main['release_date'] = pd.to_datetime(df_Main['release_date'], errors='coerce')
    df_Main['dia_semana'] = df_Main['release_date'].dt.dayofweek

#Filtrar las películas por el día especificado
    peliculas_dia = df_Main[df_Main['dia_semana'] == dia_numero]
 
# Eliminamos duplicados basados en la columna 'movie_title' por ejemplo, ajusta según tus datos
    peliculas_dia = peliculas_dia.drop_duplicates(subset=['title'])

#Obtener la cantidad de películas
    cantidad = peliculas_dia.shape[0]

#Devolver el resultado formateado
    return f"{cantidad} {'películas' if cantidad != 1 else 'película'} fueron estrenadas en los días {dia.title()}."



################################################################################################################################################################################
# Función para obtener el título, año de estreno y score de una filmación
@app.get("/Titulos")
def score_titulo(titulo):

    # Filtramos el DataFrame por el título dado
    pelicula = df_Main[df_Main['title'] == titulo]
    
    # Verificaamos si se encontró la película
    if pelicula.empty:
        return f"No se encontró información para '{titulo}'"
    
    # Obtenemos los datos de la película encontrada
    titulo = pelicula['title'].iloc[0]
    año_estreno = pelicula['release_year'].iloc[0]
    score = pelicula['popularity'].iloc[0]
    
    return "El tirulo es: " +str(titulo)+ " / El año de estreno fue: " +str(año_estreno)+ " / Y su Score fue de : " +str(score) 

################################################################################################################################################################################

# Función para obtener el título, cantidad de votos y valor promedio de votaciones
@app.get("/Votos")
def votos_titulo(titulo:str=""):
    # Filtramos el DataFrame por el título dado
    pelicula = df_Main[df_Main['title'] == titulo]
    
    # Verificamos si se encontró la película y si cumple con la condición de votos
    if pelicula.empty:
        return f"No se encontró información para '{titulo}'"
    
    if pelicula['vote_count'].iloc[0] < 2000:
        return f"La película '{titulo}' no cumple con el mínimo de 2000 valoraciones."
    
    # Obtenemos los datos de la película encontrada
    titulo = pelicula['title'].iloc[0]
    votos = pelicula['vote_count'].iloc[0]
    promedio_votos = pelicula['vote_average'].iloc[0]
    
    return "El tirulo es: " +str(titulo)+ " / Los votos que tuvo fueron: " +str(votos)+ " / Y el promedio de votos es : " +str(promedio_votos)

################################################################################################################################################################################

# Función para obtener información de un actor específico
@app.get("/Actores")
def get_actor(nombre_actor:str=""):

    # Filtramos las películas en las que ha participado el actor
    peliculas_actor = df_Main[df_Main['actores'].str.contains(nombre_actor, na=False)]
    
    # Eliminamos duplicados en 'id' para contar películas únicas
    peliculas_actor = peliculas_actor.drop_duplicates(subset=['actores'])
    
    # Unimos con el DataFrame de películas para obtener la información de retorno
    peliculas_actor = pd.merge(peliculas_actor, df_Main[['id', 'return']], on='id', how='left')
    
    # Calculamos la cantidad de películas en las que ha participado el actor (sin duplicados)
    cantidad_peliculas = peliculas_actor.shape[0]
    
    # Calculamos el éxito total (suma de retornos)
    exito_total = peliculas_actor['return'].sum()
    
    # Calculamos el promedio de retorno
    promedio_retorno = peliculas_actor['return'].mean()
    
    return 'Nombre del actor: ' +str(nombre_actor)+ '/ Cantidad de peliculas grabadas: ' +str(cantidad_peliculas)+ '/ Exito total: ' +str(exito_total)+ '/ Promedio del retorno: ' +str(promedio_retorno)

################################################################################################################################################################################
@app.get("/Directores")
def get_director(nombre_director):
    # Filtramos las películas dirigidas por el director
    peliculas_director = df_Main[df_Main['director'].str.contains(nombre_director, na=False)]
    
    # Verificamos el contenido después del filtrado
    if peliculas_director.empty:
        print(f"No se encontraron películas para el director: {nombre_director}")
        return None

    # Eliminamos duplicados en 'director' para contar películas únicas
    peliculas_director = peliculas_director.drop_duplicates(subset=['director'])

    # Verificamos el contenido después de eliminar duplicados
    print("Películas después de eliminar duplicados:", peliculas_director)

    # Unimos con el DataFrame de películas para obtener más detalles
    peliculas_director = pd.merge(peliculas_director, 
                                  df_Main[['title', 'release_date', 'return', 'budget', 'revenue', 'id']], 
                                  left_on='id', right_on='id', how='left')

    # Verificamos el contenido después de la unión
    print("Películas después de la unión:", peliculas_director)

    # Calculamos el éxito total del director (suma de retornos)
    exito_total = peliculas_director['return'].sum()

    # Preparamos la lista de detalles de cada película única
    detalles_peliculas = []
    peliculas_procesadas = set()  # Conjunto para almacenar ids de películas procesadas

    for index, pelicula in peliculas_director.iterrows():
        movie_id = pelicula['id']
        # Verificar si ya hemos procesado esta película (evitar duplicados)
        if movie_id not in peliculas_procesadas:
            detalles_peliculas.append({
                'nombre_pelicula': pelicula['title'],
                'fecha_lanzamiento': pelicula['release_date'],
                'retorno_individual': pelicula['return'],
                'costo': pelicula['budget'],
                'ganancia': pelicula['revenue']
            })
            peliculas_procesadas.add(movie_id)

    # Preparamos el mensaje final
    mensaje = (
        f"Director: {nombre_director}/"
        f"Éxito total: {exito_total}/"
        f"Películas:/"
    )

    # Imprimimos los detalles de películas de manera organizada
    for detalle in detalles_peliculas:
        mensaje += (
            f"  - {detalle['nombre_pelicula']} ({detalle['fecha_lanzamiento']}): "
            f"Retorno {detalle['retorno_individual']}, Costo {detalle['costo']}, Ganancia {detalle['ganancia']}\n"
        )

    # Imprimimos información para depuración
    print(mensaje)

    return mensaje
    
################################################################################################################################################################################
@app.get("/Recomendaciones")
def recomendar_peliculas(titulo: str):
    # Filtramos el dataset para encontrar la película dada
    pelicula_dada = df_Main[df_Main['title'] == titulo]
    
    if pelicula_dada.empty:
        return f"No se encontró la película con el título: {titulo}"
    
    # Obtenemos el género de la película dada
    genero_dado = pelicula_dada.iloc[0]['genresname']
    
    # Filtramos el dataset para encontrar películas del mismo género
    peliculas_similares = df_Main[df_Main['genresname'].str.contains(genero_dado, na=False)]
    
    # Ordenamos por popularidad predicha en orden descendente
    peliculas_ordenadas = peliculas_similares.sort_values(by='predicted_popularity', ascending=False)
    
    # Excluimos la película dada de las recomendaciones (si está en la lista)
    peliculas_ordenadas = peliculas_ordenadas[peliculas_ordenadas['title'] != titulo]
    
    # Seleccionamos los títulos de las 5 mejores películas y mantener el orden
    recomendaciones = peliculas_ordenadas.head(5)[['title', 'genresname', 'predicted_popularity']].reset_index(drop=True)
    
    # Insertamos la película dada como primera fila en las recomendaciones
    recomendaciones = pd.concat([pelicula_dada[['title', 'genresname', 'predicted_popularity']], recomendaciones]).reset_index(drop=True)
    
    # Preparamos el mensaje final
    mensaje = (f"Titulo elegido: {titulo}"
           f"Recomendaciones:"
           + "\n".join([f"{idx}. {row['title']} / Género: {row['genresname']} / Popularidad predicha: {row['predicted_popularity']}"
                        for idx, row in recomendaciones.iloc[1:].iterrows()]) )

    return mensaje


##############################################################################################################################################################################

