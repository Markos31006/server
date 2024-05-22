#!/usr/bin/python3
# Autor: Marc Balaguer Guerra
# Data de creació: 15/05/2024

import socket, time

# Crear un socket TCP/IP
# Dirección IP y puerto del servidor
HOST = '0.0.0.0'  # Dirección IP local
PORT = 5000         # Puerto que abriremos
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Enlazar el socket a la dirección y puerto especificados
        servidor.bind((HOST, PORT))

        # Escuchar conexiones entrantes
        servidor.listen()
        while True:
            time.sleep(1)

            # Aceptar conexiones entrantes
            conn, addr = servidor.accept()

            with conn:
                print('Connexió establerta amb:', addr)
                try:
                    with open('/home/marc/Scripts/var.txt', 'r') as archivo:
                        contenido = archivo.read()
                        conn.sendall(contenido.encode())
                except FileNotFoundError:
                    conn.sendall("No s'ha trobat l'arxiu en el servidor.".encode())
                    print("No s'ha trobat l'arxiu.")