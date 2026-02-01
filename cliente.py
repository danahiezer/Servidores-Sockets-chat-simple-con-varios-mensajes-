import socket

# Crear el socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
host = 'localhost'
puerto = 5000
cliente.connect((host, puerto))
while True:
    # Enviar mensaje
    mensaje = input("tu: ")
    cliente.send(mensaje.encode('utf-8'))

    if mensaje.lower() == "adios":
        # Recibir respuesta
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f"Servidor responde: {respuesta}")
        break

    respuesta = cliente.recv(1024).decode("utf-8")
    print(f"servidor: {respuesta}")

# Cerrar
cliente.close()