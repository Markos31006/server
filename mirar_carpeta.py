#!/usr/bin/python3
# Autor: Marc Balaguer Guerra
# Data de creació: 07/05/2024


import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

def on_created(event):
    # Obtiene la dirección del archivo creado
    direccion_archivo = event.src_path
    # Crea un archivo o lo modifica y pone los datos.
    with open("datos.txt", 'a') as archivo_mod:
            archivo_mod.write(direccion_archivo)
    # Ejecuta el otro script y pasa la dirección del archivo como argumento
    subprocess.run(["/usr/bin/python3", "ejecutar_comandos.py"])

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Llama a la función definida fuera de la clase para manejar el evento de creación de archivos
        on_created(event)

def observar_directorio(directorio):
    observer = Observer()
    observer.schedule(Handler(), path=directorio, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directorio_a_observar = "/home/kuser/Scripts/arribades "
    observar_directorio(directorio_a_observar)