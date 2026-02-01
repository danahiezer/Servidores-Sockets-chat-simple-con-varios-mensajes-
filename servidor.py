import socket
import threading


def manejaClientes(conexion,direccion):
    print(f"nuevo cliente conectado: {direccion}")

    conexion.send("bienvenido al servidor!".encode("utf-8"))

    while True:
        try:
            # Recibir datos
            mensaje = conexion.recv(1024).decode('utf-8')
            
            if not mensaje:
                print(f"el cliente {direccion} se desconecto")
                break
            print(f"[{direccion}]: {mensaje}")

            if mensaje.lower() == "adios":
                conexion.send("hasta luego".encode("utf-8"))
                break

            respuesta = mensaje.upper()
            conexion.send(respuesta.encode("utf-8"))

        except:
            print(f"error con cliente {direccion}")
        
    conexion.close()
    print(f"conexion cerrada con [{direccion}]")

# Crear el socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurar la dirección y puerto
host = 'localhost'  # Significa "esta misma computadora"
puerto = 5000

# Enlazar el socket a la dirección
servidor.bind((host, puerto))

# Escuchar conexiones (máximo 1 en espera)
servidor.listen(4)
print(f"Servidor milti-cliente escuchando en {host}:{puerto}")
try:
    while True:
        # Aceptar una conexión
        conexion, direccion = servidor.accept()
        print(f"Conexión establecida con {direccion}")

        hilo = threading.Thread(target=manejaClientes, args=(conexion,direccion))
        hilo.start()
except KeyboardInterrupt:
    print(f"servidor detenido por el usuario")
    servidor.close()
#