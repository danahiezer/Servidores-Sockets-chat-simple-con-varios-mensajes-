import socket
import threading
import time

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

def conectar():
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect(("localhost", 5000))
            return cliente
        except:
            print("Servidor no disponible. conectando...")
            time.sleep(3)

cliente = conectar()

# recibe la bienvenida del servidor
solicitud = cliente.recv(1024).decode("utf-8")
nombre = input(solicitud)
cliente.send(nombre.encode("utf-8"))
# creamos un hilo para que pueda escuchar a los demas clientes y a la vez poder enviar mensajes
hilo = threading.Thread(target=recibirMensajes,args=(cliente,))
hilo.daemon = True
hilo.start()
# ciclo para poder enviar mensaje
while True:
    mensaje = input()

    if mensaje.lower() == "adios":
        cliente.send(mensaje.encode("utf-8"))
        break
    try:
        cliente.send(mensaje.encode("utf-8"))
    except:
        print("error al enviar mensaje")
# Cerrar
cliente.close()