import socket

# Crear el socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurar la dirección y puerto
host = 'localhost'  # Significa "esta misma computadora"
puerto = 5000

# Enlazar el socket a la dirección
servidor.bind((host, puerto))

# Escuchar conexiones (máximo 1 en espera)
servidor.listen(1)
print(f"Servidor escuchando en {host}:{puerto}")

# Aceptar una conexión
conexion, direccion = servidor.accept()
print(f"Conexión establecida con {direccion}")

while True:
    # Recibir datos
    mensaje = conexion.recv(1024).decode('utf-8')
    
    if not mensaje:
        print("el cliente se desconecto")
        break
    print(f"cliente:{mensaje}")

    if mensaje.lower() == "adios":
        conexion.send("hasta luego".encode("utf-8"))
        break
    respuesta = f"recibido: {mensaje}"
    conexion.send(respuesta.encode("utf-8"))
# Enviar respuesta
conexion.send(f"Echo: {mensaje}".encode('utf-8'))

# Cerrar
conexion.close()
servidor.close()
#