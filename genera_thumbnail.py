# Script que recorre todas las carpetas y subcarpetas de la ruta en la que se encuentra y genera una miniatura de los videos que encuentre
# Requiere tener instalado ffmpeg

import os
import subprocess
import sys

# Genera contadores
contador_avance = 0
contador_archivos = 0


# Cuenta la cantidad de archivos a editar
def contar_archivos(ruta):
    # Lista los archivos y carpetas de la ruta
    try:
        for archivo in os.listdir(ruta):
            # Si es un directorio, se busca en sus subdirectorios, excluyendo carpetas ocultas y carpetas de sistema
            if os.path.isdir(os.path.join(ruta, archivo)) and not archivo.startswith(".") and not archivo.startswith("$"):
                contar_archivos(os.path.join(ruta, archivo))
            # Si es un archivo, se genera la miniatura
            elif os.path.isfile(os.path.join(ruta, archivo)):
                # Si es un video aumenta la variable global contador_archivos
                if archivo.endswith(".mp4") or archivo.endswith(".avi") or archivo.endswith(".mkv"):
                    global contador_archivos
                    contador_archivos += 1

    except PermissionError:
        print("No se tienen permisos para acceder a la carpeta ", ruta)

# Lista directorios y archivos de la ruta
def lista_directorios(ruta):
    # Lista los archivos y carpetas de la ruta
    try:       
        for archivo in os.listdir(ruta):
            # Si es un directorio, se busca en sus subdirectorios
            if os.path.isdir(os.path.join(ruta, archivo)) and not archivo.startswith(".") and not archivo.startswith("$"):
                lista_directorios(os.path.join(ruta, archivo))
            # Si es un archivo, se genera la miniatura, excluyendo carpetas ocultas y carpetas de sistema
            elif os.path.isfile(os.path.join(ruta, archivo)) and not archivo.startswith(".") and not archivo.startswith("$"):
                # Si es un video, se genera la miniatura
                if archivo.endswith(".mp4") or archivo.endswith(".avi") or archivo.endswith(".mkv"):
                    global contador_avance
                    contador_avance += 1
                    global contador_archivos
                    print("Procesando archivo ", contador_avance, " de ", contador_archivos, ": ", archivo)
                    # Se genera la miniatura, entrega ruta y nombre del archivo por separado
                    generar_miniatura(ruta, archivo)
    except PermissionError:
        print("No se tienen permisos para acceder a la carpeta ", ruta)

# Genera una miniatura para el video, recibe la ruta completa del video
def generar_miniatura(ruta, archivo):
    # Se obtiene el nombre del archivo sin la extensión
    nombre = archivo.split(".")[0]
    # Se obtiene la ruta del archivo
    ruta_archivo = os.path.join(ruta, archivo)
    # Se obtiene la ruta de la miniatura
    ruta_miniatura = os.path.join(ruta, nombre + ".jpg")
    # Si ya existe la miniatura, no se genera
    if os.path.exists(ruta_miniatura):
        print("Miniatura de archivo ", archivo, " ya existe")
        return
    # Se genera la miniatura de un frame aleatorio con ffmpeg, sin verbose
    #subprocess.run(["ffmpeg", "-i", ruta_archivo, "-ss", "00:03:00", "-vframes", "1", ruta_miniatura], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-i", ruta_archivo, "-vf", "thumbnail", "-frames:v", "1", ruta_miniatura], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Miniatura de archivo ", archivo, " generada")

if __name__ == "__main__":
    # Si no hay ruta, se toma la ruta actual
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    # Genera miniaturas para los videos de la ruta y subrutas
    contar_archivos(ruta)
    lista_directorios(ruta)