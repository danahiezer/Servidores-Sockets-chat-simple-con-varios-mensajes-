import socket
import threading

# lista con los clientes clientes
clientes = []
nombres = {} # aca guardo los nombres de los clientes

def broadcast(mensaje,remitenteConexion):
    # envia un mensaje a todos los clientes excepto al remitente(usuario que envio el mensaje)
    for cliente in clientes:
        if cliente != remitenteConexion: # excluye al cliente que envio el mensaje
            try:
                cliente.send(mensaje.encode("utf-8"))
            except:
                if cliente in clientes:
                    clientes.remove(cliente)

def manejaClientes(conexion,direccion):
    print(f"nuevo cliente conectado: {direccion}")

    conexion.send("bienvenido al chat!.Ingresa tu nombre: ".encode("utf-8"))
    # recibe el nombre del usuario
    nombre = conexion.recv(1024).decode("utf-8")
    # le asigna un puerto especifico en el dicc. para el nombre del usuario
    nombres[conexion] = nombre
    #agrego a la lista ese nombre con su puerto
    clientes.append(conexion)

    mensajeEntrada = f"{nombre} se unio al chat"
    print(mensajeEntrada)
    broadcast(mensajeEntrada,conexion)
    conexion.send("bienvenido! escribe un mensaje ('adios' para salir):".encode("utf-8"))

    while True:
        try:
            # Recibir datos
            mensaje = conexion.recv(1024).decode('utf-8')

            # si no hay mensaje notifica que cliente se desconecto
            if not mensaje:
                print(f"el cliente {direccion} se desconecto")
                break
            print(f"[{direccion}]: {mensaje}")
            # si el cliente dice adios se desconecta y recibe mensaje despedida
            if mensaje.lower() == "adios":
                conexion.send("hasta luego".encode("utf-8"))
                break
            # muestra en el servidor y luego envia a todos el mansaje
            mensajeCompleto = f"{nombre}: {mensaje}"
            print(f"[{direccion}] {mensajeCompleto}")
            broadcast(mensajeCompleto,conexion)

        except:
            print(f"cliente {direccion} se desconecto.")
            break
    clientes.remove(conexion)
    conexion.close()
    mensajeSalida = f"{nombre} ha salido del chat"
    print(mensajeSalida)
    broadcast(mensajeSalida,None)

# Crear el socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurar la dirección y puerto
host = 'localhost'  # Significa "esta misma computadora"
puerto = 5000

# Enlazar el socket a la dirección
servidor.bind((host, puerto))

# Escuchar conexiones (máximo 3 en espera)
servidor.listen(3)
print(f"Servidor milti-cliente escuchando en {host}:{puerto}")

try:
    while True:
        
        # Aceptar una conexión
        conexion, direccion = servidor.accept()
        print(f"Conexión establecida con {direccion}")
        # crea hilo para cada cliente y asi poder atender a todos a la vez
        hilo = threading.Thread(target=manejaClientes, args=(conexion,direccion))
        hilo.start()
        print(f"Clientes activos: {threading.active_count() - 1}")

except KeyboardInterrupt:
    print(f"ERROR DE CONEXION")   
    for cliente in clientes:
        try:
            cliente.send("servidor desconectados".encode("utf-8"))
            cliente.close()
        except:
            pass
finally:        
    servidor.close()
