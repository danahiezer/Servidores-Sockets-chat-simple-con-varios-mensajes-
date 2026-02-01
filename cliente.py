import socket

# Crear el socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
cliente.connect(("localhost", 5000))
# recibe la bienvenida del servidor
bienvenida = cliente.recv(1024).decode("utf-8")
print(f"servidor: {bienvenida} ")

while True:
    # Enviar mensaje
    mensaje = input("tu: ")
    cliente.send(mensaje.encode('utf-8'))
    # recibe respuesta del servidor
    respuesta = cliente.recv(1024).decode("utf-8")
    print(f"servidor: {respuesta}")
    # si el usuario pone adios. se desconecta del servidor
    if mensaje.lower() == "adios":
        break

# Cerrar
cliente.close()