# Script para obtener portada de un anime utilizando la API de Kitsu
# El nombre del anime es el nombre de la carpeta, excluyendo etiquetas de calidad e idioma

import os
import requests
import json
import urllib.parse
import time

# Revisa subcarpetas en la ruta para obtener la portada de los animes
def obtener_portadas(ruta):
    for carpeta in os.listdir(ruta):
        # Si es una carpeta, se busca en sus subdirectorios, excluyendo carpetas ocultas y carpetas de sistema
        if os.path.isdir(os.path.join(ruta, carpeta)) and not carpeta.startswith(".") and not carpeta.startswith("$"):
            obtener_portadas(os.path.join(ruta, carpeta))
            # Se obtiene la portada del anime
            portada = animeScrap(os.path.join(ruta, carpeta))
            print(portada)

# Obtiene la portada del anime
def animeScrap(ruta):
    # Obtiene nombre de carpeta y extrae el nombre del anime

    nombre = os.path.basename(ruta)
    # Elimina etiquetas de idioma
    nombre = nombre.split("(")[0]
    print(nombre)
    # url = the target we want to open
    url = 'https://kitsu.io/api/edge/anime?filter[text]={}'.format(urllib.parse.quote(nombre))
    print(url)
    # open with GET method
    resp = requests.get(url)
    # Sleep por medio segundo para no saturar el servidor
    time.sleep(0.5)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        
        # we need a parser,Python built-in HTML parser is enough .
        resultado = json.loads(resp.content)        
        try:
            portada = resultado['data'][0]['attributes']['posterImage']['large']            
            # Descarga la portada en la carpeta de la serie con el nombre "folder.jpg"
            portada = requests.get(portada)
            time.sleep(0.5)
            with open(os.path.join(ruta, "folder.jpg"), 'wb') as f:
                f.write(portada.content)
            resultado = "Portada de {} descargada".format(nombre)
            # Se obtiene el nombre de la carpeta


        except:
            resultado = "Serie {} no encontrada".format(nombre)

    else:
        resultado = "Error en la petición"
    return resultado


if __name__ == "__main__":
    # No recibe argumentos, se ejecuta en la carpeta actual
    ruta = os.getcwd()
    print(obtener_portadas(ruta))
