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
                return False

        except:
            return False
        

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
        try:
            cliente.send(mensaje.encode("utf-8"))
        except:
            pass
        break
    try:
        cliente.send(mensaje.encode("utf-8"))
    except:
        while True:
            try:
                print("Reconectando...")
                time.sleep(3)
                cliente.close()
                cliente = conectar()
                
                # recibe la bienvenida del servidor nuevamente
                solicitud = cliente.recv(1024).decode("utf-8")
                cliente.send(nombre.encode("utf-8"))
                
                # reinicia el hilo de recepción
                hilo = threading.Thread(target=recibirMensajes,args=(cliente,))
                hilo.daemon = True
                hilo.start()
                
                # reenvía el mensaje
                cliente.send(mensaje.encode("utf-8"))
                break  # Sale del while si se reconectó correctamente
            except:
                continue  # Repite el intento

# Cerrar
cliente.close()