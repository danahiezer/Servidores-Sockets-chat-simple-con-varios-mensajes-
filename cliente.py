import socket

# Crear el socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
host = 'localhost'
puerto = 5000
cliente.connect((host, puerto))

# Enviar mensaje
mensaje = "Hola servidor!"
cliente.send(mensaje.encode('utf-8'))

# Recibir respuesta
respuesta = cliente.recv(1024).decode('utf-8')
print(f"Servidor responde: {respuesta}")

# Cerrar
cliente.close()