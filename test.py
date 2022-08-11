from ordenamientos import particion, quick
tmp_generos = '1,3,7,8'.split(',')
tmp_generos = [int(genero) for genero in tmp_generos]
selected_genres = []
genres = ['Acción', 'Aventuras', 'Ciencia ficción', 'Comedia', 'Drama', 'Thriller', 'Suspenso', 'Terror', 'Romance', 'Animación']
for i in tmp_generos:
  selected_genres.append(genres[i - 1])

# print(selected_genres)
hora = int('15:30'.replace(':', ''))
fecha = int('10/08/2022'.replace('/',''))

# quick(copy.copy(lista), 0, len(lista) - 1)
horas = [[8, 'hola'], [10, 'Andrea'], [15,'como estas'], [13, 'puñetas']]
horas_tmp = []
for i in range(len(horas)):
  horas_tmp.append(horas[i][0])

result = quick(horas_tmp, 0, len(horas_tmp) - 1)
# print(result)

sorted_billboard = []
for j in range(len(result)):
  for k in horas:
    if result[j] in k:
      sorted_billboard.append(k[1])

# print(sorted_billboard)
# Expected result como estas hola puñetas Andrea
tmp_schedule = {
          "Película": 'Top Gun',
          "Sala": 4,
          "Hora": '14:15',
          "Fecha": '10/08/2022',
          "Municipio": 'Zapopan'
        }
# print(tmp_schedule['Hora'])

hora = '15:30'.split(":")
horasMin, minutos = int(hora[0]) * 60, int(hora[1])
total = horasMin + minutos
fecha = '10/08/2022'.split("/")
dia, mes, anio = int(fecha[0]), int(fecha[1]) * 30, int(fecha[2])
totalDias = dia + mes + anio
print(totalDias) 
