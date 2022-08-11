import json
from getpass import getpass
from decouple import config
from pymongo import MongoClient
from Cartelera import base
from ordenamientos import quick, quick_descendente, particion, particion_descendente

# Importando variables de acceso para el admin
# y usuario no privilegiado, además de las credenciales
# necesarias para la base de datos

ADMIN_USER = config('ADMIN_USER')
ADMIN_PASS = config('ADMIN_PASS')

DEFAULT_USER = config('DEFAULT_USER')
DEFAULT_PASS = config('DEFAULT_PASS')

DATABASE_USER = config('DB_USER')
DATABASE_PASS = config('DB_PASS')

client = MongoClient('mongodb+srv://{}:{}@cluster0.6fzoi.mongodb.net/?retryWrites=true&w=majority'.format(DATABASE_USER, DATABASE_PASS))
db = client.ColecciónPersonal
horario = db.Horario
admin = False

def menu():
  print('Bienvenido a cartelera. Ingrese su usuario')

def menu_admin():
  print('1. Alta película \n2. Alta horario \n3. Baja película \n4. Baja horario \n5. Modificar película \n6. Consultar película \n7. Consultar cartelera \n8. Salir')

def menu_usuario():
  print('1. Buscar película por nombre \n2. Buscar película por clasificación \n3. Buscar película por género \n4. Ordenar Cartelera (A y D) \n5. Consultar película \n6. Consultar cartelera \n7. Salir')

def get_credentials():
  usuario = input('Usuario: ')
  contra = getpass('Contraseña: ')
  return [usuario, contra];

def validate_credentials():
  auth = get_credentials()

  if (auth[0] == ADMIN_USER and auth[1] == ADMIN_PASS):
    print('Bienvenido usuario administrador')
    global admin
    admin = True

  elif (auth[0] == DEFAULT_USER and auth[1] == DEFAULT_PASS):
    print('Hola {}, bienvenido'.format(auth[0].capitalize()))
    
  else:
    print('Usuario no registrado. Intententa de nuevo')
    validate_credentials()

def display_billboard(database, municipio, asc=True, time=True): 
  print('-'*70)
  cursor = horario.find({"Municipio": {"$eq": municipio}})
  date = []
  time = []
  for result in cursor:
    tmp_date = []
    tmp_time = []
    tmp_date.append(int(result['Fecha'].replace('/', '')))
    tmp_date.append(result['_id'])
    tmp_time.append(int(result['Hora'].replace(':', '')))
    tmp_time.append(result['_id'])
    date.append(tmp_date)
    time.append(tmp_time)
    format_schedule(result)
  print(date, time)

def get_billboard():
  id_estado = input('ID ESTADO: ')
  id_municipio = input('ID MUNICIPIO: ')
  return [id_estado.upper(), id_municipio.upper()];

def validate_billboard(id_estado, id_municipio):
  isValid = False
  try :
    if (base[id_estado][id_municipio]):
      isValid = True
  except:
    print('La cartelera seleccionada no es válida')
    id_estado, id_municipio = get_billboard()
    validate_billboard(id_estado, id_municipio)

  return isValid

def new_movie(database, municipio):
  movie_info = get_movie_data()
  movie_doc = {
    "Name": movie_info[0],
    "Director": movie_info[1],
    "Producer": movie_info[2],
    "Rating": movie_info[3],
    "Running_time": movie_info[4],
    "Genre": movie_info[5],
    "Municipio": municipio
  }
  try:
    database.insert_one(movie_doc)
    print('Película registrada exitosamente')
  except:
    print('Ocurrió un error al registrar la película. Intente de nuevo')
  
def get_movie_data():
  movie_info = []
  selected_genres = []
  genres = ['Acción', 'Aventuras', 'Ciencia ficción', 'Comedia', 'Drama', 'Thriller', 'Suspenso', 'Terror', 'Romance', 'Animación']
  movie_info.append(input('Nombre: '))
  movie_info.append(input('Director: ').split(','))
  movie_info.append(input('Productor: ').split(','))
  movie_info.append(input('Clasficación: '))
  movie_info.append(input('Duración: '))
  tmp_genre = input('Género (Elija una opción): ').split(',')
  try:
    tmp_genre = [int(gen) for gen in tmp_genre]
    for i in tmp_genre:
      selected_genres.append(genres[i - 1])

    movie_info.append(selected_genres)

  except:
    print('La introducción de valores no es correcta')
  return movie_info
  
def new_schedule(database, municipio):
  selected_movie = get_user_selected_movie(database, municipio, 0)
  if selected_movie != -1:
    schedule_quantity = int(input('Ingrese la cantidad de horarios a registrar para {} (MAX 10): '.format(selected_movie[2])))

    for i in range(schedule_quantity):
      print('Horario {}'.format(i + 1))
      tmp_schedule = {
        "Película": selected_movie[2],
        "Sala": int(input('Sala #: ')),
        "Hora": input('Hora: '),
        "Fecha": input('Fecha: dd/mm/aaaa: '),
        "Municipio": municipio
      }
      horario.insert_one(tmp_schedule)
    
  else:
    print('No hay películas registradas aún')

def get_movies(database, municipio):
  cursor = database.find({"Municipio" :{"$eq": municipio}})
  results = []
  for i in cursor:
    results.append(i)

  return results

def delete_movie(database, municipio):
  selected_movie = get_user_selected_movie(database, municipio, 1)
  if selected_movie != -1:
    try:
      database.delete_one({"_id": selected_movie[1]})
      print('Película eliminada correctamente')
    except:
      print('Hubo un error al eliminar la película')
  else:
    print('No hay películas registradas aún')

def modify_movie(database, municipio):
  selected_movie = get_user_selected_movie(database, municipio, 2)
  if selected_movie != -1:
    movie_info = get_movie_data()
    try:
      database.update_one(
        {"_id": selected_movie[1]},
        {"$set": {
          "Name": movie_info[0],
          "Director": movie_info[1],
          "Producer": movie_info[2],
          "Rating": movie_info[3],
          "Running_time": movie_info[4],
          "Genre": movie_info[5],
          }
        }
      )
      
      print('Película actualizada exitosamente')
    except:
      print('Ocurrió un error al actualizar la película. Intente de nuevo')

def display_movie(database, municipio):
  selected_movie = get_user_selected_movie(database, municipio, 3)
  cursor = database.find({"_id" : {"$eq": selected_movie[1]}})
  for result in cursor:
    format_movie(result)

def format_movie(movie):
  print("\nNombre: {}".format(movie['Name']))
  print("Director: {}".format(', '.join(movie['Director'])))
  print("Productor: {}".format(', '.join(movie['Producer'])))
  print("Clasificación: {}".format(movie['Rating']))
  print("Duración: {} minutos".format(movie['Running_time']))
  print("Género: {}".format(', '.join(movie['Genre'])))

def format_schedule(schedule):
  print('{}\t\t{}\t{}\t{}'.format(schedule['Película'], schedule['Sala'], schedule['Hora'], schedule['Fecha']))

def get_user_selected_movie(database, municipio, action):
  movies = get_movies(database, municipio)
  header = ['Introduzca los datos', 'Eliminar película', 'Modificar película', 'Cartelera']

  if len(movies) > 0:
    print('-|{}|-'.format(header[action]))
    for i in range(len(movies)):
      print('{} - {}'.format(i + 1, movies[i]['Name']))

    movieIndex = int(input('Elija una película: ')) - 1
    movieId = movies[movieIndex]['_id']
    movieName = movies[movieIndex]['Name']
    
    return [movieIndex, movieId, movieName];
    
  else:
    print('No hay películas registradas aún')
    return -1

def search (database, municipio):
  print('Búsqueda')
  tipoBusqueda = int(input('Ingresa el tipo de búsqueda\n1. Nombre\n2. Género\n3. Clasificación\n'))
  if tipoBusqueda == 1:
    busqueda = input('Ingresa el nombre a buscar: ')
    cursor = database.find({ "$and": [ {"Name": {"$eq": busqueda}}, {"Municipio": {"$eq": municipio}} ]})
  elif tipoBusqueda == 2:
    busqueda = input('Ingresa el género a buscar: ')
    cursor = database.find({ "$and": [ {"Genre": {"$eq": busqueda}}, {"Municipio": {"$eq": municipio}}]})
  elif tipoBusqueda == 3:
    busqueda = input('Ingresa la clasificación a buscar: ')
    cursor = database.find({ "$and": [ {"Rating": {"$eq": busqueda}}, {"Municipio": {"$eq": municipio}}]})

  for result in cursor:
    format_movie(result)

def main():
  # menu()
  # validate_credentials()
  # id_estado, id_municipio = get_billboard()
  # validate_billboard(id_estado, id_municipio)
  selected_database = db.Jalisco

  # if (admin):
  #   menu_admin()
  #   accion = int(input('Elija una opción: '))
  #   if(accion == 1):
        #new_movie(selected_database, municipio)
  #     new_movie()

  # else:
  #   menu_usuario()
  
  # new_schedule(selected_database, 'Zapopan')
  # delete_movie(selected_database, 'Zapopan')
  # modify_movie(selected_database, 'Zapopan')
  # display_movie(selected_database, 'Zapopan')
  # display_billboard(selected_database, 'Zapopan')
  # search(selected_database, 'Zapopan')
  

if __name__ == '__main__':
  main()