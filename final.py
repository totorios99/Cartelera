import json
import os
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
  print('\n1. Alta película \n2. Alta horario \n3. Baja película \n4. Baja horario \n5. Modificar película \n6. Consultar película \n7. Consultar cartelera \n8. Salir')

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

def display_billboard(database, municipio): 
  print('-'*70)
  cursor = horario.find({"Municipio": {"$eq": municipio}})
  results = []

  for i in cursor:
    results.append(i)
    
  if len(results) > 0: 
    sorted_billboard = []
    date = []
    time = []
    room = []
    auxDate = []
    auxTime = []
    auxRoom = []

    for result in cursor:
      tmp_date = []
      tmp_time = []
      tmp_room = []
      
      tmp_date.append(int(result['Fecha'].replace('/', '')))
      tmp_date.append(result['_id'])
      auxDate.append(int(result['Fecha'].replace('/', '')))

      tmp_time.append(int(result['Hora'].replace(':', '')))
      tmp_time.append(result['_id'])
      auxTime.append(int(result['Hora'].replace(':', '')))
      
      tmp_room.append(int(result['Sala']))
      tmp_room.append(result['_id'])
      auxRoom.append(int(result['Sala']))

      date.append(tmp_date)
      time.append(tmp_time)
      room.append(tmp_room)

      format_schedule(result)

    sorting_option = int(input('\nSi desea ver la cartelera por orden, ingrese \n1. Horario\n2. Fecha\n3. Sala\n4. Salir\n'))
    if sorting_option == 1:
      os.system('clear')
      sorted_schedule = quick(auxTime, 0, len(auxTime) - 1)
      for i in range(len(sorted_schedule)):
        for j in time:
          if sorted_schedule[i] in j:
            sorted_billboard.append(j[1])

      for movie in range(len(sorted_billboard)):
        for result in cursor:
          if result['_id'] == sorted_billboard[movie]:
            format_schedule(result)

    elif sorting_option == 2:
      os.system('clear')
      sorted_schedule = quick(auxDate, 0, len(auxDate) - 1)
      for i in range(len(sorted_schedule)):
        for j in date:
          if sorted_schedule[i] in j:
            sorted_billboard.append(j[1])

      for movie in range(len(sorted_billboard)):
        for result in cursor:
          if result['_id'] == sorted_billboard[movie]:
            format_schedule(result)

    elif sorting_option == 3:
      os.system('clear')
      sorted_schedule = quick(auxRoom, 0, len(auxRoom) - 1)
      for i in range(len(sorted_schedule)):
        for j in room:
          if sorted_schedule[i] in j:
            sorted_billboard.append(j[1])
      
      for movie in range(len(sorted_billboard)):
        for result in cursor:
          if result['_id'] == sorted_billboard[movie]:
            format_schedule(result)
    else:
      print('No hay películas registradas aún')

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
  print('\nAlta horario. Recordar que el horario de trabajo es de 11:00 - 00:00')
  selected_movie = get_user_selected_movie(database, municipio, 0)
  filledSchedule = 0
  if selected_movie != -1:
    schedule_quantity = int(input('Ingrese la cantidad de horarios a registrar para {} (MAX 10): '.format(selected_movie[2])))
    if schedule_quantity > 10:
      print('\nEl máximo permitido es 10 horarios por película')

    while filledSchedule <= 10:
      for i in range(schedule_quantity):
        print('Horario {}'.format(i + 1))
        tmp_schedule = {
          "Película": selected_movie[2],
          "Sala": int(input('Sala #: ')),
          "Hora": input('Hora: '),
          "Fecha": input('Fecha: dd/mm/aaaa: '),
          "Municipio": municipio,
          "Duración": input('Duración: ')
        }
        
        if(valid_schedule(tmp_schedule, database, municipio)):
          horario.insert_one(tmp_schedule)
          filledSchedule += 1
        else: 
          print('Error, la sala no puede ser ocupada en ese horario')
    
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

def search(database, municipio):
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

def valid_schedule(schedule, database, municipio):
  sala = schedule['Sala']
  hora = schedule['Hora']
  fecha = schedule['Fecha']
  duración = schedule['Duración']
  ocupados = []
  lapsoTranscurrido = obtener_lapso_transcurrido(hora, fecha, duración)

  if(lapsoTranscurrido[0] < 660 or lapsoTranscurrido[1] > 1430):
    return False

  roomFilter = database.find({ "$and": [ {"Sala": {"$eq": sala}}, {"Municipio": {"$eq": municipio}} ]})
  results = []
  for result in roomFilter:
    ocupados.append(obtener_lapso_transcurrido(result['Hora'], result['Fecha'], result['Duración']))

  for lapso in ocupados:
    if lapsoTranscurrido[1] > lapso[1] and lapsoTranscurrido[2] < lapso[2]:
      return False
    else:
      return True

def obtener_lapso_transcurrido(hora, fecha, duración):
  hora = hora.split(":")
  fecha = fecha.split("/")
  horasMin, minutos = int(hora[0]) * 60, int(hora[1])
  minutosDelDia = horasMin + minutos

  dia, mes, anio = int(fecha[0]), int(fecha[1]) * 30, int(fecha[2])
  totalDias = dia + mes + anio
  
  lapsoTranscurrido = totalDias + minutosDelDia
  fin = duración + lapsoTranscurrido + 30
  return [minutosDelDia, lapsoTranscurrido, fin]

def select_database(id_estado):
  if id_estado == 'J11':
    return db.Jalisco
  elif id_estado == 'N11':
    return db.NuevoLeon
  elif id_estado == 'E11':
    return db.EdoMex
  elif id_estado == 'C11':
    return db.Tamaulipas
  else:
    return db.Sinaloa

def cerrar_db():
  client.close()
  
def main():
  salir = False
  menu()
  validate_credentials()
  id_estado, id_municipio = get_billboard()
  validate_billboard(id_estado, id_municipio)
  selected_database = select_database(id_estado)
  municipio_seleccionado = base[id_estado][id_municipio]

  while not salir:
    if (admin):
      menu_admin()
      accion = int(input('Elija una opción: '))
      if(accion == 1):
        new_movie(selected_database, municipio_seleccionado)
      elif(accion == 2):
        new_schedule(selected_database, municipio_seleccionado)
      elif(accion == 3):
        delete_movie(selected_database, municipio_seleccionado)
      elif(accion == 4):
        pass
      elif(accion == 5):
        modify_movie(selected_database, municipio_seleccionado)
      elif(accion == 6):
        display_movie(selected_database, municipio_seleccionado)
      elif(accion == 7):
        display_billboard(selected_database, municipio_seleccionado)
      elif(accion == 8):
        cerrar_db()
        salir = True
      else:
        print('Opción incorrecta, intente de nuevo')
    else:
      menu_usuario()
      accion = int(input('Elija una opción: '))
      if(accion == 1):
        search(selected_database, municipio_seleccionado)
      elif(accion == 2):
        search(selected_database, municipio_seleccionado)
      elif(accion == 3):
        search(selected_database, municipio_seleccionado)
      elif(accion == 4):
        display_billboard(selected_database, municipio_seleccionado)
      elif(accion == 5):
        display_movie(selected_database, municipio_seleccionado)
      elif(accion == 6):
        display_billboard(selected_database, municipio_seleccionado)
      elif(accion == 7):
        cerrar_db()
        salir = True
      else:
        print('Opción incorrecta, intente de nuevo')

if __name__ == '__main__':
  main()