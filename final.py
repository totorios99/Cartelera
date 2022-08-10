from getpass import getpass
from decouple import config
from pymongo import MongoClient
from Cartelera import base

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

admin = False

peliculas = []

def database_connection():
  peliculas = collection.Películas
  cursor = peliculas.find()
  for i in cursor:
    print(i['Name'])


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

def display_billboard():
  pass

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

def new_movie(database):
  movie_info = get_movie_data()
  print(movie_info)
  movie_doc = {
    "Name": movie_info[0],
    "Director": movie_info[1],
    "Producer": movie_info[2],
    "Rating": movie_info[3],
    "Running_time": movie_info[4],
    "Genre": movie_info[5],
  }

  database.insert_one(movie_doc)
  
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
  
def main():
  # menu()
  # validate_credentials()
  # id_estado, id_municipio = get_billboard()
  # validate_billboard(id_estado, id_municipio)

  # if (admin):
  #   menu_admin()
  #   accion = int(input('Elija una opción: '))
  #   if(accion == 1):
  #     new_movie('Jalisco')

  # else:
  #   menu_usuario()
  database = db.Jalisco
  
  new_movie(database)

if __name__ == '__main__':
  main()