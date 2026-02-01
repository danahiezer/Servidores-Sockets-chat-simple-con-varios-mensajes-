import socket
import threading

def recibirMensajes(cliente):
    while True:
        try:
            # recibe mensaje
            mensaje = cliente.recv(1024).decode("utf-8")
            if mensaje:
                print(f"{mensaje}")
            else:
                break

        except:
            print("Saliste del chat")
            break


# Crear el socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
cliente.connect(("localhost", 5000))

# recibe la bienvenida del servidor
solicitud = cliente.recv(1024).decode("utf-8")
nombre = input(solicitud)
cliente.send(nombre.encode("utf-8"))

hilo = threading.Thread(target=recibirMensajes,args=(cliente,))
hilo.daemon = True
hilo.start()

while True:
    mensaje = input("tu: ")
    cliente.send(mensaje.encode("utf-8"))

    if mensaje.lower() == "adios":
        break

# Cerrar
cliente.close()