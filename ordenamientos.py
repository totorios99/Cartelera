import time
import copy


def seleccion(lista):
    for i in range(len(lista)):
        # Se asume el primer elemento de la lista como el menor
        valor_menor = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[valor_menor]:
                valor_menor = j
        # Intercambio de valores
        lista[i], lista[valor_menor] = lista[valor_menor], lista[i]
        print(lista)


def seleccion_descendente(lista):
    for i in range(len(lista)):
        # Se asume el primer elemento de la lista como el mayor
        valor_mayor = i
        for j in range(i + 1, len(lista)):
            if lista[j] > lista[valor_mayor]:
                valor_mayor = j
        # Intercambio de valores
        lista[i], lista[valor_mayor] = lista[valor_mayor], lista[i]
        print(lista)


def insercion(lista):
    # Se asume el primer elemento de la lista como el menor
    for i in range(1, len(lista)):
        elemento_a_insertar = lista[i]
        # Se guarda el elemento
        j = i - 1
        # Se recorren todos los elementos de la lista a la posición n + 1, si es que son mayores
        while j >= 0 and lista[j] > elemento_a_insertar:
            lista[j + 1] = lista[j]
            j -= 1
        # Se inserta el elemento
        lista[j + 1] = elemento_a_insertar
        print(lista)


def insercion_descendente(lista):
    # Se asume el primer elemento de la lista como el menor
    for i in range(1, len(lista)):
        elemento_a_insertar = lista[i]
        # Se guarda el elemento
        j = i - 1
        # Se recorren todos los elementos de la lista a la posición n + 1, si es que son mayores
        while j >= 0 and lista[j] < elemento_a_insertar:
            lista[j + 1] = lista[j]
            j -= 1
        # Se inserta el elemento
        lista[j + 1] = elemento_a_insertar
        print(lista)


def shell(lista, n):
    intervalo = n // 2
    while intervalo > 0:
        for i in range(intervalo, n):
            tmp = lista[i]
            j = i
            while j >= intervalo and lista[j - intervalo] > tmp:
                lista[j] = lista[j - intervalo]
                j -= intervalo

            lista[j] = tmp
        intervalo //= 2
        print(lista)


def shell_descendente(lista, n):
    intervalo = n // 2
    while intervalo > 0:
        for i in range(intervalo, n):
            tmp = lista[i]
            j = i
            while j >= intervalo and lista[j - intervalo] < tmp:
                lista[j] = lista[j - intervalo]
                j -= intervalo

            lista[j] = tmp
        intervalo //= 2
        print(lista)


def quick(lista, menor, mayor):
    if menor < mayor:
        # Encontrando el pivote
        pivote = particion(lista, menor, mayor)
        # LLamada recursiva para encontrar el pivote a la izquierda
        quick(lista, menor, pivote - 1)
        # LLamada recursiva para encontrar el pivote a la derecha
        quick(lista, pivote + 1, mayor)
    return lista


def particion(lista, menor, mayor):
    # Tomando el elemento más a la derecha como pivote
    pivote = lista[mayor]
    i = menor - 1
    # Recorrer todos los elementos en la lista y
    # comparar cada uno con el pivote
    for j in range(menor, mayor):
        if lista[j] <= pivote:
            # Si un elemento menor es encontrado, entonces
            # se intercambia por el apuntador + 1 de i
            i += 1

            # Intercambiando elementos en i por los de j
            lista[i], lista[j] = lista[j], lista[i]
    # Intercambiar el elemento pivote con el elemento i + 1
    lista[i + 1], lista[mayor] = lista[mayor], lista[i + 1]
    return i + 1


def particion_descendente(lista, menor, mayor):
    # Tomando el elemento más a la derecha como pivote
    pivote = lista[mayor]
    i = menor - 1
    # Recorrer todos los elementos en la lista y
    # comparar cada uno con el pivote
    for j in range(menor, mayor):
        if lista[j] >= pivote:
            # Si un elemento mayor es encontrado, entonces
            # se intercambia por el apuntador + 1 de i
            i += 1
            # Intercambiando elementos en i por los de j
            lista[i], lista[j] = lista[j], lista[i]
    # Intercambiar el elemento pivote con el elemento i + 1
    lista[i + 1], lista[mayor] = lista[mayor], lista[i + 1]
    return i + 1


def quick_descendente(lista, menor, mayor):
    if menor < mayor:
        # Encontrando el pivote
        pivote = particion_descendente(lista, menor, mayor)
        # LLamada recursiva para encontrar el pivote a la izquierda
        quick_descendente(lista, menor, pivote - 1)
        # LLamada recursiva para encontrar el pivote a la derecha
        quick_descendente(lista, pivote + 1, mayor)
    print(lista)


def merge_ordenamiento(lista_izquierda, lista_derecha):
    lista_ordenada = []
    indice_lista_izquierda = indice_lista_derecha = 0
    longitud_lista_izquierda, longitud_lista_derecha = len(lista_izquierda), len(lista_derecha)
    # Creando variables para la longitud de cada lista
    for i in range(longitud_lista_izquierda + longitud_lista_derecha):
        if indice_lista_izquierda < longitud_lista_izquierda and indice_lista_derecha < longitud_lista_derecha:
            # Se comprueba que el valor de cada elemento en cada lista,
            # para ver cual es menor.
            if lista_izquierda[indice_lista_izquierda] <= lista_derecha[indice_lista_derecha]:
                lista_ordenada.append(lista_izquierda[indice_lista_izquierda])
                indice_lista_izquierda += 1
            # Si el elemento al principio de la lista de la derecha es menor,
            # se añade de igual forma a la lista ordenada
            else:
                lista_ordenada.append(lista_derecha[indice_lista_derecha])
                indice_lista_derecha += 1
        # Si se ha llegado al final de la lista izquierda, se añaden 
        # los elementos de la derecha
        elif indice_lista_izquierda == longitud_lista_izquierda:
            lista_ordenada.append(lista_derecha[indice_lista_derecha])
            indice_lista_derecha += 1
        elif indice_lista_derecha == longitud_lista_derecha:
            lista_ordenada.append(lista_izquierda[indice_lista_izquierda])
            indice_lista_izquierda += 1
    print(lista_ordenada)
    return lista_ordenada

def merge(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    # Divide y vencerás
    lista_izquierda = merge(lista[:medio])
    lista_derecha = merge(lista[medio:])
    return merge_ordenamiento(lista_izquierda, lista_derecha)
    

def merge_ordenamiento_descendente(lista_izquierda, lista_derecha):
    lista_ordenada = []
    indice_lista_izquierda = indice_lista_derecha = 0
    longitud_lista_izquierda, longitud_lista_derecha = len(lista_izquierda), len(lista_derecha)
    # Creando variables para la longitud de cada lista
    for i in range(longitud_lista_izquierda + longitud_lista_derecha):
        if indice_lista_izquierda < longitud_lista_izquierda and indice_lista_derecha < longitud_lista_derecha:
            # Se comprueba que el valor de cada elemento en cada lista,
            # para ver cual es menor.
            if lista_izquierda[indice_lista_izquierda] >= lista_derecha[indice_lista_derecha]:
                lista_ordenada.append(lista_izquierda[indice_lista_izquierda])
                indice_lista_izquierda += 1
            # Si el elemento al principio de la lista de la derecha es menor,
            # se añade de igual forma a la lista ordenada
            else:
                lista_ordenada.append(lista_derecha[indice_lista_derecha])
                indice_lista_derecha += 1
        # Si se ha llegado al final de la lista izquierda, se añaden 
        # los elementos de la derecha
        elif indice_lista_izquierda == longitud_lista_izquierda:
            lista_ordenada.append(lista_derecha[indice_lista_derecha])
            indice_lista_derecha += 1
        elif indice_lista_derecha == longitud_lista_derecha:
            lista_ordenada.append(lista_izquierda[indice_lista_izquierda])
            indice_lista_izquierda += 1
    print(lista_ordenada)
    return lista_ordenada

def merge_descendente(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    # Divide y vencerás
    lista_izquierda = merge_descendente(lista[:medio])
    lista_derecha = merge_descendente(lista[medio:])
    return merge_ordenamiento_descendente(lista_izquierda, lista_derecha)

def burbuja_mejorada(lista):
    for i in range(len(lista)):
        # Uso de la bandera para indicar cuando el programa deber terminar
        # además de utilizarse para indicar cada intercambio
        cambio = False
        for j in range(0, len(lista) - i - 1):
            # Comparar dos elementos adyacentes
            if lista[j] > lista[j + 1]:
                # Intercambio
                tmp = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = tmp
                cambio = True
                print(lista)
        if not cambio:
            break

def burbuja_mejorada_descendente(lista):
    for i in range(len(lista)):
        # Uso de la bandera para indicar cuando el programa deber terminar
        # además de utilizarse para indicar cada intercambio
        cambio = False
        for j in range(len(lista) - 1, 0, -1):
            # Comparar dos elementos adyacentes
            if lista[j] > lista[j - 1]:
                # Intercambio
                tmp = lista[j]
                lista[j] = lista[j - 1]
                lista[j - 1] = tmp
                cambio = True
                print(lista)
        if not cambio:
            break

def validar_entero(numero):
    return int(numero)

def validar_flotante(numero):
    return float(numero)

def crear_lista(rango):
    lista = []
    i = 0
    while i < rango:
        entrada = input("Ingresa el dato {} ".format(i + 1))
        try:
            numero = validar_flotante(entrada)
            if (numero > 0):
                lista.append(numero)
                i += 1
            else: 
                print("Los números negativos no están permitidos")
        except:
            print("El dato ingresado no pertenece al conjunto de los números reales ")
    return lista

def main():
    entrada = input("¿Cuántos numeros ingresarás? (1 - 15) ")
    try:
        num = validar_entero(entrada)
        if (num > 0 and num <= 15):
            lista = crear_lista(num)
            print("\nLa lista quedó así {}".format(lista))

            for i in range(40): print("-", end="")
            print("\nOrdenandola a través el método burbuja mejorada \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            burbuja_mejorada(copy.copy(lista))
            print("\nDescendente")
            burbuja_mejorada_descendente(copy.copy(lista))
            fin = time.time()
            print("Tomó {} segundos ordenar por método burbuja mejorada".format(fin - inicio))
            
            for i in range(40): print("-", end="")
            print("\nOrdenandola a través del método de selección \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            seleccion(copy.copy(lista))
            print("\nDescendente")
            seleccion_descendente(copy.copy(lista))
            fin = time.time()
            print("Tomó {} segundos ordenar por método selección".format(fin - inicio))

            for i in range(40): print("-", end="")
            print("\nOrdenandola a través del método de inserción \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            insercion(copy.copy(lista))
            print("\nDescendente")
            insercion_descendente(copy.copy(lista))
            fin = time.time()
            print("Tomó {} segundos ordenar por método inserción".format(fin - inicio))

            for i in range(40): print("-", end="")
            print("\nOrdenandola a través del método de shell \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            shell(copy.copy(lista), len(lista))
            print("\nDescendente")
            shell_descendente(copy.copy(lista), len(lista))
            fin = time.time()
            print("Tomó {} segundos ordenar por método shell".format(fin - inicio))

            for i in range(40): print("-", end="")
            print("\nOrdenandola a través del método de quick \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            quick(copy.copy(lista), 0, len(lista) - 1)
            print("\nDescendente")
            quick_descendente(copy.copy(lista), 0, len(lista) - 1)
            fin = time.time()
            print("Tomó {} segundos ordenar por método quick".format(fin - inicio))

            for i in range(40): print("-", end="")
            print("\nOrdenandola a través del método de merge \nAscendente")
            # Midiendo el tiempo de ejecución
            inicio = time.time()
            merge(copy.copy(lista))
            print("\nDescendente")
            merge_descendente(copy.copy(lista))
            fin = time.time()
            print("Tomó {} segundos ordenar por método merge".format(fin - inicio))

        else:
            print("Rango inválido (1 - 15)")
    except:
        print("No se ingresó un número válido, intenta de nuevo")
        main()

if __name__ == '__main__':
    main()
