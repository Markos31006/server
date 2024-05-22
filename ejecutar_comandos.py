#!/usr/bin/python3
# Autor: Marc Balaguer Guerra
# Data de creació: 07/05/2024

from pathlib import Path
import subprocess,os

# Abrira el txt y leera la linia que hemos utilizado para leer el nuevo archivo en el script de mirar_carpeta.py
with open("datos.txt", 'r') as archivo_mod:
            ubicacion = archivo_mod.read()
            print(ubicacion)

# El path sirve para cambiar el formato de cadena para que el metodo unlink, que nos servira para borrar el archivo, lo entienda
archivo = Path("datos.txt")
archivo.unlink()

# Abrir el archivo de texto en modo lectura que acaba de llegar
with open(ubicacion, 'r') as file:
    # Leer las líneas del archivo
    for line in file:
        # Dividir cada línea en tres variables utilizando split(',')
        nombre, bd, repliques = line.strip().split(',')
# El print es para ver como funciona el script, en la parte final se quitara
print(nombre,bd,repliques)

def obtener_numero():
    try:
        with open("numero.txt", "r") as f:
            numero = int(f.read())
            return numero
    except FileNotFoundError:
        return 0

def escribir_numero(numero):
    with open("numero.txt", "w") as f:
        f.write(str(numero))

def obtener_puerto():
    try:
        with open("puerto.txt", "r") as f:
            puerto = int(f.read())
            return puerto
    except FileNotFoundError:
        return 30000  # Valor predeterminado del puerto si el archivo no existe

def escribir_puerto(puerto):
    with open("puerto.txt", "w") as f:
        f.write(str(puerto))

def agregar_datos(nombre, puerto):
    numero = obtener_numero()
    puerto = obtener_puerto()
    with open("var.txt", "a") as f:
        f.write("Nombre: {}\tPuerto-Web: {}\tPuerto-PHPMYADMIN: {}\n".format(nombre, puerto+1, puerto+501))
        f.write("i = {}\n\n".format(numero))
    escribir_numero(numero + 1)
    escribir_puerto(puerto + 1)

# Los valores predeterminados para nombre y puerto

puerto = obtener_puerto()

agregar_datos(nombre, puerto)


ultimo_puerto = obtener_puerto()


   
def modificar_archivo(archivo_original, archivo_modificado, palabras_a_modificar):
    try:
        with open(archivo_original, 'r') as archivo_orig:
            contenido = archivo_orig.read()
            
            for palabra_original, palabra_nueva in palabras_a_modificar.items():
                contenido = contenido.replace(palabra_original, palabra_nueva)
                
        with open(archivo_modificado, 'w') as archivo_mod:
            archivo_mod.write(contenido)
            
        print(f"Archivo modificado creado como '{archivo_modificado}'")
    except FileNotFoundError:
        print("¡El archivo original no fue encontrado!")

# Palabras a modificar
#Archivos mysql_deploy.yaml
palabrasmodificar2 = {
    "nombre1": f"{bd}",
    "nombre2": nombre+"-bd",
    "nombre3": nombre+"-mysql-claim",
    "nombre4": nombre+"-mysql",
}

#Archivos mysql_svc.yaml
palabrasmodificar3 = {
    "nombre1": nombre+"-mysql-service",  
    "nombre2": nombre+"-mysql",  
}

#Archivos webapp_deploy.yaml
palabrasmodificar4 = {
    "repliques": str(repliques),
    "nombre3": nombre+"-webapp-claim",
    "nombre4": nombre+"-webapp",
}

#Archivos webapp_svc.yaml
palabrasmodificar5 = {
    "nombre1": nombre+"-webapp",
    "puerto_webapp": str(ultimo_puerto),
}

#Archivos phpmyadmin_deploy.yaml
palabrasmodificar6 = {
    "nombre4": nombre+"-phpmyadmin",
    "servicio_mysql": nombre+"-mysql-service",
    "nombre3": nombre+"-phpmyadmin-claim",
}

#Archivos phpmyadmin_svc.yaml
palabrasmodificar7 = {
    "nombre1": nombre+"-phpmyadmin",
    "puerto_phpmyadmin": str(ultimo_puerto+500),
}


#Modifica el archivo mysql_deploy.yaml
modificar_archivo("default_conf/mysql_deploy.yaml", f"final_conf/{nombre}_mysql_deploy.yaml", palabrasmodificar2)

#Modifica el archivo mysql_svc.yaml
modificar_archivo("default_conf/mysql_svc.yaml", f"final_conf/{nombre}_mysql_svc.yaml", palabrasmodificar3)

#Modifica el archivo webapp_deploy.yaml
modificar_archivo("default_conf/webapp_deploy.yaml", f"final_conf/{nombre}_webapp_deploy.yaml", palabrasmodificar4)

#Modifica el archivo webapp_svc.yaml
modificar_archivo("default_conf/webapp_svc.yaml", f"final_conf/{nombre}_webapp_svc.yaml", palabrasmodificar5)

#Modifica el archivo phpmyadmin_deploy.yaml
modificar_archivo("default_conf/phpmyadmin_deploy.yaml", f"final_conf/{nombre}_phpmyadmin_deploy.yaml", palabrasmodificar6)

#Modifica el archivo phpmyadmin_svc.yaml
modificar_archivo("default_conf/phpmyadmin_svc.yaml", f"final_conf/{nombre}_phpmyadmin_svc.yaml", palabrasmodificar7)

# Esta función es para ejecutar cualquier comando y poder leer la salida de el
def ejecutar_comando(comando):
    # Ejecutar el comando y capturar la salida
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Leer la salida del comando
    salida, error = proceso.communicate()

    # Verificar si ahi errores
    if proceso.returncode != 0:
        print("Error:", error.decode("utf-8"))
    else:
        print("Salida:", salida.decode("utf-8"))


comando2 = f"kubectl create -f final_conf/{nombre}_mysql_svc.yaml"
salida2 = ejecutar_comando(comando2)
print(salida2)

comando3 = f"kubectl create -f final_conf/{nombre}_mysql_deploy.yaml"
salida3 = ejecutar_comando(comando3)
print(salida3)

comando4 = f"kubectl create -f final_conf/{nombre}_webapp_deploy.yaml"
salida4 = ejecutar_comando(comando4)
print(salida4)

comando5 = f"kubectl create -f final_conf/{nombre}_webapp_svc.yaml"
salida5 = ejecutar_comando(comando5)
print(salida5)

comando6 = f"kubectl create -f final_conf/{nombre}_phpmyadmin_deploy.yaml"
salida6 = ejecutar_comando(comando6)
print(salida6)

comando7 = f"kubectl create -f final_conf/{nombre}_phpmyadmin_svc.yaml"
salida7 = ejecutar_comando(comando7)
print(salida7)