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
  peliculas = db.Películas
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
    print('Bienvenido al sistema de cartelera')
    
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

  return isValid

def main():
  menu()
  validate_credentials()
  id_estado, id_municipio = get_billboard()
  validate_billboard(id_estado, id_municipio)
  
  if (admin):
    menu_admin()
  else:
    menu_usuario()

if __name__ == '__main__':
  main()