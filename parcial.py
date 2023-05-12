#PRIMER PARCIAL LABORATORIO
#NOMBRE: LAURA SILVINA GAUTO MORALES
#DIVISION 1-B

import csv
import re
from unidecode import unidecode
import random
from datetime import datetime
import json

ruta = "DBZ.csv"


def parser_csv(path:str) -> list:
    with open(path, "r", encoding="utf-8") as archivo_dbz:
        lista_personajes_csv = []
        for personaje in archivo_dbz:
            linea = personaje.replace("\n", "")
            linea_aux = linea.split(",")
            lista_personajes_csv.append(linea_aux)
    return lista_personajes_csv

lista_personajes_csv = parser_csv(ruta)

def convertir_a_diccionario(lista):
    lista_personajes =[]
    
    for personaje in lista:
        lista_habilidades = []
        diccionario_personaje = {}
        diccionario_personaje["Id"] = int(personaje[0])
        diccionario_personaje["Nombre"] = personaje[1]
        
        if  "-Humano" in personaje[2]:
            diccionario_personaje["Raza"] =  re.split("-", personaje[2])
        else:
            diccionario_personaje["Raza"] = personaje[2]

        diccionario_personaje["Poder de pelea"] = float(personaje[3])
        diccionario_personaje["Poder de ataque"] = float(personaje[4])
        habilidades = personaje[5].split("|$%")
        for valor in habilidades:    
            habilidad = valor.strip(" ")
            lista_habilidades.append(habilidad)
            diccionario_personaje["Habilidades"] = lista_habilidades

        lista_personajes.append(diccionario_personaje)
    return lista_personajes

lista_personajes = convertir_a_diccionario(lista_personajes_csv)

'''
2. Listar cantidad por raza: mostrará todas las razas indicando la cantidad de personajes que
corresponden a esa raza.
'''


def setear_lista_razas(lista):
    lista_razas = []
    for personaje in lista:
        raza = personaje["Raza"]
        if type(raza) == list:
            for subraza in raza:
                lista_razas.append(subraza)
        else:
            lista_razas.append(raza)
    lista_razas = set(lista_razas)
    return lista_razas



def listar_cantidad_por_raza(lista):
    lista_razas = setear_lista_razas(lista)
    for raza in lista_razas:
        contador = 0
        for personaje in lista:
            if type(personaje["Raza"]) == list:
                for subraza in personaje["Raza"]:
                    if raza == subraza:
                        contador += 1
            else:
                if raza == personaje["Raza"]:
                    contador += 1
        print(f"{raza}: {contador}")


'''
3. Listar personajes por raza: mostrará cada raza indicando el nombre y poder de ataque de cada
personaje que corresponde a esa raza. Dado que hay personajes que son cruza, los mismos podrán
repetirse en los distintos listados.
'''

def listar_por_raza(lista):
    lista_razas = setear_lista_razas(lista)
    for raza in lista_razas:
        print(f"Raza: {raza}")
        for personaje in lista:
            if type(personaje["Raza"]) == list:
                for subraza in personaje["Raza"]:
                    if subraza == raza:
                        print(f"    {personaje['Nombre']} - Poder de Ataque {personaje['Poder de ataque']}")
                        
            else:
                if personaje["Raza"] == raza:
                    print(f"    {personaje['Nombre']} -Poder de Ataque {personaje['Poder de ataque']}")



'''
4. Listar personajes por habilidad: el usuario ingresa la descripción de una habilidad y el programa
deberá mostrar nombre, raza y promedio de poder entre ataque y defensa.
'''
def reemplazar_tildes(texto):
    texto_sin_tildes = unidecode(texto)
    return texto_sin_tildes

def listar_por_habilidad(lista):
    ingreso_usuario = input("Ingrese una habilidad").lower()
    if ("-") in ingreso_usuario:
        ingreso_usuario = ingreso_usuario.replace("-", "")
    ingreso_usuario = reemplazar_tildes(ingreso_usuario)
    lista_coincidencias = []
    for personaje in lista:       
        if type(personaje["Habilidades"]) == list:
            for subhabilidad in personaje["Habilidades"]:
                if ("-") in subhabilidad:
                    subhabilidad = subhabilidad.replace("-", "")
                habilidad = subhabilidad.lower()
                habilidad = reemplazar_tildes(habilidad)
                if habilidad == ingreso_usuario:
                    lista_coincidencias.append(personaje["Nombre"])
    return lista_coincidencias


def mostrar_datos_coincidencias(lista):
    lista_coincidencias = listar_por_habilidad(lista) #aca me devuelve el listado de concidencias
    if len(lista_coincidencias) == 0:
        print("No se encontraron coincidencias")
    else:
        for personaje in lista:
            for nombre in lista_coincidencias:
                if nombre == personaje["Nombre"]:
                    nombre = personaje["Nombre"]
                    poder_ataque = personaje["Poder de ataque"]
                    poder_pelea = personaje["Poder de pelea"]
                    promedio = (poder_ataque+poder_pelea)/2
                    if type(personaje["Raza"]) == list:
                        raza_lista = personaje["Raza"]
                        separador = "/"
                        raza = separador.join(raza_lista)
                    else:
                        raza = personaje["Raza"]
                    print(f"Nombre: {nombre} Raza: {raza} Promedio entre poder de ataque y poder de pelea: {promedio}")


'''
5. Jugar batalla: El usuario seleccionará un personaje. La máquina selecciona otro al azar. 

Gana la batalla el personaje que más poder de ataque tenga.
El personaje que gana la batalla se deberá guardar en un archivo de texto, 
incluyendo la 
fecha de la batalla, 
-el nombre del personaje que ganó y
-el nombre del perdedor. 
-Este archivo anexará cada dato.
'''
def jugar_batalla(lista):
    #definir jugador usuario
    eleccion_usuario = input("Ingrese un nombre de un personaje").lower()
    bandera_coincidencia = False

    #todos los personajes del diccionario principal los vuelvo lower
    for personaje in lista:
        nombre_lower = personaje["Nombre"].lower()

        #valido que el ingreso del usuario exista en la lista
        if(eleccion_usuario == nombre_lower):
            poder_ataque_usuario = personaje["Poder de ataque"]
            nombre_jugador_usuario = personaje["Nombre"]
            bandera_coincidencia = True
    if bandera_coincidencia == True:
        jugador_usuario = eleccion_usuario
    else:
        print("No existe")

    #definir jugador maquina
    eleccion_maquina = random.choice(lista)
    #(nombre_maquina)
    jugador_maquina = eleccion_maquina["Nombre"].lower()

    #validar que el jugador que ingreso el usuario no sea el mismo que el que genero la maquina
    while jugador_usuario == jugador_maquina:
        print("eligiendo otro personaje")
        eleccion_maquina = random.choice(lista)
        jugador_maquina = eleccion_maquina["Nombre"].lower()
    
    nombre_jugador_maquina = eleccion_maquina["Nombre"]
    poder_ataque_maquina = eleccion_maquina["Poder de ataque"]

    if poder_ataque_maquina > poder_ataque_usuario:
        ganador = nombre_jugador_maquina
        perdedor = nombre_jugador_usuario
    else:
        ganador = nombre_jugador_usuario
        perdedor = nombre_jugador_maquina
    
    fecha_hora_actual = datetime.now()
    
    with open("batallas.txt", "a", encoding="utf-8") as prueba_archivo:
        with open("batallas.txt", "r", encoding="utf-8") as lectura_archivo:
            lectura = lectura_archivo.read()
        if lectura == "":
            prueba_archivo.write(f"Ganador: {ganador} | Perdedor: {perdedor}| Fecha de batalla: {fecha_hora_actual}")
        else:
            prueba_archivo.write(f"\n Ganador: {ganador} | Perdedor: {perdedor}| Fecha de batalla: {fecha_hora_actual}")

#jugar_batalla(lista_personajes)

'''
Guardar Json: El usuario ingresa una raza y una habilidad. 
Generar un listado de los personajes que cumplan con los dos criterios ingresados, los mismos se guardarán en un archivo Json. 
Deberíamos guardar el 
-nombre del personaje, 
-el poder de ataque, y 
-las habilidades que no fueron parte de la búsqueda. 
El nombre del archivo estará nomenclado con la descripción de la habilidad y de la raza.
'''


def guardar_json(lista):
    ingreso_raza = input("Ingrese una raza").lower()

    ingreso_habilidad = input("Ingrese una habilidad").lower() 
    
    diccionario_personaje_principal = {}
    diccionario_personaje_principal["Personaje"] = []
    #banderas para determinar que la habilidad y la raza que ingreso el usuario existan
    bandera_coincidencia = False

    for personaje in lista:
        bandera_coincidencia_habilidad = False
        bandera_coincidencia_raza = False


        if type(personaje["Raza"]) == list:
            for subraza in personaje["Raza"]:
                personaje_raza = subraza.lower()
                if personaje_raza == ingreso_raza:
                    bandera_coincidencia_raza = True
        else:
            personaje_raza = personaje["Raza"].lower()
            if personaje_raza == ingreso_raza:
                bandera_coincidencia_raza = True
        
        if type(personaje["Habilidades"]) == list:
            #Mind Control |$%Summon Majins
            for subhabilidad in personaje["Habilidades"]:
                personaje_habilidad = subhabilidad.lower()
                if personaje_habilidad == ingreso_habilidad:
                    bandera_coincidencia_habilidad = True
                    
        else:
            personaje_habilidad = personaje["Habilidades"].lower()
            if personaje_habilidad == ingreso_habilidad:
                    bandera_coincidencia_habilidad = True
                    

        if (bandera_coincidencia_raza == True) and (bandera_coincidencia_habilidad == True):
            lista_habilidades = []
            #traigo las habilidades que no ingreso el usuario
            nombre_coincidencia = personaje["Nombre"]
            #vuelvo a recorrer la lista
            for personaje in lista:
                if type(personaje["Habilidades"]) == list:
                    for subhabilidad in personaje["Habilidades"]:
                        nombre_habilidad_lower = subhabilidad.lower() #para comparar con ingreso habilidad
                        if (nombre_coincidencia == personaje["Nombre"]) and (nombre_habilidad_lower != ingreso_habilidad):
                            lista_habilidades.append(nombre_habilidad_lower)
                            diccionario = {}
                            diccionario["Nombre"] = personaje["Nombre"]
                            diccionario["Poder de ataque"] = personaje["Poder de ataque"]
                            diccionario["Habilidades"] = lista_habilidades
                            diccionario_personaje_principal["Personaje"].append(diccionario)
                            
                else:
                    nombre_habilidad_lower = personaje_habilidad.lower()
                    if (nombre_coincidencia == personaje["Nombre"]) and (nombre_habilidad_lower != ingreso_habilidad):
                            lista_habilidades.append(nombre_habilidad_lower)
                            diccionario = {}
                            diccionario["Nombre"] = personaje["Nombre"]
                            diccionario["Poder de ataque"] = personaje["Poder de ataque"]
                            diccionario["Habilidades"] = lista_habilidades
                            diccionario_personaje_principal["Personaje"].append(diccionario)
            bandera_coincidencia = True
        
    #informar al usuario que no hubo coincidencia
    if bandera_coincidencia == False:
        print("no hubo coincidencia")
    print(diccionario_personaje_principal)

guardar_json(lista_personajes)